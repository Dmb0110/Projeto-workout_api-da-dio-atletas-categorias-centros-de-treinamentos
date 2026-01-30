# workout_api

API REST em FastAPI para gerenciar atletas, categorias e centros de treinamento. Projeto usa SQLAlchemy (async) + Alembic para migrações e PostgreSQL em Docker.

## Stack
- Python 3.11+ (recomendado)
- FastAPI
- SQLAlchemy (async)
- asyncpg
- Alembic
- Uvicorn
- PostgreSQL (via docker-compose)

Versões das dependências principais: veja `requirements.txt`.

## Recursos
- CRUD de Atletas, Categorias e Centros de Treinamento
- Pydantic schemas para validação
- Conexão assíncrona com DB (AsyncSession)
- Migrações com Alembic

## Estrutura principal
- `workout_api/main.py` — FastAPI app / ponto de entrada
- `workout_api/routers.py` — agregador de routers
- `workout_api/configs/` — settings e conexão com DB
- `workout_api/contrib/models.py` — Base dos modelos (metadata)
- `workout_api/atleta/`, `workout_api/categorias/`, `workout_api/centro_treinamento/` — domain modules
- `workout_api/alembic/` — migrações

## Quickstart (Windows PowerShell)

1. Subir PostgreSQL (docker-compose)
```powershell
docker-compose up -d
```

2. Criar e ativar virtualenv
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instalar dependências
```powershell
pip install -r workout_api/requirements.txt
```

4. Definir variáveis de ambiente (ex.: criar `.env` na raiz)  
Exemplo `.env`:
```
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/workout_db
# outras vars: SECRET_KEY, etc. (se houver)
```
Obs.: o projeto usa `settings.DB_URL` — confirme o nome da variável esperado em `workout_api/configs/settings.py`.

5. Aplicar migrações
```powershell
python -m alembic upgrade head
```

6. Rodar a aplicação
```powershell
uvicorn workout_api.main:app --reload --host 0.0.0.0 --port 8000
```

7. Acessar docs interativos
- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
------------------------------------

## Rotas da API

## atleta
GET /atleta/ Consultar todos os atletas

POST /atleta/ Criar um novo atleta

GET /atleta/{id} Consultar um Atleta pelo id

PATCH /atleta/{id} Editar um Atleta pelo id

DELETE /atleta/{id} Deletar um Atleta pelo id

## categoria
GET /categoria/ Consultar todas as categorias

POST /categoria/ Criar uma nova Categoria

GET /categoria/{id} Consultar uma Categoria pelo id

PATCH /categoria/{id} Editar um Atleta pelo id

DELETE /categoria/{id}

## centro_treinamento
GET /centro_treinamento/ Consultar todas os centros de treinamento

POST /centro_treinamento/ Criar um novo Centro de Treinamento

GET /centro_treinamento/{id} Consultar um Centro de Treinamento pelo id

PATCH /centro_treinamento/{id} Editar um CentroTreinamento pelo id

DELETE /centro_treinamento/{id} Deletar um Centro_treinamento pelo id

### Atletas

GET /atleta
Lista todos os atletas cadastrados.

