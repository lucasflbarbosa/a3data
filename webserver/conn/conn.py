import logging
import psycopg2
import os

"""
Script responsavel por criar conexão com banco de dados a partir de variaveis de ambiente
"""
__author__ = "Lucas Felix"
__date__ = "03/12/2023"
__version__ = open("version").readline()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# flag que permite ativar/desativar log
try:
    logger.disabled = False if (os.environ["LOG"] == "True") else True
except Exception:
    logger.disabled = True


class Connection:
    def __init__(self):
        self.secret = None

    def connect(self):
        logging.info("Realizando leitura de variavies de ambiente")
        try:
            json_result = {
                "endpoint": os.environ["DATABASE_HOST"],
                "user": os.environ["DATABASE_USER"],
                "password": os.environ["DATABASE_PASSWORD"],
                "name": os.environ["DATABASE_NAME"],
                "port": os.environ["DATABASE_PORT"],
            }
            logging.info("Credenciais do SGBD encontradas")
        except Exception as ex:
            logger.error(f"Erro ao tentar acessar variavel de ambiente. Erro: {ex}")

        logging.info("Realizando conexao com PostgreSQL")
        try:
            conn = psycopg2.connect(
                    host=json_result["endpoint"],
                    user=json_result["user"],
                    password=json_result["password"],
                    dbname=json_result["name"],
                    port=json_result["port"],
                )
            cursor = conn.cursor()
            cursor.execute("""SET timezone TO 'America/Recife';
                              SET datestyle TO "ISO, DMY";""")
            return conn
        except Exception as ex:
            logger.error(f"Erro ao tentar realizar conexao com SGBD. Erro: {ex}")
