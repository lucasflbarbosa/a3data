import os
import logging
import psycopg2
from fastapi import APIRouter
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


router = APIRouter(prefix='/api/resources/user/login',
                   tags=['/api/resources/user'])


class UserListLogin(BaseModel):
    id: int
    name: str
    email: str


class UserLogin(BaseModel):
    email: str
    password: str


@router.post('')
def resources_user_login(request: UserLogin):

    logger.info("resources_user_login iniciada")
    logger.info("Validacao do JSON relizado com sucesso.")

    try:
        status: str = "success"
        data: list[dict] = []

        cnx = Connection().connect()
        cursor = cnx.cursor()

        secret_key = os.environ["SECRET"]

        query = f"""SELECT  id,
                            name,
                            email,
                            pgp_sym_decrypt(password::bytea, '{secret_key}')
                    FROM public."user"
                    WHERE email = '{request.email}' """

        cursor.execute(query)
        result = cursor.fetchone()

        if result is None:
            raise ValueError("noFind")
        else:
            if result[3] == request.password:
                user_data = UserListLogin(id=result[0],
                                          name=result[1],
                                          email=result[2])
            else:
                raise ValueError("noFind")

            user = {
                "id": user_data.id,
                "name": user_data.name,
                "email": user_data.email
            }

            user_auth = Token(conn=cnx, id_user=user_data.id)
            user_auth.get_token_by_id()
            if user_auth.token:
                user_auth.validation()
            else:
                user_auth.authentication()

            data.append({
                        "user": user,
                        "token": user_auth.token
                        })

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
