import json
from pathlib import Path
from typing import List

from ic_toolkit_edd.abstract.credentials import get_default
from ic_toolkit_edd.abstract.utilities import FileExtension
from ic_toolkit_edd.beta.arquivo.abstract import ArquivoAbstract
from ic_toolkit_edd.beta.arquivo.original import ArquivoOriginal
from ic_toolkit_edd.beta.arquivo.padronizado import ArquivoPadronizado
from ic_toolkit_edd.beta.arquivo.parseado import ArquivoParseado
from ic_toolkit_edd.beta.identify import Identify, IdentifyResult
from ic_toolkit_edd.beta.input import InputTextConfig
from ic_toolkit_edd.beta.input_type import InputType, Project, input_project, project_source
from ic_toolkit_edd.beta.pdf2txt import Pdf2Txt


class ArquivoFactory:
    @classmethod
    def get_instace(cls, input_type: InputType, *args, **kwargs) -> ArquivoAbstract:
        if input_type == InputType.id_arquivo_original:
            return ArquivoOriginal(*args, **kwargs)
        if input_type == InputType.id_arquivo_parseado:
            return ArquivoParseado(*args, **kwargs)
        if input_type == InputType.id_arquivo_padronizado:
            return ArquivoPadronizado(*args, **kwargs)


class Helper:
    def __init__(self):
        self.provider = get_default(auto_load=True)
        self.identify = Identify()

    @property
    def identify_pdf(self):
        return Path(self.provider.github_path, project_source[Project.identify])

    @property
    def identify_pdf_test_file(self):
        return self.identify_pdf.joinpath('src', 'test', 'java', 'test_config.json')

    @property
    def parser_txt2csv(self):
        return Path(self.provider.github_path, project_source[Project.txt2csv])

    @property
    def parser_txt2csv_test_file(self):
        return self.parser_txt2csv.joinpath('src', 'test', 'parser_config', 'toolkit.json')

    @property
    def padronizador(self):
        return Path(self.provider.github_path, project_source[Project.padronizador])

    @property
    def padronizador_test_file(self):
        return self.padronizador.joinpath('tests', 'jsons', 'toolkit', 'sample_request.json')

    @classmethod
    def __get_test_arquivo_parseado__(cls, inputs: List[InputTextConfig]):
        return {
            'input': [entry.dict for entry in inputs],
            'output': {
                'bucket': 'ic-transient',
                'prefix': 'txt2csv/'
            }
        }

    def get_test_txt2csv(self, arquivo: ArquivoAbstract, payload: IdentifyResult):
        result = []
        for response in Pdf2Txt(arquivo.s3).send_request(payload.strippers):
            config = InputTextConfig(
                bucket=response.bucket,
                prefix=response.prefix,
                filename=response.filename,
                version_id=response.version_id,
                parser=payload.parser,
                main=result.__len__() == 0,
            )
            result.append(config)
        return self.__get_test_arquivo_parseado__(result)

    def get_test_identify(self, arquivo: ArquivoAbstract):
        return {
            'multifiles': [
                {
                    'bucket': arquivo.s3.bucket,
                    'prefix': arquivo.s3.prefix,
                    'filename': arquivo.s3.filename,
                }
            ]
        }

    def get_test_arquivo_padronizado(self, arquivo: ArquivoAbstract):
        return {
            'function_name': 'Parser',
            's3': {
                'bucket': arquivo.s3.bucket,
                'prefix': arquivo.s3.prefix,
                'filename': arquivo.s3.filename,
                'version_id': arquivo.s3.version_id,
            },
            'icMetadata': {
                'id_prestador': '',
                'id_operadora': '',
                'id_arquivo_original': arquivo.data['id_arquivo_original'].__str__(),
                'id_arquivo_parseado': arquivo.data['id_arquivo_parseado'].__str__(),
                'tipoDocumento': {
                    'tipoDocumento': arquivo.data['tipo_arquivo_1'],
                    'tipoDocumento_complemento1': arquivo.data['tipo_arquivo_2'],
                    'tipoDocumento_complemento2': arquivo.data['tipo_arquivo_3']
                },
                'rawdata_source': {
                    'name': 'Plataforma',
                    'endpoint': 'Upload'
                },
                'usuario': 'IC - ' + self.provider.logger_user
            }
        }

    @classmethod
    def download(cls, input_type: InputType, id_arquivo: int):
        arquivo = ArquivoFactory.get_instace(input_type, id_arquivo)
        arquivo.__load__()
        arquivo.s3.download()

    def gen_test(self, project: Project, id_arquivo: int):
        test_type = input_project[project]
        arquivo = ArquivoFactory.get_instace(test_type, id_arquivo)
        arquivo.__load__()
        if arquivo.extension == FileExtension.PDF:
            print('Obtendo TXT para identificação...')
            for response in Pdf2Txt(arquivo.s3).send_request(['RAW'], end_page=5):
                if project == Project.identify:
                    print('Identificando parser...')
                    payload = self.identify.get_response({
                        'bucket': response.bucket,
                        'prefix': response.prefix,
                        'filename': response.filename,
                    })
                    print(f'Parser: {payload.parser}')
                    print(f'Strippers: {payload.strippers}')
                    sample = self.get_test_identify(arquivo)
                    print(f'Escrevendo sample no projeto: {project.name}...')
                    result = json.dumps(sample, indent=2, ensure_ascii=False)
                    with open(self.identify_pdf_test_file, mode='w', encoding='utf-8') as file:
                        file.write(result)
                    print('Sample request implementado')
                    return result
                elif project == Project.txt2csv and arquivo.extension == FileExtension.PDF:
                    print('Identificando parser...')
                    payload = self.identify.get_response({
                        'bucket': response.bucket,
                        'prefix': response.prefix,
                        'filename': response.filename,
                    })
                    print(f'Parser: {payload.parser}')
                    print(f'Strippers: {payload.strippers}')
                    sample = self.get_test_txt2csv(arquivo, payload)
                    print(f'Escrevendo sample no projeto: {project.name}...')
                    result = json.dumps(sample, indent=2, ensure_ascii=False)
                    with open(self.parser_txt2csv_test_file, mode='w', encoding='utf-8') as file:
                        file.write(result)
                    print('Sample request implementado')
                    return result
        elif project == Project.padronizador:
            sample = self.get_test_arquivo_padronizado(arquivo)
            result = json.dumps(sample, indent=4, ensure_ascii=False)
            with open(self.padronizador_test_file, mode='w', encoding='utf-8') as file:
                file.write(result)
            return result
        else:
            print('Formato de arquivo não suportado')

    @classmethod
    def pdf2txt(cls, id_arquivo: int, strippers: list):
        arquivo = ArquivoFactory.get_instace(InputType.id_arquivo_original, id_arquivo)
        arquivo.__load__()
        return Pdf2Txt(arquivo.s3).send_request(strippers)


def run():
    helper = Helper()
    helper.gen_test(Project.padronizador, 140388477)


if __name__ == '__main__':
    run()
