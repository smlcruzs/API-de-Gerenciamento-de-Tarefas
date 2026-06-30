# API de Gerenciamento de Tarefas

API REST para gerenciamento de tarefas com autenticação JWT e múltiplos usuários, construída em **Clean Architecture**: as regras de negócio não conhecem FastAPI, SQLAlchemy ou nenhum detalhe de infraestrutura.

## Stack

- **FastAPI** — routers e validação de entrada
- **PostgreSQL** + **SQLAlchemy 2.0** — persistência
- **JWT** (PyJWT) + **bcrypt** — autenticação
- **Pytest** — testes unitários e de integração
- **Docker / docker-compose** — ambiente de desenvolvimento

## Arquitetura

```
Frameworks & Drivers     FastAPI · PostgreSQL · JWT · Pytest
  └─ Interface Adapters   Routers · Schemas (Pydantic) · Repository impl.
       └─ Use Cases       CreateTask · ListTasks · UpdateTask · DeleteTask ...
            └─ Entities   Task · User (regra de negócio pura)
```

Regra de ouro: a dependência sempre aponta para dentro. `Entities` não conhece FastAPI. `Use Cases` não conhece PostgreSQL — eles dependem apenas de interfaces (`TaskRepository`, `UserRepository`, `PasswordHasher`, `TokenService`), e as implementações concretas são injetadas via `Depends()` na camada de adapters.

### Fluxo de uma requisição (`POST /tasks`)

1. O router [tasks.py](task_manager/adapters/api/tasks.py) recebe o JSON.
2. O schema Pydantic [task_schema.py](task_manager/adapters/schemas/task_schema.py) valida o payload.
3. `Depends()` resolve o usuário autenticado (decodifica o JWT) e instancia o use case `CreateTask`, injetando um `SQLTaskRepository` já configurado com a sessão do banco — via [dependencies.py](task_manager/adapters/api/dependencies.py).
4. O use case [create_task.py](task_manager/application/use_cases/create_task.py) cria a entity `Task`, validando as regras de negócio, e chama `repository.save(task)` — sem saber que por trás existe SQL.
5. O [sql_task_repository.py](task_manager/infrastructure/sql_task_repository.py) converte a entity em modelo SQLAlchemy e persiste no Postgres.

## Estrutura de pastas

```
task_manager/
├── domain/
│   ├── entities/        # Task, User — regra de negócio pura
│   ├── interfaces/      # TaskRepository, UserRepository, PasswordHasher, TokenService (ABCs)
│   └── exceptions.py
├── application/
│   └── use_cases/       # create_task, list_tasks, get_task, update_task, delete_task, register_user, login_user
├── adapters/
│   ├── api/              # routers (tasks.py, auth.py) + dependencies.py (composition root)
│   └── schemas/          # Pydantic (task_schema.py, user_schema.py)
├── infrastructure/
│   ├── models.py          # SQLAlchemy models
│   ├── database.py        # engine, sessão
│   ├── sql_task_repository.py / sql_user_repository.py
│   └── security/           # BcryptPasswordHasher, JWTTokenService
└── main.py

tests/
├── unit/          # entities, use cases (com fakes/in-memory), bcrypt, JWT
├── integration/   # repositories SQL e API completa, contra SQLite em memória
└── fakes/         # InMemoryTaskRepository, InMemoryUserRepository, FakePasswordHasher, FakeTokenService
```

## Como rodar

### Com Docker (recomendado)

```bash
cp .env.example .env
docker compose up --build
```

A API sobe em `http://localhost:8000` (docs interativas em `/docs`). Se você já tiver um Postgres local usando a porta 5432, ajuste `POSTGRES_PORT` no seu `.env`.

### Localmente, sem Docker

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
pytest                           # roda a suíte de testes (usa SQLite em memória)
```

Para subir a API local sem Docker, é necessário um Postgres acessível e a variável `DATABASE_URL` configurada; depois:

```bash
uvicorn task_manager.main:app --reload
```

## Variáveis de ambiente

Ver [.env.example](.env.example):

| Variável | Descrição |
|---|---|
| `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_DB` | Credenciais do Postgres |
| `POSTGRES_PORT` | Porta exposta no host para o container do Postgres (padrão `5432`) |
| `DATABASE_URL` | String de conexão usada pela aplicação |
| `JWT_SECRET_KEY` / `JWT_ALGORITHM` / `JWT_EXPIRE_MINUTES` | Configuração do token JWT |

## Endpoints

| Método | Rota | Descrição | Auth |
|---|---|---|---|
| POST | `/auth/register` | Cadastrar usuário | — |
| POST | `/auth/login` | Login → retorna JWT | — |
| GET | `/tasks` | Listar tarefas (filtros por `status`/`priority` + paginação `limit`/`offset`) | JWT |
| POST | `/tasks` | Criar tarefa | JWT |
| GET | `/tasks/{id}` | Buscar tarefa por ID | JWT |
| PUT | `/tasks/{id}` | Atualizar tarefa | JWT |
| PATCH | `/tasks/{id}/status` | Mudar status (`todo`→`in_progress`→`done`) | JWT |
| DELETE | `/tasks/{id}` | Deletar tarefa | JWT |

Tarefas são isoladas por usuário: tentar acessar/alterar a tarefa de outro usuário resulta em `404`.

## Testes

```bash
pytest tests/unit -v          # entities, use cases (com fakes), bcrypt, JWT
pytest tests/integration -v   # repositories SQL + API completa (SQLite em memória)
pytest -v                     # tudo
```

49 testes cobrindo entities, use cases, repositories e o fluxo completo da API (registro → login → CRUD → isolamento entre usuários).
