from enum import Enum
from pathlib import Path

import pyperclip
import tkinter as tk


def get_extension(filename: str) -> str:
    return Path(filename).suffix.lstrip('.').lower()


class Clipboard:
    def __init__(self):
        self._tk = tk.Tk()
        self._tk.withdraw()

    def copy(self, text: str) -> None:
        try:
            pyperclip.copy(text)
        except pyperclip.PyperclipException:
            self._tk.clipboard_clear()
            self._tk.clipboard_append(text)
            self._tk.after(500, self._tk.destroy)
            self._tk.mainloop()

    def paste(self) -> str:
        try:
            return pyperclip.paste()
        except pyperclip.PyperclipException:
            return self._tk.clipboard_get()
        except tk.TclError:
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
