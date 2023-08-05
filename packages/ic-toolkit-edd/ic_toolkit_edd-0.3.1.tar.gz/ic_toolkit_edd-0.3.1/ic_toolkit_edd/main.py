import base64
import re
import sys
from pathlib import Path

import pandas as pd
import typer
from botocore.exceptions import UnauthorizedSSOTokenError

import ic_toolkit_edd
from ic_toolkit_edd.abstract.file_downloader import download_file
from ic_toolkit_edd.abstract.s3_utils import S3Object
from ic_toolkit_edd.abstract.utilities import Clipboard, FileIdTypes
from ic_toolkit_edd.abstract.utilities import PdfStrippers, PipelineSteps, ConfigMode
from ic_toolkit_edd.beta import main
from ic_toolkit_edd.beta.helper import Helper
from ic_toolkit_edd.beta.input_type import InputType, PipelineType, Project
from ic_toolkit_edd.commands.config import config_handler
from ic_toolkit_edd.commands.cvtpdf import cvtpdf_handler
from ic_toolkit_edd.commands.gethash import gethash_handler
from ic_toolkit_edd.commands.reexec import reexec_handler
from ic_toolkit_edd.commands.sso import sso_handler
from ic_toolkit_edd.commands.tiradup import tiradup_handler
from ic_toolkit_edd.commands.upload import upload_handler
from ic_toolkit_edd.commands.walk import walk_handler

app = typer.Typer()

app.add_typer(main.app, name='beta')


@app.command()
def version():
    """exibe a versao atual do toolkit"""
    print(f'Versao atual: {ic_toolkit_edd.__version__}')


@app.command()
def getcwd():
    """exibe a diretorio atual"""
    path = Path()
    print(f'Pasta atual: {path.resolve()}')


@app.command()
def sso(
        login: bool = typer.Option(False, '--login', '-l', help='faz login antes de atualizar das credenciais')
):
    """roda a solucao magica do sso"""
    sso_handler(login)


@app.command()
def config(
        show: bool = typer.Option(False, '--show', '-s', help='exibe as credenciais salvas'),
        mode: ConfigMode = typer.Option(ConfigMode.classic, '--mode', '-m', help='tipo de configuracao')
):
    """configura as credenciais (mysql, logger)"""
    config_handler(show, mode)


@app.command()
def downpadr(
        id_arq: str,
        tipo_id: FileIdTypes = typer.Option(FileIdTypes.padronizado, "--tipo-id", "-t"),
        output_path: Path = typer.Option("./", "--output-path", "-o", exists=True, file_okay=False)
):
    download_file(FileIdTypes.padronizado, tipo_id, id_arq, str(output_path))


@app.command()
def downpars(
        id_arq: str,
        tipo_id: FileIdTypes = typer.Option(FileIdTypes.parseado, "--tipo-id", "-t"),
        output_path: Path = typer.Option("./", "--output-path", "-o", exists=True, file_okay=False)
):
    download_file(FileIdTypes.parseado, tipo_id, id_arq, str(output_path))


@app.command()
def downorig(
        id_arq: str,
        tipo_id: FileIdTypes = typer.Option(FileIdTypes.original, "--tipo-id", "-t"),
        output_path: Path = typer.Option("./", "--output-path", "-o", exists=True, file_okay=False)
):
    download_file(FileIdTypes.original, tipo_id, id_arq, str(output_path))


@app.command()
def gethash(plain_md5: bool = False, sha256: bool = False):
    gethash_handler(plain_md5, sha256)


@app.command()
def upload(
        path: Path = typer.Option(".", "--dir", "-d", exists=True, file_okay=False),
        filename_prefix: str = typer.Option("", "--prefix", "-p"),
        ignore_hashing: bool = typer.Option(False, "--desabilitar-hashing", "-H")
):
    upload_handler(path, filename_prefix, ignore_hashing)


@app.command()
def cvtpdf(
        input_path: Path = typer.Option(".", "--input-dir", "-i", exists=True),
        stripper: PdfStrippers = typer.Option("raw", "--stripper", "-s", prompt="Escolha o stripper:"),
        output_path: Path = typer.Option(".", "--output-dir", "-o", exists=True, file_okay=False, writable=True)
):
    cvtpdf_handler(input_path, stripper, output_path)


