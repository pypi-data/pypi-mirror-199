import configparser
import re
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TextIO


class CredentialsProviderException(Exception):
    pass


class CredentialsNotFound(CredentialsProviderException):
    pass


class CredentialsLoadError(CredentialsProviderException):
    pass


class AbstractCredentialsProvider(ABC):
    def __init__(self, auto_load=False):
        self.config = configparser.ConfigParser()
        # create sections
        self.config.add_section('mysql')
        self.config.add_section('logger')
        self.config.add_section('github')
        if auto_load:
            self.load()

    @property
    def mysql_user(self):
        return self.config['mysql'].get('user', fallback='')

    @mysql_user.setter
    def mysql_user(self, value):
        self.config.set('mysql', 'user', value)

    @property
    def mysql_password(self):
        return self.config['mysql'].get('password', fallback='')

    @mysql_password.setter
    def mysql_password(self, value):
        self.config.set('mysql', 'password', value)

    @property
    def mysql_host(self):
        return self.config['mysql'].get('host', fallback='')

    @mysql_host.setter
    def mysql_host(self, value):
        self.config.set('mysql', 'host', value)

    @property
    def mysql_port(self):
        return self.config['mysql'].getint('port', fallback=3306)

    @mysql_port.setter
    def mysql_port(self, value):
        self.config.set('mysql', 'port', value)

    @property
    def mysql_db(self):
        return self.config['mysql'].get('database', fallback='upload')

    @mysql_db.setter
    def mysql_db(self, value):
        self.config.set('mysql', 'database', value)

    @property
    def logger_user(self):
        return self.config['logger'].get('user', fallback='')

    @logger_user.setter
    def logger_user(self, value):
        self.config.set('logger', 'user', value)

    @property
    def github_path(self):
        return self.config['github'].get('path', fallback='')

    @github_path.setter
    def github_path(self, value):
        self.config.set('github', 'path', value)

    @property
    def credentials_path(self):
        return Path.home().joinpath('.intuitivecare')

    @property
    @abstractmethod
    def __filename__(self):
        pass

    @property
    def credentials_file(self):
        return self.credentials_path.joinpath(self.__filename__)

    def get_text(self):
        if self.credentials_file.exists():
            with open(self.credentials_file, 'r') as file:
                return file.read()

    @abstractmethod
    def __validate__(self):
        pass

    @abstractmethod
    def __load__(self):
        pass

    def load(self):
        if not self.credentials_file.resolve().exists():
            raise CredentialsNotFound('Arquivo de configuração não encontrado')
        try:
            self.__load__()
        except KeyError:
            pass
        try:
            self.__validate__()
        except KeyError as e:
            raise CredentialsLoadError(f'Chave {e} não encontrada no arquivo de configuração') from e
        except Exception as e:
            raise CredentialsLoadError(f'Erro desconhecido: {e}') from e

    @abstractmethod
    def __save__(self, file: TextIO):
        pass

    def save(self):
        self.__validate__()
        self.credentials_path.mkdir(exist_ok=True)
        # write a beta credentials
        with open(self.credentials_file.resolve().__str__(), 'w') as file:
            self.__save__(file)

    def convert_to(self, provider):
        credentials = provider()
        credentials.handler = self.config
        return credentials

    def __str__(self):
        output = []
        for section in self.config.sections():
            text = [f'[{section}]']
            for key in self.config[section]:
                if 'pass' in key.lower():
                    __pass__ = '*' * self.config[section][key].__len__()
                    text.append(f'{key}={__pass__}')
                    continue
                text.append(f'{key}={self.config[section][key]}')
            output.append('\n'.join(text))
        return '\n\n'.join(output)


class ClassicProvider(AbstractCredentialsProvider):
    @property
    def __filename__(self):
        return '.credentials'

    def __read_dict__(self):
        lines = tuple()
        if self.get_text():
            lines = re.findall(r'(.+?):(.+)', self.get_text())
        return dict(lines)

    def __load__(self):
        credentials = self.__read_dict__()
        self.config.set('mysql', 'user', credentials['userDB'])
        self.config.set('mysql', 'password', credentials['passwordDB'])
        self.config.set('mysql', 'host', credentials['hostDB'])
        self.config.set('mysql', 'port', credentials['portDB'])
        self.config.set('mysql', 'database', credentials['nameDB'])
        self.config.set('logger', 'user', credentials['userIC'])
        self.config.set('github', 'path', credentials['pathGIT'])

    def __validate__(self):
        if 'user' not in self.config['mysql']:
            raise KeyError('userDB')
        if 'password' not in self.config['mysql']:
            raise KeyError('passwordDB')
        if 'database' not in self.config['mysql']:
            raise KeyError('hostDB')
        if 'host' not in self.config['mysql']:
            raise KeyError('portDB')
        if 'port' not in self.config['mysql']:
            raise KeyError('nameDB')
        if 'user' not in self.config['logger']:
            raise KeyError('userIC')
        if 'path' not in self.config['github']:
            raise KeyError('pathGIT')

    def __save__(self, file: TextIO):
        lines = [
            f'userDB:{self.mysql_user}',
            f'passwordDB:{self.mysql_password}',
            f'hostDB:{self.mysql_host}',
            f'portDB:{self.mysql_port}',
            f'nameDB:{self.mysql_db}',
            f'userIC:{self.logger_user}',
            f'pathGIT:{self.github_path}',
        ]
        output = '\n'.join(lines)
        file.write(output)


class BetaProvider(AbstractCredentialsProvider):
    @property
    def __filename__(self):
        return '.credentials.beta'

    def __load__(self):
        self.config.read(self.credentials_file)

    def __validate__(self):
        if 'user' not in self.config['mysql']:
            raise KeyError('mysql.user')
        if 'password' not in self.config['mysql']:
            raise KeyError('mysql.password')
        if 'database' not in self.config['mysql']:
            raise KeyError('mysql.database')
        if 'host' not in self.config['mysql']:
            raise KeyError('mysql.host')
        if 'port' not in self.config['mysql']:
            raise KeyError('mysql.port')
        if 'user' not in self.config['logger']:
            raise KeyError('logger.user')
        if 'path' not in self.config['github']:
            raise KeyError('github.path')

    def __save__(self, file: TextIO):
        self.config.write(file)


def get_default(auto_load=False, default=BetaProvider) -> AbstractCredentialsProvider:
    classes = [
        BetaProvider,
        ClassicProvider,
    ]
    for cls in classes:
        provider = cls()
        if provider.credentials_file.exists():
            provider.load()
            return provider
    return default(auto_load=auto_load)


def run():
    try:
        provider = get_default(auto_load=True)
        print('Provider: ' + provider.__class__.__name__, end='\n\n')
        print(provider)
    except CredentialsProviderException as e:
        print(f'Erro: {e}')


if __name__ == '__main__':
    run()
