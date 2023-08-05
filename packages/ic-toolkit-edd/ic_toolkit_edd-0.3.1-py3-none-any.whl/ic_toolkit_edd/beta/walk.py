import json
from typing import List

import pandas as pd

from ic_toolkit_edd.abstract.database import get_dataframe
from ic_toolkit_edd.beta.input_type import InputType, PipelineType, input_pipeline


class WalkException(Exception):
    pass


input_query = {
    InputType.ic_hash: '''
        select
            ao.id_arquivo_original as `id_this`,
            ap.id_arquivo_parseado as `id_next`
        from upload.arquivo_original ao
            inner join upload.arquivo_original ao2
                on ao2.ic_hash = ao.ic_hash and ao2.duplicata = 0
            left join upload.arquivo_parseado ap
                on ap.id_arquivo_original = ao2.id_arquivo_original
        where
            ao.ic_hash in %(input_list)s
        ;
    ''',
    InputType.id_arquivo_original: '''
        select
            ao.id_arquivo_original as `id_this`,
            ap.id_arquivo_parseado as `id_next`
        from upload.arquivo_original ao
            inner join upload.arquivo_original ao2
                on ao2.ic_hash = ao.ic_hash and ao2.duplicata = 0
            left join upload.arquivo_parseado ap
                on ap.id_arquivo_original = ao2.id_arquivo_original
        where
            ao.id_arquivo_original in %(input_list)s
        ;
    ''',
    InputType.id_arquivo_parseado: '''
        select
            ap2.id_arquivo_parseado as `id_this`,
            ap3.id_arquivo_padronizado as `id_next`
        from upload.arquivo_parseado ap
            inner join upload.arquivo_parseado ap2
                on ap2.ic_hash = ap.ic_hash and ap2.duplicata = 0
            left join upload.arquivo_padronizado ap3
                on ap3.id_arquivo_parseado = ap2.id_arquivo_parseado
        where
            ap.id_arquivo_parseado in %(input_list)s
        ;
    ''',
    InputType.id_arquivo_padronizado: '''
        select
            ap2.id_arquivo_padronizado as `id_this`,
            a.id_arquivo as `id_next`
        from upload.arquivo_padronizado ap
            inner join upload.arquivo_padronizado ap2
                on (ap2.ic_hash = ap.ic_hash or ap2.ic_hash_2 = ap.ic_hash_2) and ap2.duplicata = 0
            left join intuitive.arquivos a
                on a.id_arquivo_padronizado = ap2.id_arquivo_padronizado
        where
            ap.id_arquivo_padronizado in %(input_list)s
        ;
    '''
}

pipeline = {
    InputType.ic_hash: (InputType.id_arquivo_original, InputType.id_arquivo_parseado),
    InputType.id_arquivo_original: (InputType.id_arquivo_original, InputType.id_arquivo_parseado),
    InputType.id_arquivo_parseado: (InputType.id_arquivo_parseado, InputType.id_arquivo_padronizado),
    InputType.id_arquivo_padronizado: (InputType.id_arquivo_padronizado, InputType.id_arquivo),
}


def get_df(input_type: InputType, input_list: List):
    if input_list.__len__() > 0:
        return get_dataframe(
            query=input_query[input_type],
            args={'input_list': input_list}
        )
    else:
        return pd.DataFrame(columns=['id_this', 'id_next'])


def walk_by(input_type: InputType, output_type: PipelineType, input_list: List):
    this_type, next_type = pipeline[input_type]

    df = get_df(input_type, input_list)

    record = {
        'this_type': this_type,
        'next_type': next_type,
        'this_stopped_list': [
            int(x) for x in df[df['id_next'].isna()]['id_this'].tolist()
        ],
        'this_passed_list': [
            int(x) for x in df[df['id_next'].notna()]['id_this'].tolist()
        ],
        'next_input_list': [
            int(x) for x in df[df['id_next'].notna()]['id_next'].tolist()
        ],
    }

    if input_pipeline[this_type] == output_type:
        record['output_type'] = this_type
        record['output_list'] = record['this_passed_list']
        return [record]

    if input_pipeline[next_type] == output_type and PipelineType.arquivo == output_type:
        record['output_type'] = next_type
        record['output_list'] = record['next_input_list']
        return [record]

    history = [record]
    result_history = walk_by(next_type, output_type, record['next_input_list'])
    history.extend(result_history)
    return history


def run():
    input_list = [
        140225356
    ]

    history = walk_by(InputType.id_arquivo_parseado, PipelineType.arquivo, input_list)

    print(json.dumps(history, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    run()
