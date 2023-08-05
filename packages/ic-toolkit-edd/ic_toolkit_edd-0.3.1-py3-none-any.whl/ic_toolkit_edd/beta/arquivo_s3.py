import json
import posixpath
import re
from pathlib import Path
from typing import Optional, Dict

import boto3


class ArquivoS3Error(Exception):
    pass


class CannotConnectS3(ArquivoS3Error):
    pass


class ErrorParseS3URI(ArquivoS3Error):
    pass


class ArquivoS3:
    def __init__(self, bucket: str, prefix: str, filename: str, version_id: Optional[str] = None):
        self.bucket = bucket
        self.prefix = prefix
        self.filename = filename

        self.object = self.__get_object__()

        if version_id is None:
            self.version_id = self.object.get('VersionId')
        else:
            self.version_id = version_id

        self.etag = self.object.get('ETag')

    def extension(self):
        result = re.search(r'(?P<extension>[^.]+)(?=\\.)$', self.filename)
        if result:
            return result.group('extension')
        return None

    @property
    def dict(self):
        return {
            'bucket': self.bucket,
            'prefix': self.prefix,
            'filename': self.filename,
            'version_id': self.version_id
        }

    def __str__(self):
        return json.dumps(self.dict, indent=4, ensure_ascii=False)

    @property
    def key(self):
        return posixpath.join(self.prefix, self.filename)

    @property
    def uri(self):
        return f's3://{posixpath.join(self.bucket, self.prefix, self.filename)}'

    @property
    def object_name(self):
        return posixpath.join(self.prefix, self.filename)

    @property
    def __s3__(self):
        return boto3.client('s3')

    def __get_object__(self):
        try:
            return self.__s3__.get_object(Bucket=self.bucket, Key=self.key)
        except Exception as e:
            raise CannotConnectS3(e) from e

    def __get_bytes__(self):
        return self.object['Body'].read()

    @staticmethod
    def from_dict(response: Dict):
        return ArquivoS3(
            bucket=response.get('bucket'),
            prefix=response.get('prefix'),
            filename=response.get('filename'),
        )

    @staticmethod
    def parse_uri(uri: str):
        result = re.search(r's3://(?P<bucket>[^/]+)/(?P<prefix>.+/)(?P<filename>[^/]+)', uri)
        if result:
            return ArquivoS3(
                bucket=result.group('bucket'),
                prefix=result.group('prefix'),
                filename=result.group('filename'),
            )
        else:
            raise ErrorParseS3URI()

    @staticmethod
    def get_default_download_path():
        return Path.home().joinpath('Downloads')

    def get_download_filepath(self):
        return self.get_default_download_path().joinpath(self.filename)

    def download(self):
        print(f'Baixando: {self.filename}')
        try:
            file_bytes = self.__get_bytes__()
            with open(self.get_download_filepath(), 'wb') as file:
                file.write(file_bytes)
            print('Arquivo baixado')
        except Exception as e:
            print(f'Erro ao baixar arquivo: {e}')