Exemplo de requisiçao:
```json
[
  {
    "id": "128f3418-d841-4b7d-a98d-19d12c243025",
    "created_at": "2025-10-22T16:51:44.659008",
    "nome": "Pedro",
    "cpf": "99045678900",
    "idade": 20,
    "peso": 62.5,
    "altura": 1.67,
    "sexo": "M",
    "categoria": { "nome": "iniciante" },
    "centro_treinamento": { "nome": "CT king" }
  }
]

---------------------------
POST /atleta
Cria um novo atleta.

Exemplo de requisição:

{
  "nome": "Joao",
  "cpf": "12345678900",
  "idade": 25,
  "peso": 75.5,
  "altura": 1.7,
  "sexo": "M",
  "categoria": {
    "nome": "Scale"
  },
  "centro_treinamento": {
    "nome": "CT king"
  }
}
---
Exemplo de resposta:
{
  "id": "string",
  "created_at": "2026-01-30T16:23:32.680Z",
  "nome": "Joao",
  "cpf": "12345678900",
  "idade": 25,
  "peso": 75.5,
  "altura": 1.7,
  "sexo": "M",
  "categoria": {
    "nome": "Scale"
  },
  "centro_treinamento": {
    "nome": "CT king"
  }
}

----------------------------
GET /atleta/{id}
Retorna os dados de um atleta específico pelo seu id.

Exemplo de resposta:

{
  "id": "string",
  "created_at": "2026-01-29T22:45:43.993Z",
  "nome": "Joao",
  "cpf": "12345678900",
  "idade": 25,
  "peso": 75.5,
  "altura": 1.7,
  "sexo": "M",
  "categoria": {
    "nome": "Scale"
  },
  "centro_treinamento": {
    "nome": "CT king"
  }
}

------------------------------
PATCH /atleta/{id}
Atualiza parcialmente os dados de um atleta.

Exemplo de requisição:

{
  "nome": "Joao",
  "idade": 25,
  "peso": 75.5
}
---
Exemplo de resposta:

{
  "id": "string",
  "created_at": "2026-01-30T16:33:38.335Z",
  "nome": "Joao",
  "cpf": "12345678900",
  "idade": 25,
  "peso": 75.5,
  "altura": 1.7,
  "sexo": "M",
  "categoria": {
    "nome": "Scale"
  },
  "centro_treinamento": {
    "nome": "CT king"
  }
}

------------------------------
DELETE /atleta/{id}
Remove um atleta do sistema.

Exemplo de resposta:

{
  "message": "Atleta deletado com sucesso"
}

-------------------------------------
### Categoria

GET /atleta
Lista todos os atletas cadastrados.

Exemplo de resposta:
[
  {
    "nome": "anônimo",
    "id": "string"
  }
]

------------------------------------
POST /categoria
Cria uma nova categoria.

Exemplo de requisição:
{
  "nome": "string"
}
---
Exemplo de resposta:

{
  "nome": "string",
  "id": "string"
}

-------------------------------------
GET /categoria/{id}
Consultar uma categoria pelo id

Exemplo de resposta:

{
  "nome": "Scale",
  "id": "string"
}

-------------------------------------
PATCH /categoria/{id}
Editar um Atleta pelo id

Exemplo de requisiçao:

{
  "nome": "CT king",
  "endereco": "Rua A, 123"
}
---
Exemplo de resposta:

{
  "nome": "Scale",
  "id": "string"
}

-------------------------------------
DELETE /categoria/{id}
Deletar uma categoria pelo id

Exemplo de resposta:
{
  "mensagem":"categoria deletada com sucesso"
}

-------------------------------------
### Centro treinamento

GET /centro_treinamento
Consultar todos os centros de treinamento.

Exemplo de resposta:
[
  {
    "nome": "Ct king",
    "endereco": "Rua x.002",
    "proprietario": "Marcos",
    "id": "string"
  }
]

-------------------------------------
POST /centro_treinamento
Criar um novo centro de treinamento

Exemplo de requisiçao:
{
  "nome": "Ct king",
  "endereco": "Rua x.002",
  "proprietario": "Marcos"
}
---
Exemplo de resposta:
{
  "nome": "Ct king",
  "endereco": "Rua x.002",
  "proprietario": "Marcos",
  "id": "string"
}

-------------------------------------
GET /centro_treinamento/{id}
Consultar um centro de treinamento pelo id

Exemplo de resposta:

{
  "nome": "Ct king",
  "endereco": "Rua x.002",
  "proprietario": "Marcos",
  "id": "string"
}

----------------------------------
PATCH /centro_treinamento/{id}
Editar um centro de treinamento pelo id

Exemplo de requisiçao:

{
  "nome": "Ct king",
  "endereco": "Rua x.002",
  "proprietario": "Marcos"
}
---
Exemplo de resposta:

{
  "nome": "Ct king",
  "endereco": "Rua x.002",
  "proprietario": "Marcos",
  "id": "string"
}

------------------------------------
DELETE /centro_treinamento/{id}

Exemplo de resposta:

{
  "mesagem":"centro de treinamento deletado com sucesso"
}

-------------------------------------

## Testes
Se houver testes:
```powershell
pytest -q
```

## Comandos úteis
- Criar migration (autogerada):
```powershell
python -m alembic revision --autogenerate -m "mensagem"
```
- Ver status dos containers Docker:
```powershell
docker ps
```

## Troubleshooting (problemas comuns)
- Erro de import/router: verifique se cada controller exporta `router` e se `main.py`/`routers.py` incluem os routers corretamente.
- Migrations vazias/falhas: confirme `target_metadata` em `alembic/env.py` aponta para `contrib.models.BaseModel.metadata`.
- Erro de conexão DB: confirme `DATABASE_URL`/`settings.DB_URL` e se o container Postgres está rodando.
- Uso de SQLAlchemy async: nos handlers use `async with session.begin():` e `await session.execute(...)`.

## Contribuição
- Abra issue descrevendo o problema ou a feature.
- Faça um fork / branch com nome `feat/<descrição>` ou `fix/<descrição>`.
- Inclua testes quando aplicável.

## Licença
Adicione aqui a licença do projeto (ex.: MIT) ou apague esta seção se não aplicável.

---
Arquivo `requirements.txt` contém versões testadas; use-as para reproduzir ambiente.

## Estrutura do projeto

workout_api/
│
├── main.py                 # Ponto de entrada da aplicação FastAPI
├── routers.py              # Agregador de todos os routers
│
├── configs/                # Configurações e conexão com DB
│   ├── settings.py         # Variáveis de ambiente e configs
│   └── database.py         # Conexão assíncrona com PostgreSQL
│
├── contrib/    
|   ├── repository/   
|   |   ├── dependencies.py
|   |   └── models.py            # Recursos compartilhados
│   | 
|   ├── models.py           # Base dos modelos (metadata)
|   └── schemas.py 
|
├── atleta/                 # Módulo de domínio "Atleta"
│   ├── models.py           # Modelo SQLAlchemy
│   ├── schemas.py          # Schemas Pydantic
│   ├── controller.py       # Rotas/handlers
│   └── service.py          # Regras de negócio
│
├── categorias/             # Módulo de domínio "Categoria"
│   ├── models.py
│   ├── schemas.py
│   ├── controller.py
│   └── service.py
│
├── centro_treinamento/     # Módulo de domínio "Centro de Treinamento"
│   ├── models.py
│   ├── schemas.py
│   ├── controller.py
│   └── service.py
│
├── alembic/                # Migrações do banco
│   ├── versions/           # Arquivos de migração
│   └── env.py              # Configuração do Alembic
│
├── tests/     
|   ├── cofitest.py             # Testes automatizados
│   ├── test_atleta.py
│   ├── test_categoria.py
│   └── test_centro.py
│
├── requirements.txt        # Dependências do projeto
├── docker-compose.yml      # Configuração do PostgreSQL
├── Dockerfile              # Container da aplicação

routers
requirements-
rascunhos
makefile
maia
docker compose
alembic.ini
contrib
configs
venv
