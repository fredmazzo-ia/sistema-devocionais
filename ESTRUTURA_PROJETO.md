# 📁 Estrutura Detalhada do Projeto

## Árvore de Diretórios

```
sistema-devocionais/
│
├── backend/                          # Backend Python (FastAPI)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # Aplicação FastAPI principal
│   │   ├── config.py                # Configurações e Settings
│   │   ├── database.py              # Modelos SQLAlchemy
│   │   ├── logging_config.py        # Configuração de logs
│   │   │
│   │   ├── routers/                 # Endpoints da API
│   │   │   ├── __init__.py
│   │   │   ├── devocional.py        # Endpoints principais
│   │   │   ├── devocional_context.py # Contexto histórico
│   │   │   ├── devocional_test.py   # Endpoints de teste
│   │   │   ├── news.py              # (Legado - não usado)
│   │   │   ├── monitoring.py       # (Legado - não usado)
│   │   │   └── notifications.py     # (Legado - não usado)
│   │   │
│   │   ├── devocional_service.py    # Lógica de envio WhatsApp
│   │   ├── devocional_scheduler.py  # Agendamento automático
│   │   ├── devocional_integration.py # Integração com APIs
│   │   ├── whatsapp_service.py     # (Legado - não usado)
│   │   ├── scraper.py               # (Legado - não usado)
│   │   ├── analyzer.py              # (Legado - não usado)
│   │   └── scheduler.py             # (Legado - não usado)
│   │
│   ├── requirements.txt            # Dependências Python
│   └── env.example                  # Exemplo de variáveis
│
├── database/                        # Scripts SQL
│   ├── devocionais_schema.sql       # Schema completo
│   ├── migrate_metadata_to_metadata_json.sql # Migração
│   ├── limpar_devocionais_manter_contatos.sql # Limpeza
│   ├── adicionar_contato_frederico.sql # Exemplo
│   ├── adicionar_contato_alex.sql  # Exemplo
│   └── example_queries.sql         # Queries úteis
│
├── Dockerfile                        # Container Docker
├── docker-compose.example.yml        # Docker Compose
├── .dockerignore                    # Arquivos ignorados no build
│
└── Documentação/                    # Documentação do projeto
    ├── README.md                    # Documentação principal
    ├── GUIA_RAPIDO_INICIO.md        # Guia rápido
    ├── ESTRUTURA_PROJETO.md         # Este arquivo
    ├── DEPLOY_GITHUB_EASYPANEL.md   # Deploy
    ├── WORKFLOW_N8N_COMPLETO_PASSO_A_PASSO.md # Workflow n8n
    ├── PROMPT_GERADOR_N8N.md        # Prompt geração
    ├── PROMPT_ANALISE_N8N.md        # Prompt análise
    ├── CODIGO_EXTRAIR_JSON_IA.md    # Extração JSON
    └── ... (outros guias)
```

## 🔑 Arquivos Principais

### Backend

#### `backend/app/main.py`
- Aplicação FastAPI principal
- Configuração de CORS
- Registro de routers
- Lifespan events (start/stop scheduler)

#### `backend/app/config.py`
- Classe `Settings` com Pydantic
- Todas as variáveis de ambiente
- Valores padrão

#### `backend/app/database.py`
- Modelos SQLAlchemy:
  - `Devocional`
  - `DevocionalContato`
  - `DevocionalEnvio`
- Funções `init_db()` e `get_db()`

#### `backend/app/routers/devocional.py`
- Endpoints principais:
  - `POST /api/devocional/webhook` - Receber devocional
  - `POST /api/devocional/send` - Enviar devocional
  - `GET /api/devocional/today` - Devocional de hoje
  - `GET /api/devocional/devocionais` - Listar todos
  - `GET /api/devocional/horario` - Verificar horário
  - `POST /api/devocional/contatos` - Adicionar contato
  - `GET /api/devocional/contatos` - Listar contatos
  - `DELETE /api/devocional/contatos/{id}` - Remover contato
  - `GET /api/devocional/stats` - Estatísticas

#### `backend/app/devocional_service.py`
- Classe `DevocionalService`
- Lógica de envio via Evolution API
- Rate limiting
- Retry automático
- Personalização de mensagens

#### `backend/app/devocional_scheduler.py`
- Agendamento automático diário
- Usa timezone de São Paulo
- Envio em massa

#### `backend/app/devocional_integration.py`
- Integração com APIs externas
- Salvar devocionais
- Buscar devocionais

### Database

#### `database/devocionais_schema.sql`
- Schema completo do PostgreSQL
- Tabelas, índices, views, funções

#### `database/migrate_metadata_to_metadata_json.sql`
- Migração para renomear campo `metadata`

## 🔄 Fluxo de Dados

```
n8n (IA) 
  → Webhook (/api/devocional/webhook)
    → Salva no PostgreSQL (devocionais)
      → Scheduler (06:00 SP)
        → DevocionalService
          → Evolution API
            → WhatsApp
```

## 📦 Dependências Principais

- `fastapi` - Framework web
- `uvicorn` - Servidor ASGI
- `sqlalchemy` - ORM
- `psycopg2-binary` - Driver PostgreSQL
- `pydantic` - Validação de dados
- `requests` - HTTP client
- `schedule` - Agendamento
- `zoneinfo` - Timezones (Python 3.9+)

---

**Estrutura completa documentada!** 📁