@app.command()
def equiv(
        destination_df: str = typer.Option(..., "--destino", "-d", prompt="Entre o nome do dataframe de destino"),
        origin_df: str = typer.Option("df", "--origem", "-o")
):
    typer.prompt(
        "Copie as três primeiras colunas da planilha de equivalência e pressione enter...", default="",
        show_default=False, prompt_suffix=""
    )
    equivalence_template = f"self.{destination_df}['{{0}}'] = self.{origin_df}['{{1}}']\n"
    equivalence_hardcoded_template = f"self.{destination_df}['{{0}}'] = {{1}}\n"
    equivalences = pd.read_clipboard()
    if len(equivalences.columns) != 3 or len(equivalences) == 0:
        typer.echo(" " + typer.style("\nERRO: EQUIVALÊNCIAS NÃO ENCONTRADAS", typer.colors.WHITE, typer.colors.RED))
        typer.echo("\nAs células copiadas estão vazias ou não estão no formato correto")
        typer.echo(
            'Certifique-se de copiar as três primeiras colunas da '
            'planilha ("Coluna (DOCUMENTO)", "OBS" e "Equivalencia")'
        )
        return
    equivalences.drop(equivalences.columns[1], axis=1, inplace=True)
    equivalences.iloc[:, 1] = equivalences[equivalences.columns[1]].str.replace(r"^\s*$", "", regex=True).replace("",
                                                                                                                  pd.NA)
    equivalences.dropna(inplace=True)
    n_columns = equivalences.shape[0]
    equivalence_code = ""
    equivalence_code_hardcoded = ""
    for i in range(n_columns):
        if "'" in equivalences.iloc[i, 1]:
            equivalence_code_hardcoded += equivalence_hardcoded_template.format(equivalences.iloc[i, 0].strip(),
                                                                                equivalences.iloc[i, 1].strip())
        else:
            equivalence_code += equivalence_template.format(equivalences.iloc[i, 0].strip(),
                                                            equivalences.iloc[i, 1].strip())
    equivalence_code += equivalence_code_hardcoded.strip()
    clipboard = Clipboard()
    clipboard.copy(equivalence_code)
    typer.echo(typer.style("\nSUCESSO\n", fg=typer.colors.GREEN, bold=True))
    typer.echo("O código de equivalência foi copiado para sua área de transferência")


@app.command()
def verids3(
        bucket: str = typer.Option(..., prompt=True), prefix: str = typer.Option(..., prompt=True),
        filename: str = typer.Option(..., prompt=True)
):
    clipboard = Clipboard()
    __object__ = S3Object(bucket, prefix, filename)
    try:
        version_id = __object__.version_id()
        clipboard.copy(version_id)
        typer.echo(typer.style("\nSUCESSO\n", fg=typer.colors.GREEN, bold=True))
        typer.echo(f"ID da versão na AWS: {version_id}")
        typer.echo("O ID da versão também foi copiado para sua área de transferência")
    except Exception as e:
        typer.echo("\n\n" + typer.style("ERRO AO OBTER O VERSION_ID!", typer.colors.WHITE, typer.colors.RED))
        typer.echo(f"\nExceção encontrada: {e}")


@app.command()
def downs3(
        bucket: str = typer.Option(..., prompt=True), prefix: str = typer.Option(..., prompt=True),
        filename: str = typer.Option(..., prompt=True),
        output_path: Path = typer.Option(
            ".", "--output-dir", "-o", prompt=True, exists=True, file_okay=False, writable=True
        )
):
    __object__ = S3Object(bucket, prefix, filename)
    try:
        __object__.download(str(output_path))
    except FileExistsError:
        choice = typer.confirm("O arquivo a ser baixado já existe no diretório de destino. Substituir?")
        if choice:
            __object__.download(output_path.resolve().__str__(), True)
        else:
            typer.echo(typer.style("ERRO AO BAIXAR O OBJETO!", typer.colors.WHITE, typer.colors.RED))
            typer.echo(f"\nO objeto {__object__} já existe no diretório \"{output_path}\"")
            return
    except Exception as e:
        typer.echo("\n\n" + typer.style("ERRO AO BAIXAR O OBJETO!", typer.colors.WHITE, typer.colors.RED))
        typer.echo(f"\nExceção encontrada: {e}")
    typer.echo(typer.style("\nSUCESSO\n", fg=typer.colors.GREEN, bold=True))
    typer.echo(f"O arquivo foi baixado com sucesso para o diretório {output_path}")


