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


@router.delete('')
def resources_patient_delete(id: Optional[str] = Query(None,
                                                       title="Busca personalizada",
                                                       description="""Essa variável permite fazer uma busca
                                                                      personalizada através de um id no banco de dados e excluir."""),
                             user_token: str = Header(None)):

    logger.info("resources_patient_delete iniciada")
    logger.info("Validacao do JSON relizado com sucesso.")

    try:
        status: str = "success"
        data: list[dict] = []

        cnx = Connection().connect()
        cursor = cnx.cursor()

        user_auth = Token(conn=cnx, token=user_token)
        user_auth.validation()

        logger.info("Token validado com sucesso.")

        query = f"""SELECT TRUE
                    FROM public."patient"
                    WHERE id = '{id}'"""

        cursor.execute(query)
        result = cursor.fetchone()

        if result is None:
            raise ValueError("noFind")

        query = f"""DELETE FROM public."patient"
                    WHERE id = '{id}'
                    RETURNING TRUE"""

        cursor.execute(query)
        result = cursor.fetchone()

        if result is None:
            raise psycopg2.DatabaseError("Erro na exclusao do paciente na tabela de pacientes!")

        cnx.commit()

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
