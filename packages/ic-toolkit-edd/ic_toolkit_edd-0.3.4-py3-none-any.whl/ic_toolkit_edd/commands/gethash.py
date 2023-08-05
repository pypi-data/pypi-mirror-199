import hashlib
import math
import os

import typer

from ic_toolkit_edd.abstract.utilities import Clipboard


def gethash_handler(plain_md5: bool = False, sha256: bool = False):
    aws_chunk_size = 8 * (1024 ** 2)  # 8 Mb
    hash_list = []
    filename_list = [f for f in os.listdir('./') if os.path.isfile(f)]
    for file in filename_list:
        with open(file, "rb") as f:
            data = f.read()
            if not plain_md5 and len(data) > aws_chunk_size:
                hash_type = 'MD5 (Etag S3)'
                n_chunks = math.ceil(len(data) / aws_chunk_size)
                chunk_hashes = []
                for i in range(n_chunks):
                    chunk = data[i * aws_chunk_size:(i + 1) * aws_chunk_size]
                    chunk_hashes.append(hashlib.md5(chunk).digest())
                readable_hash = hashlib.md5(b''.join(chunk_hashes)).hexdigest() + f'-{n_chunks}'
            elif sha256:
                hash_type = 'SHA256'
                readable_hash = hashlib.sha256(data).hexdigest()
            else:
                hash_type = 'MD5' + ('' if plain_md5 else '(Etag S3)')
                readable_hash = hashlib.md5(data).hexdigest()
            hash_list.append(f'"{readable_hash}"')
    hashses = ', '.join(str(__hash__) for __hash__ in hash_list)
    typer.echo(
        f"Foram calculados os hashes {hash_type} de {len(hash_list)} arquivo(s): {hashses}")
    if not sha256:
        clipboard = Clipboard()
        clipboard.copy(f'select * from upload.pipeline p where orig_ic_hash in ({hashses});')
        typer.echo("Uma query SQL para acompanhar o(s) arquivo(s) na pipeline foi copiada para a área de transferência")
