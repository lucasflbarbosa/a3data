import os
import logging
import psycopg2
from fastapi import APIRouter, Header, Query
from fastapi.responses import JSONResponse
from typing import Optional
from utils import common_essential_functions as response
from conn.conn import Connection
from auth.token_authentication import Token

__author__ = "Lucas Felix"
__date__ = "03/12/2023"

logger = logging.getLogger()
logger.setLevel(logging.INFO)
# flag que permite ativar/desativar log
logger.disabled = False if os.environ.get("LOG", "True") == "True" else True


router = APIRouter(prefix='/api/resources/patient',
                   tags=['/api/resources/patient'])


@router.get('')
def resources_patient_list(id: Optional[str] = Query(None,
                                                     title="Busca personalizada",
                                                     description="""Essa variável permite fazer uma busca
                                                                    personalizada através de um id no banco de dados."""),
                           user_token: str = Header(None)):

    logger.info("resources_patient_list iniciada")
    logger.info("Validacao do JSON relizado com sucesso.")

    try:
        status: str = "success"
        data: list[dict] = []

        cnx = Connection().connect()
        cursor = cnx.cursor()

        user_auth = Token(conn=cnx, token=user_token)
        user_auth.validation()

        logger.info("Token validado com sucesso.")

        sub_query = ""
        if id:
            sub_query = f"WHERE id = '{id}'"

        query = f"""SELECT id, birthplace, ssn, first_name, last_name
                    FROM public."patient" {sub_query}"""

        cursor.execute(query)
        result = cursor.fetchall()

        if result is None:
            raise psycopg2.DatabaseError("Erro na busca do paciente na tabela de pacientes!")

        for patient in result:
            data.append({
                "id": patient[0],
                "birthplace": patient[1],
                "ssn": patient[2],
                "first_name": patient[3],
                "last_name": patient[4]
            })

    except KeyError as ex:
        logger.error("KeyError " + str(ex))
        status = "keyError"
    except psycopg2.IntegrityError as ex:
        logger.error("validationError " + str(ex))
        status = "validationError"
    except (psycopg2.DataError, psycopg2.InternalError,
            psycopg2.ProgrammingError) as ex:
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
