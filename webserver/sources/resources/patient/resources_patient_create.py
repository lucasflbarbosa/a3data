import os
import logging
import psycopg2
from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
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


class PatientCreate(BaseModel):
    id: str
    birthplace: str
    ssn: str
    first_name: str
    last_name: str


@router.post('')
def resources_patient_create(user: PatientCreate, user_token: str = Header(None)):

    logger.info("resources_patient_create iniciada")
    logger.info("Validacao do JSON relizado com sucesso.")

    try:
        status: str = "created"
        data: list[dict] = []

        cnx = Connection().connect()
        cursor = cnx.cursor()

        user_auth = Token(conn=cnx, token=user_token)
        user_auth.validation()

        logger.info("Token validado com sucesso.")

        query = f"""SELECT TRUE
                    FROM public."patient"
                    WHERE id = '{user.id}'"""

        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            raise ValueError("duplicatedElement")

        query = f"""INSERT INTO public."patient"
                    (id, birthplace, ssn, first_name, last_name)
                    VALUES('{user.id}', '{user.birthplace}', '{user.ssn}', '{user.first_name}', '{user.last_name}')
                    RETURNING id"""

        cursor.execute(query)
        result = cursor.fetchone()

        if result is None:
            raise psycopg2.DatabaseError("Erro na insercao do paciente na tabela de pacientes!")

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
