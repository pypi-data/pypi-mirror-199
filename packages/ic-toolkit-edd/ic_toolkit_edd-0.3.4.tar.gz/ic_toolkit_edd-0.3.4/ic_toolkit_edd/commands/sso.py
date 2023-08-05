import sys
import time
from datetime import datetime

import typer
from botocore.exceptions import UnauthorizedSSOTokenError

from ic_toolkit_edd.beta.sso_manager import UpdateCredentialsError, ManagerSSO, LoginSSOError


def sso_handler(login: bool):
    sso_manager = ManagerSSO()
    if login:
        try:
            sso_manager.sso_login()
            typer.echo()
        except LoginSSOError:
            typer.echo('Error authorizing request')
            sys.exit()
    try:
        while True:
            try:
                timestamp = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                sso_manager.sso_update_credentials()
                typer.echo(f'Credenciais atualizadas em {timestamp}')
            except UpdateCredentialsError as e:
                typer.echo(typer.style(f'Erro ao atualizar credenciais: {e}', fg=typer.colors.RED))
            time.sleep(3600)
    except UnauthorizedSSOTokenError:
        typer.echo('Sua conexão SSO expirou, favor executar: ic sso --login')
