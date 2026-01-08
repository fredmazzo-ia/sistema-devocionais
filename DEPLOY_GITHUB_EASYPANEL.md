# 🚀 Guia Completo: Deploy no GitHub + EasyPanel

## 📋 Pré-requisitos

- [ ] Conta no GitHub
- [ ] Conta no EasyPanel
- [ ] Repositório criado no GitHub
- [ ] Acesso SSH ou HTTPS ao repositório

## 🔧 Passo 1: Preparar Repositório no GitHub

### 1.1 Criar Repositório

1. Acesse [GitHub](https://github.com)
2. Clique em **"New repository"**
3. Configure:
   - **Name**: `sistema-devocionais` (ou nome de sua preferência)
   - **Description**: "Sistema de envio automático de devocionais via WhatsApp"
   - **Visibility**: Private (recomendado) ou Public
   - **NÃO** marque "Initialize with README" (já temos arquivos)

### 1.2 Inicializar Git Local

Abra o terminal na pasta do projeto:

```bash
# Navegar para a pasta do projeto
cd C:\Users\fred\OneDrive\Documentos\Imprensa

# Inicializar git (se ainda não tiver)
git init

# Adicionar todos os arquivos
git add .

# Fazer commit inicial
git commit -m "Initial commit: Sistema de devocionais completo"

# Adicionar remote do GitHub
git remote add origin https://github.com/SEU_USUARIO/sistema-devocionais.git

# Ou se usar SSH:
# git remote add origin git@github.com:SEU_USUARIO/sistema-devocionais.git

# Enviar para GitHub
git branch -M main
git push -u origin main
```

## 📝 Passo 2: Criar .gitignore

Crie arquivo `.gitignore` na raiz do projeto:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# Database
*.db
*.sqlite
*.sqlite3

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Frontend (se tiver)
node_modules/
dist/
build/
.next/

# Temporary
*.tmp
*.temp
```

## 🐳 Passo 3: Verificar Dockerfile

Certifique-se que o `Dockerfile` está na raiz do projeto (já criamos antes):

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY backend/ .

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1

# Expor porta
EXPOSE 8000

# Comando
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📦 Passo 4: Criar README.md (se não tiver)

Crie `README.md` na raiz:

```markdown
# Sistema de Envio de Devocionais

Sistema robusto para envio automático de devocionais via WhatsApp usando Evolution API.

## 🚀 Tecnologias

- Python 3.11
- FastAPI
- PostgreSQL
- Evolution API
- Docker

## 📋 Configuração

Veja `INTEGRACAO_N8N_EASYPANEL.md` para instruções completas.

## 🔧 Variáveis de Ambiente

Veja `backend/env.example` para todas as variáveis necessárias.
```

## 🚀 Passo 5: Deploy no EasyPanel

### 5.1 Criar Projeto no EasyPanel

1. Acesse seu EasyPanel
2. Clique em **"New Project"**
3. Escolha **"Application"**
4. Configure:
   - **Name**: `devocionais-api`
   - **Source**: `GitHub`
   - **Repository**: Selecione seu repositório
   - **Branch**: `main`

### 5.2 Configurar Build

No EasyPanel, configure:

**Build Settings:**
- **Build Command**: (deixe vazio - usa Dockerfile)
- **Port**: `8000`
- **Dockerfile Path**: `Dockerfile` (raiz do projeto)

### 5.3 Adicionar Banco de Dados

1. No projeto, clique em **"Add Service"**
2. Escolha **"PostgreSQL"**
3. Configure:
   - **Name**: `devocionais-db`
   - **Version**: `15` (ou mais recente)
4. Anote as credenciais:
   - Host
   - Port
   - Database
   - Username
   - Password

### 5.4 Configurar Variáveis de Ambiente

No projeto, vá em **"Environment Variables"** e adicione:

```env
# Database
DATABASE_URL=postgresql://usuario:senha@devocionais-db:5432/devocionais

# Evolution API
EVOLUTION_API_URL=http://evolution:8080
EVOLUTION_API_KEY=sua-chave-evolution
EVOLUTION_INSTANCE_NAME=Devocional

# Rate Limiting
DELAY_BETWEEN_MESSAGES=3.0
MAX_MESSAGES_PER_HOUR=20
MAX_MESSAGES_PER_DAY=200

# Retry
MAX_RETRIES=3
RETRY_DELAY=5.0

# Scheduler
DEVOCIONAL_SEND_TIME=06:00

# Webhook
DEVOCIONAL_WEBHOOK_SECRET=seu-secret-super-seguro
DEVOCIONAL_FETCH_MODE=webhook
```

### 5.5 Deploy

1. Clique em **"Deploy"**
2. Aguarde o build completar
3. Verifique os logs se houver erros

## 🔍 Passo 6: Verificar Deploy

### 6.1 Testar API

Após deploy, teste:

```bash
# Health check
curl https://seu-dominio.easypanel.app/health

# Deve retornar: {"status": "healthy"}
```

### 6.2 Verificar Banco de Dados

No EasyPanel, acesse o banco e execute:

```sql
-- Verificar tabelas criadas
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';

-- Deve mostrar:
-- devocionais
-- devocional_contatos
-- devocional_envios
```

### 6.3 Criar Tabelas (se necessário)

Se as tabelas não foram criadas automaticamente, execute o schema:

```bash
# No terminal do EasyPanel ou via psql
psql $DATABASE_URL < database/devocionais_schema.sql
```

## 🔗 Passo 7: Configurar n8n

### 7.1 Atualizar URL do Webhook

No n8n, atualize a URL do webhook:

```
Antes: http://localhost:8000/api/devocional/webhook
Agora: https://seu-dominio.easypanel.app/api/devocional/webhook
```

### 7.2 Adicionar Header de Segurança

No n8n, adicione header:

```
X-Webhook-Secret: seu-secret-super-seguro
```

## 📊 Passo 8: Testar Fluxo Completo

### 8.1 Testar Webhook

No n8n, teste enviando um devocional:

```json
POST https://seu-dominio.easypanel.app/api/devocional/webhook
Headers:
  Content-Type: application/json
  X-Webhook-Secret: seu-secret

Body: {
  "text": "📅 ...",
  "title": "...",
  ...
}
```

### 8.2 Verificar no Banco

```sql
SELECT * FROM devocionais ORDER BY created_at DESC LIMIT 1;
```

### 8.3 Testar Envio

```bash
POST https://seu-dominio.easypanel.app/api/devocional/send
Body: {
  "message": "Teste"
}
```

## 🐛 Troubleshooting

### Erro: "Cannot connect to database"
- Verifique `DATABASE_URL` nas variáveis de ambiente
- Confirme que o banco está rodando
- Verifique se o nome do serviço está correto

### Erro: "Module not found"
- Verifique se `requirements.txt` está completo
- Confirme que o build instalou todas as dependências

### Erro: "Port already in use"
- Verifique se a porta 8000 está configurada corretamente
- Confirme que não há outro serviço usando a porta

## ✅ Checklist Final

- [ ] Repositório criado no GitHub
- [ ] Código enviado para GitHub
- [ ] Projeto criado no EasyPanel
- [ ] Banco PostgreSQL criado
- [ ] Variáveis de ambiente configuradas
- [ ] Deploy realizado com sucesso
- [ ] Health check funcionando
- [ ] Tabelas criadas no banco
- [ ] Webhook do n8n atualizado
- [ ] Teste de envio funcionando

---

**Pronto para deploy!** 🚀
