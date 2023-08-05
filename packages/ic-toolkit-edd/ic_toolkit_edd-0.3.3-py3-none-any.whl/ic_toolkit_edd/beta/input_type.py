from enum import Enum


class InputType(str, Enum):
    ic_hash = 'hash'
    id_arquivo_original = 'orig'
    id_arquivo_parseado = 'pars'
    id_arquivo_padronizado = 'padr'
    id_arquivo = 'arqv'


class PipelineType(str, Enum):
    arquivo_original = 'orig'
    arquivo_parseado = 'pars'
    arquivo_padronizado = 'padr'
    arquivo = 'arqv'


class Project(str, Enum):
    identify = 'ident'
    txt2csv = 'txt2csv'
    padronizador = 'padr'


input_pipeline = {
    InputType.ic_hash: PipelineType.arquivo_original,
    InputType.id_arquivo_original: PipelineType.arquivo_original,
    InputType.id_arquivo_parseado: PipelineType.arquivo_parseado,
    InputType.id_arquivo_padronizado: PipelineType.arquivo_padronizado,
    InputType.id_arquivo: PipelineType.arquivo,
}

output_pipeline = {
    PipelineType.arquivo_original: InputType.id_arquivo_original,
    PipelineType.arquivo_parseado: InputType.id_arquivo_parseado,
    PipelineType.arquivo: InputType.id_arquivo_padronizado,
}

test_pipeline = {
    PipelineType.arquivo_parseado: InputType.id_arquivo_original,
    PipelineType.arquivo_padronizado: InputType.id_arquivo_parseado,
}

input_project = {
    Project.identify: InputType.id_arquivo_original,
    Project.txt2csv: InputType.id_arquivo_original,
    Project.padronizador: InputType.id_arquivo_parseado,
}

project_source = {
    Project.identify: 'ETL-Identify-PDF',
    Project.txt2csv: 'ETL-Transform-TXT2CSV',
    Project.padronizador: 'ETL-PadronizadorLambda'
}
