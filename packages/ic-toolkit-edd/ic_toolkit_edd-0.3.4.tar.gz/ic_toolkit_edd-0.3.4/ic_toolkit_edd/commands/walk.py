import typer
import json
from ic_toolkit_edd.beta.input_type import InputType, PipelineType
from ic_toolkit_edd.beta.walk import walk_by


def walk_handler(input_type: InputType, output_type: PipelineType):
    typer.echo(f'Informe a lista de {input_type.name}, separado por quebra de linha (2xEnter para aceitar)')
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line.strip())
        else:
            break
    typer.echo('Analisando pipeline...')
    typer.echo('-' * 60)
    for response in walk_by(input_type, output_type, lines):
        typer.echo(response['this_type'].name)
        typer.echo(typer.style(json.dumps(response['this_stopped_list']), fg=typer.colors.RED))
        typer.echo(typer.style(json.dumps(response['this_passed_list']), fg=typer.colors.GREEN))
        typer.echo('-' * 60)
        if 'output_list' in response:
            typer.echo(response['output_type'].name)
            typer.echo(typer.style(json.dumps(response['output_list']), fg=typer.colors.BLUE))
            typer.echo('-' * 60)


if __name__ == "__main__":
    walk_handler(
        InputType.ic_hash, PipelineType.arquivo_padronizado
    )