@app.command()
def uploads3(
        bucket: str = typer.Option(..., prompt=True), prefix: str = typer.Option(..., prompt=True),
        filename: str = typer.Option(""),
        input_path: Path = typer.Option(..., "--input-file", "-i", prompt=True, exists=True, dir_okay=False)
):
    if filename == "":
        filename = typer.prompt("filename", default=input_path.name)
    obj = S3Object('', '', '')
    try:
        obj = S3Object.upload_file(str(input_path), bucket, prefix, filename)
    except FileExistsError:
        choice = typer.confirm(
            "O arquivo a ser enviado para a s3 já existe no bucket/prefixo informado. Deseja substituir o objeto?")
        if choice:
            obj = S3Object.upload_file(str(input_path), bucket, prefix, filename, override_object=True)
        else:
            typer.echo(typer.style("ERRO AO ENVIAR O ARQUIVO PARA A S3!", typer.colors.WHITE, typer.colors.RED))
            typer.echo(f"\nO arquivo \"{input_path}\" já existe no bucket/prefixo informado")
            return
    except Exception as e:
        typer.echo("\n\n" + typer.style("ERRO AO CARREGAR O ARQUIVO PARA A S3", typer.colors.WHITE, typer.colors.RED))
        typer.echo(f"\nExceção encontrada ao fazer o upload do arquivo \"{input_path}\": {e}")
    typer.echo(typer.style("\nSUCESSO\n", fg=typer.colors.GREEN, bold=True))
    typer.echo("O arquivo foi salvo com sucesso na S3 como o objeto:")
    typer.echo(str(obj))


@app.command()
def reexec(
        passo: PipelineSteps = typer.Option(None, "--passo-pipeline", "-p"),
        intervalo: int = typer.Option(None, "--tempo-intervalo", "-t"),
        printar_ids: bool = typer.Option(False, "--mostrar-ids", "-i"),
        prioritario: bool = typer.Option(False, "--prioritario")
):
    reexec_handler(passo, intervalo, printar_ids, prioritario)


@app.command()
def filtro(
        id_arq: str, creditos: bool = typer.Option(False, "--creditos")
):
    if creditos:
        rota = "conciliacao/creditos"
    else:
        rota = "glosas/auditar-glosas"
    if "," in id_arq:
        filtro = '{"id_arquivo":{"$in":[filter]}}'.replace("filter", id_arq)
    else:
        filtro = '{"id_arquivo":{"$eq":filter}}'.replace("filter", id_arq)
    base64_filtro = str(base64.b64encode(filtro.encode('utf-8'))).replace("b'", "").replace("'", "")
    clipboard = Clipboard()
    clipboard.copy(f"https://app.intuitivecare.com/{rota}/protocolo/?filters={base64_filtro}")
    typer.echo("O filtro foi copiado para a área de transferência")


@app.command()
def formatprot():
    """
    Colocar aspas e vírgula em vários protocolos, deixando-os passíveis de query no banco. Ex:
    Input:
    340098590119
    340098600325
    Output:
    "340098590119", "340098600325"
    """
    typer.echo("Entre os protocolos e pressione enter:")
    prots_input = ''
    for line in sys.stdin:
        if line == "\n" or line == "":
            break
        prots_input += line
    prots_input = prots_input.strip()
    prots_input = [prot_ for prot_ in re.split(r",(?!\s)|,?\s+", prots_input) if prot_ != '']
    typer.echo('Protocolos formatados com aspas copiados para a área de transferência:')
    typer.echo(str(prots_input)[1:-1].replace("'", '"'))
    clipboard = Clipboard()
    clipboard.copy(str(prots_input)[1:-1].replace("'", '"'))


@app.command()
def tiradup(
        colocar_aspas: bool = typer.Option(False, "--aspas")
):
    tiradup_handler(colocar_aspas)


@app.command()
def test(
        project: Project,
        id_arquivo: int,
):
    helper = Helper()
    try:
        helper.gen_test(project, id_arquivo)
        typer.echo('Arquivo de teste gerado!')
    except UnauthorizedSSOTokenError:
        typer.echo('Conexão com SSO expirou, favor executar: ic sso --login')
    except Exception as e:
        typer.echo(f'Erro ao gerar arquivo de teste: {e}')


@app.command()
def walk(input_type: InputType, output_type: PipelineType):
    walk_handler(input_type, output_type)
