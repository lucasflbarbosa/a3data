import datetime
import pytz

__author__ = "Lucas Felix"
__date__ = "03/12/2023"

__version__ = open("version").readline()


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
