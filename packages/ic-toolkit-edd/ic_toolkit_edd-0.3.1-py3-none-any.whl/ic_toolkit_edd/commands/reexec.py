import re
import sys

import click
import typer

from ic_toolkit_edd.abstract.credentials import get_default
from ic_toolkit_edd.abstract.re_execution import ReParsear, RePadronizar, ReLoad, ReProcessar
from ic_toolkit_edd.abstract.utilities import PipelineSteps, pipeline_file_id_type, FileIdTypes


def reexec_handler(passo: PipelineSteps, intervalo: int, printar_ids: bool, prioritario: bool):
    if passo is None or intervalo is None:
        if passo is None:
            passo = PipelineSteps(typer.prompt(
                "Escolha o passo do pipeline para reprocessar",
                type=click.types.Choice(list(map(lambda x: x.value, PipelineSteps)))
            ))
        if intervalo is None:
            intervalo = typer.prompt(
                "Entre o intervalo entre cada requisição de reprocessamento (em segundos)",
                type=click.types.IntRange(min=0)
            )
        printar_ids = typer.confirm("Deseja printar os IDs?", default=True)
        if passo == PipelineSteps.load:
            prioritario = typer.confirm("Deseja usar o load antigo (prioritário)?", default=False)
    id_type = pipeline_file_id_type[passo]
    id_type_name = "id_arquivo" + (f"_{id_type.value}" if id_type != FileIdTypes.arquivo else "")
    typer.echo(
        f"Entre os {id_type_name}'s separados por espaços, enter ou "
        f"vírgulas. Ao final, deixe uma linha vazia e pressione enter..."
    )
    ids_input = ''
    for line in sys.stdin:
        if line == "\n" or line == "":
            break
        ids_input += line
    ids_input = ids_input.strip()
    ids = [id_ for id_ in re.split(r",(?!\s)|,?\s+", ids_input) if id_ != '']
    provider = get_default(auto_load=True)
    re_exec = None
    if passo == PipelineSteps.parsing:
        re_exec = ReParsear(ids, intervalo, provider.logger_user)
    elif passo == PipelineSteps.padronizacao:
        re_exec = RePadronizar(ids, intervalo, provider.logger_user)
    elif passo == PipelineSteps.load:
        re_exec = ReLoad(ids, intervalo, provider.logger_user)
    elif passo == PipelineSteps.pos_proc:
        re_exec = ReProcessar(ids, intervalo, provider.logger_user)
    try:
        re_exec.run(prioritario=prioritario, printar_ids=printar_ids)
    except Exception as e:
        typer.echo("\n\n" + typer.style("ERRO AO REPROCESSAR ARQUIVOS!", typer.colors.WHITE, typer.colors.RED) + "\n")
        typer.echo(f"A seguinte exceção foi encontrada: {e}")
