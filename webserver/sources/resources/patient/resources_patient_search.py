import os
import logging
import psycopg2
from fastapi import APIRouter, Header, Query
from fastapi.responses import JSONResponse
from typing import Optional
from utils import common_essential_functions as response
from conn.conn import Connection
from auth.token_authentication import Token
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ElasticsearchException

__author__ = "Lucas Felix"
__date__ = "03/12/2023"

logger = logging.getLogger('elasticsearch')
logger.setLevel(logging.INFO)
# flag que permite ativar/desativar log
logger.disabled = False if os.environ.get("LOG", "True") == "True" else True


router = APIRouter(prefix='/api/resources/patient/search',
                   tags=['/api/resources/patient'])


@router.get('')
def resources_patient_search(search: Optional[str] = Query(None,
                                                           title="Busca personalizada",
                                                           description="""Essa variável permite fazer uma busca
                                                                          personalizada através de um string em
                                                                          uma base de dados Synthea."""),
                             user_token: str = Header(None)):

    logger.info("resources_patient_search iniciada")
    logger.info("Validacao do JSON relizado com sucesso.")

    try:
        status: str = "success"
        data: list[dict] = []

        cnx = Connection().connect()

        user_auth = Token(conn=cnx, token=user_token)
        user_auth.validation()

        logger.info("Token validado com sucesso.")

        es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])

        try:
            if es.ping():
                print("Conexão bem-sucedida!")
            else:
                print("Não foi possível estabelecer a conexão.")
        except ElasticsearchException as e:
            print(f"Erro de conexão: {e}")
            raise Exception()

        consulta = {
            "query": {
                "bool": {
                    "should": [
                        {"wildcard": {"Id": f"*{search}*"}},
                        {"wildcard": {"SSN": f"*{search}*"}},
                        {"wildcard": {"DRIVERS": f"*{search}*"}},
                        {"wildcard": {"PASSPORT": f"*{search}*"}},
                        {"wildcard": {"PREFIX": f"*{search}*"}},
                        {"wildcard": {"FIRST": f"*{search}*"}},
                        {"wildcard": {"LAST": f"*{search}*"}},
                        {"wildcard": {"SUFFIX": f"*{search}*"}},
                        {"wildcard": {"MAIDEN": f"*{search}*"}},
                        {"wildcard": {"MARITAL": f"*{search}*"}},
                        {"wildcard": {"RACE": f"*{search}*"}},
                        {"wildcard": {"ETHNICITY": f"*{search}*"}},
                        {"wildcard": {"GENDER": f"*{search}*"}},
                        {"wildcard": {"BIRTHPLACE": f"*{search}*"}},
                        {"wildcard": {"ADDRESS": f"*{search}*"}},
                        {"wildcard": {"CITY": f"*{search}*"}},
                        {"wildcard": {"STATE": f"*{search}*"}},
                        {"wildcard": {"COUNTRY": f"*{search}*"}},
                        {"wildcard": {"FIPS": f"*{search}*"}},
                        {"wildcard": {"ZIP": f"*{search}*"}},
                        {"wildcard": {"LAT": f"*{search}*"}},
                        {"wildcard": {"LON": f"*{search}*"}},
                        {"wildcard": {"HEALTHCARE_EXPENSES": f"*{search}*"}},
                        {"wildcard": {"HEALTHCARE_COVERAGE": f"*{search}*"}},
                        {"wildcard": {"INCOME": f"*{search}*"}}
                    ]
                }
            }
        }
        data = []
        resultados = es.search(index='patients_csv', body=consulta)
        for resultado in resultados['hits']['hits']:
            data.append(resultado['_source'])

    except KeyError as ex:
        logger.error("KeyError " + str(ex))
        status = "keyError"
    except psycopg2.IntegrityError as ex:
        logger.error("duplicatedElement " + str(ex))
        status = "duplicatedElement"
    except (psycopg2.DataError, psycopg2.IntegrityError,
            psycopg2.InternalError, psycopg2.ProgrammingError) as ex:
        logger.info("DataError " + str(ex))
        status = "dataError"
    except psycopg2.DatabaseError as ex:
        logger.error("DatabaseError " + str(ex))
        status = "databaseError"
    except PermissionError as ex:
        logger.error(ex)
        status = "noAccess"
    except ValueError as ex:
        logger.error(ex)
        status = str(ex)
    except Exception as ex:
        logger.error(ex)
        status = "default"
    finally:
        try:
            cnx.close()
        except Exception:
            pass
        finally:
            response_return, status_code = response.doReturn(status, data)
            return JSONResponse(status_code=status_code, content=response_return)
