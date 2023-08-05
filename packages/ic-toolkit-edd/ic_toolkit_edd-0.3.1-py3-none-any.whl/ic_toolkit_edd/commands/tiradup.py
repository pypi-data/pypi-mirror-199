import re
import sys
import typer

from ic_toolkit_edd.abstract.utilities import Clipboard


def tiradup_handler(colocar_aspas: bool):
    typer.echo("Entre os valores com duplicata e pressione enter:")
    values_input = ''
    for line in sys.stdin:
        if line == "\n" or line == "":
            break
        values_input += line
    values_input = values_input.strip()
    values_input = [prot_ for prot_ in re.split(r",(?!\s)|,?\s+", values_input) if prot_ != '']
    typer.echo(f"</> Len COM DUPLICAÇÕES: {len(values_input)}")
    typer.echo(f"</> Len SEM DUPLICAÇÕES: {len(set(values_input))}")
    typer.echo('Protocolos SEM duplicações copiados para área de transferência:')

    if colocar_aspas:
        typer.echo(str(set(values_input))[1:-1].replace("'", '"'))
        clipboard = Clipboard()
        clipboard.copy(str(set(values_input))[1:-1].replace("'", '"'))
    else:
        typer.echo(", ".join(set(values_input)))
        clipboard = Clipboard()
        clipboard.copy(", ".join(set(values_input)))
