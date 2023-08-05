import json
import os
from pathlib import Path

import requests
import typer

from ic_toolkit_edd.abstract.s3_utils import S3Object
from ic_toolkit_edd.abstract.utilities import PdfStrippers


def cvtpdf_handler(input_path: Path, stripper: PdfStrippers, output_path: Path):
    if not os.path.isfile(input_path):
        pdf_names = [
            os.path.basename(f) for f in os.listdir(input_path) if
            os.path.isfile(os.path.join(input_path, f)) and f.lower().endswith('.pdf')
        ]
    elif input_path.name.lower().endswith('.pdf'):
        pdf_names = [os.path.basename(input_path)]
        input_path = os.path.dirname(input_path)
    else:
        pdf_names = []
    if len(pdf_names) == 0:
        typer.echo(" " + typer.style("ERRO: NENHUM PDF ENCONTRADO", typer.colors.WHITE, typer.colors.RED))
        typer.echo(f'\nCaminho de entrada: "{input_path}"')
        return
    s3_bucket = 'ic-teste'
    s3_prefix = 'temp/'
    request_url = "https://api-transform.intuitivecare.com/prod/transform/pdf2txt/v2"
    request_payload = {
        "input": [
            {
                "filename": '',
                "prefix": s3_prefix,
                "bucket": s3_bucket,
                "options": {
                    "stripper": stripper.value
                }
            }
        ],
        "output": {
            "bucket": "ic-transient",
            "prefix": "txt2csv/"
        }
    }
    with typer.progressbar(range(len(pdf_names)), length=len(pdf_names)) as progress:
        for i in progress:
            pdf_path = os.path.join(input_path, pdf_names[i])
            try:
                pdf_object = S3Object.upload_file(pdf_path, s3_bucket, s3_prefix, pdf_names[i], override_object=False)
            except FileExistsError:
                pdf_object = S3Object(s3_bucket, s3_prefix, pdf_names[i])
            request_payload['input'][0]['filename'] = pdf_object.filename
            request_body = json.dumps(request_payload, indent=2).encode('utf-8')
            try:
                response = requests.post(request_url, data=request_body)
                if not response.ok:
                    typer.echo(" " + typer.style("ERRO AO ENVIAR REQUISIÇÃO PARA O CONVERSOR",
                                                 typer.colors.WHITE, typer.colors.RED))
                    typer.echo(f"\n{response.status_code} - {response.json()['message']}")
                    return
                response_data = response.json()
                txt_object = S3Object(response_data['response'][0]["Bucket"], response_data['response'][0]["Prefix"],
                                      response_data['response'][0]["Filename"])
                txt_object.download(str(output_path))
                # Escrevendo informações do objeto dos TXT em um arquivo temporário
                txt_info = str(txt_object)
                with open(os.path.join(output_path, f"{os.path.splitext(txt_object.filename)[0]}_caminho.txt"),
                          'w') as info_file:
                    info_file.write(txt_info)
            except Exception as e:
                typer.echo("\n\n" + typer.style('ERRO', typer.colors.WHITE, typer.colors.RED))
                typer.echo(f'Exceção encontrada durante a conversão do PDF "{pdf_names[i]}": {e}')
                return
    typer.echo(typer.style(" SUCESSO", fg=typer.colors.GREEN, bold=True))
    typer.echo(
        f'\nForam convertidos {len(pdf_names)} arquivos! Os TXTs e caminhos para os objetos na S3 foram salvos no diretório "{output_path}"')
