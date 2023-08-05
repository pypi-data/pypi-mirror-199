import configparser
import os
from pathlib import Path

import boto3
from pkg_resources import parse_version


class ManagerSSOError(Exception):
    pass


class UpdateCredentialsError(ManagerSSOError):
    pass


class LoginSSOError(ManagerSSOError):
    pass


class ManagerSSO:
    def __init__(self):
        self.min_version = parse_version('1.26.60')

    def sso_update_credentials(self):
        if self.min_version > parse_version(boto3.__version__):
            raise UpdateCredentialsError('Unable to execute: boto3 requires version ≥ ' + self.min_version.__str__())

        session = boto3.Session()

        config = configparser.ConfigParser()

        credentials = session.get_credentials()

        if credentials is None:
            raise UpdateCredentialsError()

        config.add_section('default')
        config.set('default', 'aws_access_key_id', credentials.access_key)
        config.set('default', 'aws_secret_access_key', credentials.secret_key)
        config.set('default', 'aws_session_token', credentials.token)

        filepath = Path.home().joinpath('.aws', 'credentials').resolve()

        with open(filepath, 'w') as file:
            config.write(file)

    @staticmethod
    def sso_login():
        if os.system('aws sso login') != 0:
            raise LoginSSOError('Erro ao fazer login no SSO')
