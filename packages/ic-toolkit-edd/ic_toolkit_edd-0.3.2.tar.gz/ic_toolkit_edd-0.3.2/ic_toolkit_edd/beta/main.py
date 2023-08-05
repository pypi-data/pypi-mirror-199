import typer

from ic_toolkit_edd.beta.etag import calculate_s3_etag
from ic_toolkit_edd.beta.helper import Helper
from ic_toolkit_edd.beta.input_type import InputType
from ic_toolkit_edd.beta.list_file import get_files

app = typer.Typer()


@app.command()
def downorig(id_arquivo: int):
    """baixa arquivo original"""
    helper = Helper()
    helper.download(InputType.id_arquivo_original, id_arquivo)


@app.command()
def downpars(id_arquivo: int):
    """baixa arquivo parseado"""
    helper = Helper()
    helper.download(InputType.id_arquivo_parseado, id_arquivo)


@app.command()
def downpadr(id_arquivo: int):
    """baixa arquivo padronizado"""
    helper = Helper()
    helper.download(InputType.id_arquivo_padronizado, id_arquivo)


@app.command()
def etag():
    """lista etag dos arquivos na pasta atual"""
    result = map(calculate_s3_etag, get_files())
    result = '\n'.join(result)
    print(result)


if __name__ == "__main__":
    app()
