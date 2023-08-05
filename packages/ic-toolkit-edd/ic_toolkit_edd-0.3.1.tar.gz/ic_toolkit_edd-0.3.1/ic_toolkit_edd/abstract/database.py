import pandas as pd
from pymysql import Connection, connect
from pymysql.cursors import DictCursor

from ic_toolkit_edd.abstract.credentials import get_default


class ConnectionException(Exception):
    pass


def get_connection() -> Connection:
    provider = get_default(auto_load=True)
    try:
        print('Estabelecedo conexão com o banco...')
        return connect(
            user=provider.mysql_user,
            password=provider.mysql_password,
            host=provider.mysql_host,
            port=provider.mysql_port,
            database=provider.mysql_db,
            cursorclass=DictCursor,
        )
    except Exception as e:
        raise ConnectionException(f'Erro ao criar conexao: {e}') from e


def get_cursor(connection) -> DictCursor:
    return connection.cursor()


def get_dataframe(query: str, args=None) -> pd.DataFrame:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, args)
            return pd.DataFrame.from_records(cursor.fetchall())
