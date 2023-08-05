import os
import re
from pathlib import Path

import typer

from ic_toolkit_edd.abstract.s3_utils import S3Object
from ic_toolkit_edd.abstract.utilities import FileExtension
from ic_toolkit_edd.commands.gethash import gethash_handler


def upload_handler(path: Path, filename_prefix: str, ignore_hashing: bool):
    filename_list = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    set_prefixo = "n"
    if filename_prefix:
        print()
        set_prefixo = input(
            f"/> Fazer upload de {len(os.listdir())} arquivo(s) setando o prefixo '{filename_prefix}'? [S/n] ").lower()

    with typer.progressbar(range(len(filename_list)), length=len(filename_list)) as progress:
        for i in progress:
            prefix = "Original/Plataforma/Upload/Old/"

            if set_prefixo in "sy":
                os.rename(os.path.join(path, filename_list[i]),
                          os.path.join(path, f"{filename_prefix}_{filename_list[i]}")
                          )
                filename_list[i] = f"{filename_prefix}_{filename_list[i]}"

            file_name = filename_list[i]
            file_type = re.search(r'.*\.(.*)$', file_name).group(1)
            file_path = os.path.join(path, file_name)
            try:
                file_type = FileExtension(file_type.lower())
            except ValueError:
                typer.echo(' ' + typer.style("ERRO", fg=typer.colors.WHITE, bg=typer.colors.RED))
                typer.echo(f'\nTipo de arquivo ".{file_type}" não suportado pela plataforma')
                return
            bucket = 'ic-filerepo-nvus'
            prefix += file_type.value + '/'
            try:
                S3Object.upload_file(file_path, bucket, prefix, file_name)
            except ConnectionError as e:
                typer.echo(' ' + typer.style("ERRO NO UPLOAD DO ARQUIVO", fg=typer.colors.WHITE, bg=typer.colors.RED))
                typer.echo(f'\nO cliente da S3 encontrou o seguinte erro fazer o upload do arquivo: {e}')
                return
            except RuntimeError as e:
                typer.echo(' ' + typer.style("ERRO NO UPLOAD DO ARQUIVO", fg=typer.colors.WHITE, bg=typer.colors.RED))
                typer.echo(f'\nExceção encontrada durante o upload do arquivo: {e}')
                return
            except FileExistsError as e:
                typer.echo(' ' + typer.style("ERRO NO UPLOAD DO ARQUIVO", fg=typer.colors.WHITE, bg=typer.colors.RED))
                typer.echo("Arquivo já existente no S3")
                continue

    typer.echo(typer.style(" SUCESSO", fg=typer.colors.GREEN, bold=True))
    if not ignore_hashing:
        gethash_handler(plain_md5=False, sha256=False)
