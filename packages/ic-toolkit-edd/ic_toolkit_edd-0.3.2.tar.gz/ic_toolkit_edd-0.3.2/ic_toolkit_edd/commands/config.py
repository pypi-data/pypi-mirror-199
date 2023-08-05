import typer

from ic_toolkit_edd.abstract.credentials import get_default, CredentialsProviderException, BetaProvider, ClassicProvider
from ic_toolkit_edd.abstract.utilities import ConfigMode


def config_handler(show: bool, mode: ConfigMode):
    if show:
        try:
            provider = get_default(auto_load=True)
            typer.echo(provider.__str__())
        except CredentialsProviderException as e:
            typer.echo(typer.style(f'Erro: {e}', fg=typer.colors.RED))
    else:
        if mode == ConfigMode.beta:
            provider = BetaProvider()
        else:
            provider = ClassicProvider()
        typer.echo('[mysql]')
        provider.mysql_user = typer.prompt('user')
        provider.mysql_password = typer.prompt('password')
        provider.mysql_host = typer.prompt('host')
        provider.mysql_port = typer.prompt('port')
        provider.mysql_db = typer.prompt('database')
        typer.echo()
        typer.echo('[logger]')
        provider.logger_user = typer.prompt('user (seu usuario da IC)')
        typer.echo()
        typer.echo('[github]')
        provider.github_path = typer.prompt('path (sua pasta default para repositórios do GitHub)')
        provider.save()
