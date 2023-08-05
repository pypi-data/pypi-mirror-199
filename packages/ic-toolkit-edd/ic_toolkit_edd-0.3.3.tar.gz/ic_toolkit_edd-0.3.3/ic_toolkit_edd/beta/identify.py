import json
import sys
from typing import Dict, List

import boto3


class IdentifyResult:
    def __init__(self, parser: str, strippers: List[str]):
        self.parser = parser
        self.strippers = strippers

    @classmethod
    def from_dict(cls, response):
        return IdentifyResult(
            parser=response.get('parser'),
            strippers=response.get('strippers'),
        )


class Identify:
    @property
    def __client__(self):
        return boto3.client('lambda')

    def __get_response__(self, payload: Dict):
        response = self.__client__.invoke(
            FunctionName='ETL-Identify-PDF',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        return json.loads(
            response['Payload'].read()
        )

    def get_response(self, payload: Dict):
        try:
            response = self.__get_response__(payload)
            if 'errorMessage' in response:
                print('Error Message: {}'.format(response['errorMessage']))
                print('Error Type: {}'.format(response['errorType']))
                print('Stack Trace:')
                for trace in response['stackTrace']:
                    print(f'\t{trace}')
                sys.exit()
            return IdentifyResult.from_dict(response)
        except:
            return None
