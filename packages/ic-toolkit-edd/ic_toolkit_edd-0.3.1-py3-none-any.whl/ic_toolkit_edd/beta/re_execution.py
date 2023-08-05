import os.path
import requests
import time
from abc import ABC, abstractmethod
import json
from datetime import datetime, timedelta


class ReExecution(ABC):
    def __init__(self, filename: str, sleep_time: int = 30, user: str = 'ReExecution'):
        self.user = user
        self.filename = filename

        with open(os.path.join(os.getcwd(), 'pending', self.filename), 'r') as f:
            id_arquivos = list([line.strip() for line in f])

        self._parser_request(id_arquivos, sleep_time)

    @property
    @abstractmethod
    def get_etl_step(self) -> str:
        pass

    @property
    @abstractmethod
    def get_name_ids(self) -> str:
        pass

    @staticmethod
    def countdown(t: int):
        while t >= 0:
            print(f'Aguardando {t} segundos para enviar o proximo lote.    ', end='\r')
            time.sleep(1)
            t -= 1
        print('                                                    ', end='\r')

    def _parser_request(self, id_arquivos: list, sleep_time: int = 30):
        self.set_id_arquivos = set(id_arquivos)
        self.sleep_time = sleep_time
        # rescreve os arquivos pendentes tirando os ids repetidos
        with open(os.path.join(os.getcwd(), 'pending', self.filename), 'w') as f:
            f.write(str.join('\n', self.set_id_arquivos))

        self.enviados = []
        self.pending = self.set_id_arquivos.copy()

        if os.path.exists(os.path.join(os.getcwd(), 'finish', self.filename)):
            with open(os.path.join(os.getcwd(), 'finish', self.filename), 'r') as f:
                self.enviados = list([line.strip() for line in f])
                self.pending = self.set_id_arquivos.difference(self.enviados)
        # Measure time to finish:
        total_seconds = len(self.pending) * self.sleep_time
        m, s = divmod(total_seconds, 60)
        h, m = divmod(m, 60)

        currently_time = datetime.now()
        time_add = timedelta(hours=h, minutes=m, seconds=s)
        print(f'\n<> Há {len(self.enviados)} {self.get_name_ids} enviados de {len(self.set_id_arquivos)}')
        print(f'<> Previsão de hora: ' + (currently_time + time_add).strftime('%H:%M:%S'))

        h, m, s = list(
            map(
                lambda x: f'0{x}' if len(str(x)) == 1 else x, [h, m, s]
            )
        )

        print(f'<> Tempo estimado: {h}h {m}min {s}seg\n')

    def run(self, prioritario: bool = True, printar_ids: bool = False):
        try:
            c = 0

            len_ = len(self.set_id_arquivos)
            for idx, id_ in enumerate(self.set_id_arquivos):

                if id_ not in self.pending:
                    continue

                url = 'https://v8wcnj1p11.execute-api.us-east-1.amazonaws.com/Prod/'
                headers = {
                    'x-generator-key': 'GfkRdSHPM5rNBHgX2b4FVzuqDma7jhTT5utt7mY9kQ735pWekGp8jV6AayRSYF8q',
                    'Content-Type': 'application/json'
                }
                body = {
                    'endpoint': 'icdb-prod',
                    'input-type': 'multiple-id',
                    'input': [id_],
                    'etl-step': self.get_etl_step,
                    'usuario': f'ReExecution - {self.user}'
                }

                if prioritario:
                    body['prioridade'] = 'true'  # Só fará efeito em caso de DCM | DPGuias

                body = json.dumps(body)

                requests.post(url, data=body, headers=headers)

                if printar_ids:
                    print(f'{id_} ({len(self.enviados) + 1}/{len_})')
                c += 1
                start = '' if len(self.enviados) == 0 else '\n'
                self.enviados.append(id_)

                with open(os.path.join(os.getcwd(), 'finish', self.filename), 'a') as f:
                    f.write(start + id_)

                self.countdown(self.sleep_time)
            print(f'{c} mensagens enviadas')

        except KeyboardInterrupt:
            print('Execução interrompida pelo usuario.')


class ReProcessar(ReExecution):
    def __init__(self, filename: str, sleep_time: int = 30, user: str = 'ReExecution'):
        super().__init__(filename, sleep_time, user)

    @property
    def get_etl_step(self) -> str:
        return 'posprocessamento'

    @property
    def get_name_ids(self) -> str:
        return 'id_arquivos'


class ReLoad(ReExecution):
    def __init__(self, filename: str, sleep_time: int = 30, user: str = 'ReExecution'):
        super().__init__(filename, sleep_time, user)

    @property
    def get_etl_step(self) -> str:
        return 'load'

    @property
    def get_name_ids(self) -> str:
        return 'id_arquivo_padronizado'


class RePadronizar(ReExecution):
    def __init__(self, filename: str, sleep_time: int = 30, user: str = 'ReExecution'):
        super().__init__(filename, sleep_time, user)

    @property
    def get_etl_step(self) -> str:
        return 'padronizacao'

    @property
    def get_name_ids(self) -> str:
        return 'id_arquivo_parseado'


class ReParsear(ReExecution):
    def __init__(self, filename: str, sleep_time: int = 30, user: str = 'ReExecution'):
        super().__init__(filename, sleep_time, user)

    @property
    def get_etl_step(self) -> str:
        return 'parser'

    @property
    def get_name_ids(self) -> str:
        return 'id_arquivo_original'
