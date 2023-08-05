import json
from typing import Dict, List, Union, Tuple

import requests

from ic_toolkit_edd.beta.arquivo_s3 import ArquivoS3


class Pdf2Txt:
    def __init__(self, config_json: ArquivoS3):
        self.config = config_json
        self.url = 'https://api-transform.intuitivecare.com/prod/transform/pdf2txt/v2'
        self.headers = {
            'Content-Type': 'application/json'
        }

    @staticmethod
    def get_body(config_input: list):
        return {
            'input': config_input,
            'output': {
                'bucket': 'ic-transient',
                'prefix': 'txt2csv/'
            }
        }

    def gen_input(self, config_stripper: str, end_page: int = 0):
        return {
            'bucket': self.config.bucket,
            'prefix': self.config.prefix,
            'filename': self.config.filename,
            'options': {
                'stripper': config_stripper,
                'endPage': end_page,
            }
        }

    @staticmethod
    def normalize_response(response: Dict):
        return ArquivoS3(
            bucket=response.get('Bucket'),
            prefix=response.get('Prefix'),
            filename=response.get('Filename'),
        )

    @classmethod
    def get_response_postman(cls, data: Dict):
        response = data.get('response', [])
        return [
            cls.normalize_response(__data__) for __data__ in response
        ]

    def send_request(self, strippers: List[str], end_page: int = 0):
        config_input = []
        for stripper in strippers:
            gen_input = self.gen_input(stripper, end_page)
            config_input.append(gen_input)
        body = self.get_body(config_input)
        response = requests.post(self.url, data=json.dumps(body), headers=self.headers)
        return self.get_response_postman(response.json())
