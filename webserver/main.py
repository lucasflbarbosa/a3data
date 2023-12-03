import uvicorn
import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from utils import common_essential_functions as response

from sources.resources.user import resources_user_login


__author__ = "Lucas Felix"
__date__ = "03/12/2023"
__version__ = open("version").readline()

logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger("uvicorn.error")
logger.propagate = False
# logger.setLevel(logging.INFO)
# flag que permite ativar/desativar log
logger.disabled = False if os.environ.get("LOG", "True") == "True" else True


description = """
### **Technical Challenge for Software Engineer - Backend Focus.**
__________________________________________________________
"""

paths_description = [
    {
        "name": 'Health',
        "description": "Retorno de verificação de status API."
    },
    {
        "name": '/api/resources/user',
        "description": "Grupo de Endpoints para o tratamento de Usuários."
    }
]

app = FastAPI(
    title="Technical Challenge a3data - APIs",
    description=description,
    version=__version__,
    openapi_tags=paths_description,
    docs_url="/documentation",
    redoc_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return_response, status_code = response.doReturn(
        "invalidArgumentException", [])
    return JSONResponse(status_code=status_code, content=return_response)


# Endpoints /resources/user
app.include_router(resources_user_login.router)


@app.get("/health", tags=['Health'])
def health():
    """
    Validação do estado de saúde da API.
    """
    response_return, status_code = response.doReturn("health", [])
    return JSONResponse(status_code=status_code, content=response_return)


if __name__ == "__main__":
    logging.info("Starting Webserver in PORT " + str(os.environ.get("SERVER_PORT", 8090)))
    uvicorn.run(
        "main:app",
        port=int(os.environ.get("SERVER_PORT", 8090)),
        log_level=os.environ.get("SERVER_LOG_LEVEL", "info"),
        reload=True
    )
