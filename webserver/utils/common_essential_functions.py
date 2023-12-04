import os
import datetime
import pytz
import logging
import pandas as pd
from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import ElasticsearchException
from elasticsearch.helpers.errors import BulkIndexError

__author__ = "Lucas Felix"
__date__ = "03/12/2023"
__version__ = open("version").readline()


logger = logging.getLogger('elasticsearch')
logger.setLevel(logging.INFO)
# flag que permite ativar/desativar log
logger.disabled = False if os.environ.get("LOG", "True") == "True" else True


def create_indexes_elasticsearch(index_name: str, path_csv: str):
    es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])

    try:
        if es.ping():
            logger.info("Conexão bem-sucedida!")
        else:
            logger.info("Não foi possível estabelecer a conexão.")
    except ElasticsearchException as e:
        logger.info(f"Erro de conexão: {e}")

    if not es.indices.exists(index=index_name):

        df = pd.read_csv(path_csv)

        # Substituir valores 'nan' por undefined no DataFrame
        df = df.where(pd.notna(df), "undefined")

        # Converter todas as colunas para o tipo str
        df = df.astype(str)

        data_to_index = df.to_dict(orient='records')

        actions = [
                {
                    "_op_type": "index",  # Operação de indexação
                    "_index": index_name,
                    "_source": data
                }
                for data in data_to_index
            ]

        # Usar a função helpers.bulk para indexar em lote
        try:
            helpers.bulk(es, actions)
        except BulkIndexError as e:
            for erro in e.errors:
                logger.info(f"Erro no documento: {erro}")

        logger.info(f"Index {index_name} criado!")
    else:
        logger.info(f"Index {index_name} ja existe!")


def get_timestamp():
    return (datetime.datetime.now(pytz.timezone("America/Recife"))).strftime("%d-%m-%Y - %H:%M:%S")


returns = {
    # Teste de API executando
    "health": {"message": "Healthy...", "code": 200},
    # ------------------------------------------------------------------------------------------------------------------
    # Respostas Comuns
    # -> Banco de dados
    "noData": {"message": "Nenhum elemento encontrado!", "code": 200},
    "notModified": {"message": "Nenhuma modificação!", "code": 304},
    "noFind": {"message": "Nenhum elemento encontrado!", "code": 404},
    "integrityError": {"message": "Erro de integridade no banco!", "code": 409},
    "duplicatedElement": {"message": "Elemento já cadastrado no sistema!", "code": 409},
    "dataError": {"message": "Falha na persistência da informação!", "code": 500},
    "internalError": {"message": "Erro interno no banco de dados!", "code": 500},
    "databaseError": {"message": "Falha na comunicação com o serviço de armazenamento!", "code": 500},
    # -------------------------------------
    "success": {"message": "Função executada com sucesso!", "code": 200},
    "created": {"message": "Elemento criado!", "code": 201},
    "noContent": {"message": "Nenhum conteúdo encontrado!", "code": 204},
    "keyError": {"message": "Não foi possível obter valores na requisição!", "code": 400},
    "validationError": {"message": "Validação falhou para dados recebidos!", "code": 400},
    "noAccess": {"message": "Sem permissão para essa função!", "code": 401},
    "invalidArgumentException": {"message": "Argumentos inválidos para requisição!", "code": 422},
    "default": {"message": "Erro interno do serviço!", "code": 500},
    # ------------------------------------------------------------------------------------------------------------------
}


def doReturn(situation, data=[]):
    situation = "default" if not (situation in returns.keys()) else situation
    return {
        "results": {
                "message": returns[situation]["message"],
                "data": data,
                "metaInfo": {
                    "timestamp": get_timestamp(),
                    "apiVersion": __version__
                }
        },
        "statusCode": returns[situation]["code"]
    }, returns[situation]["code"]
