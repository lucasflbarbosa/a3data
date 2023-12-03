import uuid
import logging
import os

"""
Componente que faz processo de validação de Token.
"""

__author__ = "Lucas Felix"
__date__ = "03/12/2023"

logger = logging.getLogger()
logger.setLevel(logging.INFO)
# flag que permite ativar/desativar log
logger.disabled = False if os.environ.get("LOG", "False") == "True" else True


class Token:
    def __init__(self, conn, id_user=None, token=None, identifier_profile=None):
        self.__connection = conn
        self.__validation = None
        self.token = token
        self.id_user = id_user
        self.identifier_profile = identifier_profile
        logger.info("Elemento token iniciado...")

    def authentication(self):
        logger.info("Realizando processo de autenticacao...")
        cursor = self.__connection.cursor()
        token = uuid.uuid4().hex

        qry = f"""
            INSERT INTO public."session"
            (token, expiration, id_user)
            VALUES('{token}', (now() + INTERVAL '01:00:00'), {self.id_user})
            ON CONFLICT (id_user) DO UPDATE SET expiration = (now() + INTERVAL '01:00:00'), "token" = '{token}';
            """
        cursor.execute(qry)
        self.__connection.commit()
        self.token = token
        self.__validation = True
        logger.info("Autenticacao finalizada.")

    def validation(self):
        logger.info("Realizando processo de validacao para token...")

        if self.token is None or self.token == "":
            raise PermissionError("Token nao existe!")

        cursor = self.__connection.cursor()
        qry = f"""
            UPDATE public."session"
            SET expiration = (now() + INTERVAL '01:00:00')
            WHERE "token" = '{self.token}' and expiration > now()
            RETURNING "token", id_user, (SELECT identifier_profile
                                         FROM public."user"
                                         WHERE id = id_user) """
        cursor.execute(qry)
        result = cursor.fetchone()

        if result is None:
            raise PermissionError("Token invalido!")
        else:
            self.token = result[0]
            self.id_user = result[1]
            self.identifier_profile = result[2]

            if self.token is None or self.id_user is None:
                raise PermissionError("Sessao nao encontrada")

            self.__connection.commit()

    def get_token_by_id(self):
        logger.info("Buscando token valido para usuario...")

        cursor = self.__connection.cursor()

        qry = f"""
            SELECT token
            FROM public."session"
            WHERE id_user = {self.id_user} AND expiration > now()"""

        cursor.execute(qry)
        result = cursor.fetchone()

        if result:
            self.token = result[0]
        else:
            self.token = None
