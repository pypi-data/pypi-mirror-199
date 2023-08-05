from enum import Enum
from pathlib import Path

import pyperclip


def get_extension(filename: str) -> str:
    return Path(filename).suffix.lstrip('.').lower()


class Clipboard:
    @classmethod
    def copy(cls, text: str) -> None:
        pyperclip.copy(text)

    @classmethod
    def paste(cls) -> str:
        try:
            return pyperclip.paste()
        except pyperclip.PyperclipException:
            return ''


class FileIdTypes(str, Enum):
    original = 'original'
    parseado = 'parseado'
    padronizado = 'padronizado'
    arquivo = 'arquivo'


class FileExtension(str, Enum):
    CSV = 'csv'
    HTML = 'html'
    JSON = 'json'
    PDF = 'pdf'
    TXT = 'txt'
    XLS = 'xls'
    XLSM = 'xlsm'
    XLSX = 'xlsx'
    XML = 'xml'
    ZIP = 'zip'

    @classmethod
    def from_filename(cls, filename: str):
        return cls(
            value=get_extension(filename)
        )


class PdfStrippers(str, Enum):
    raw = 'RAW',
    layout = 'LAYOUT',
    ordered_raw = 'ORDERED_RAW',
    ordered_layout = 'ORDERED_LAYOUT'


class PipelineSteps(str, Enum):
    parsing = 'pars',
    padronizacao = 'padr',
    load = 'load',
    pos_proc = 'proc'


pipeline_file_id_type = {
    PipelineSteps.parsing: FileIdTypes.original,
    PipelineSteps.padronizacao: FileIdTypes.parseado,
    PipelineSteps.load: FileIdTypes.padronizado,
    PipelineSteps.pos_proc: FileIdTypes.arquivo,
}


class ConfigMode(str, Enum):
    classic = 'classic'
    beta = 'beta'
