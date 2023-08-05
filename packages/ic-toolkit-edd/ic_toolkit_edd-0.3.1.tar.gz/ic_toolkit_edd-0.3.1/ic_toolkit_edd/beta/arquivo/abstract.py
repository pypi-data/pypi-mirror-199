from abc import ABC, abstractmethod
from typing import Optional, Dict

from ic_toolkit_edd.abstract.database import get_connection, get_cursor
from ic_toolkit_edd.abstract.utilities import FileExtension
from ic_toolkit_edd.beta.arquivo_s3 import ArquivoS3


class ArquivoException(Exception):
    pass


class ArquivoAbstract(ABC):
    def __init__(self, id_arquivo: int):
        self.id_arquivo = id_arquivo
        self.data: Optional[Dict] = None
        self.s3: Optional[ArquivoS3] = None

    @property
    @abstractmethod
    def __query__(self) -> str:
        pass

    def __load__(self):
        try:
            with get_connection() as connection:
                with get_cursor(connection) as cursor:
                    cursor.execute(self.__query__, {'id_arquivo': self.id_arquivo})
                    self.data = cursor.fetchone()
            self.s3 = ArquivoS3.from_dict(self.data)
        except Exception as e:
            raise ArquivoException(e) from e

    @property
    def extension(self):
        return FileExtension.from_filename(self.s3.filename)
