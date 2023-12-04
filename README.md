# DESAFIO TÉCNICO A3DATA - APIs
____________________________________________________________
> Status do Projeto: Concluido :white_check_mark:
____________________________________________________________

## 1. Requisitos

Docker >= 24.0.5  
Docker Compose >= v2.20.2  

<br>

## 2. Docker-compose

<p align="justify"><b>Esses são os passos para executar o docker-compose no linux. </p></b>

```bash
export PATH_TO_DATABASE="coloque aqui o diretório" && export VERSION_DATABASE=$(cat database/version) && export VERSION_WEBSERVER=$(cat webserver/version) && docker-compose up -d  
```

ou use o comando abaixo para persistir o banco na pasta do projeto:  

```bash
export PATH_TO_DATABASE=$(pwd) && export VERSION_DATABASE=$(cat database/version) && export VERSION_WEBSERVER=$(cat webserver/version) && docker compose up -d  
```

<p align="justify"><b>Esses são os passos para executar o docker-compose no windows com powershell. </p></b>

```shell
set PATH_TO_DATABASE="coloque aqui o diretório" && set VERSION_DATABASE=$(cat database/version) && set VERSION_WEBSERVER=$(cat webserver/version) && docker-compose up -d  
```

ou use o comando abaixo para persistir o banco na pasta do projeto:  

```shell
set PATH_TO_DATABASE=$(pwd) && set VERSION_DATABASE=$(cat database/version) && set VERSION_WEBSERVER=$(cat webserver/version) && docker compose up -d  
```

<b>1. Conferir variáveis de ambiente na seção 3.</b>  
<b>2. Sempre lembrar de especificar as variáveis de ambiente.</b>

<br>

## 3. Variáveis de Ambiente

<p align="justify"> Essas são as variavéis de ambiente que devem existir no container ou SO na hora em que estiver executando. </p>

- PATH_TO_DATABASE: inserir aqui o caminho até a pasta que vai conter a persistência dos dados do container do banco de dados.
- VERSION_DATABASE: aqui está o comando que pega a versão mais atual do banco de dados, e cria a imagem baseada na versão mais atual.
- VERSION_WEBSERVER: aqui está o comando que pega a versão mais atual do webserver, e cria a imagem baseada na versão mais atual.

<br>

## 4. Estrutura das pastas do projeto

- /webserver: contém o repositório do webserver como submódulo. (Python 3.10 + FastApi)
  - /auth: código relacionado a autenticação e validação de usuários.
  - /conn: submódulo que faz comunicação e acesso ao banco de dados.
  - /sources: contém as relações de conjuntos de endpoints.
    - /sources/integrations: todos endpoints que se comunicam com endpoints ou serviços externos.
    - /sources/resources: todos endpoints que proveem dados para o front-end e manipulação direta.
    - /sources/servers: todos endpoints que se comunicam internamente com serviços em background.
  - /utils: contém código que são comuns a todos endpoints, como mensagens de retorno.
  - main.py: código que executa o servidor e define a rota dos endpoints.
  - requirements.txt: lista de bibliotecas e frameworks necessários para execução do projeto.
  - Dockerfile: arquivo dockerfile referente ao container webserver.
  - webserver.conf: arquivo com as variáveis de ambiente referente a execução do webserver.
  - version: arquivo que contém a versão atual do projeto. Ele é definido da seguinte maneira:
    -  X . Y . Z  -> COMPATIBILIDADE . FEATURE . BUG

- /database: contém os arquivos de configuração do banco de dados. (Postgresql 13)
  - /deploy: contém os arquivos sql conforme as atualizações do banco de dados, no formato dia-mês-ano, sem os '-'.
  - /diff: contém as diferenças entre as versões, sempre da última utilizada para a nova versão em uso.
  - /modeling: contém os arquivos para modelagem no pgmodeler e as imagens das versões.
    - {VERSÃO}.sql: arquivo de configuração do banco de dados, sempre usar a versão mais atual.
  - database.conf: arquivo com as variáveis de ambiente referente a execução do banco de dados.
  - version: versão do banco de dados mais atual, sempre no formato dia-mês-ano. Ex: 25032022.  
- docker-compose.yml: arquivo docker-compose que faz o gerenciamento de todos containers (webserver, database, elasticsearch).
- version: arquivo que contém a versão atual do projeto. Ele é definido da seguinte maneira:
  -  X . Y . Z  -> COMPATIBILIDADE . FEATURE . BUG

<br>

## 5. Manipulando os endpoints e Funcionalidades

- O desafio técnico implementou todas espeficiações, incluindo o elasticsearch;
- Existem 3 containers (database, elasticsearch, webserver)
- Após subir os containers é possível acessar e manipular os endpoints (Swagger) através do browser no endereço: (http://localhost:8090/documentation)
- O usuário para poder manipular os endpoints é:
  - Login: admin@email.com
  - Senha: 123456
- Para manipular os endpoints com excessão do login, é necessário copiar o token e inserir no cabeçalho do endpoint no próprio Swagger.
- O endpoint /api/resources/patient/search faz uma busca com elasticsearch em uma base de dados synthea.
- Através da consulta anterior é possível visualizar os dados, e com esses dados é possível inserir no nosso banco de dados através do CRUD em /patient.
