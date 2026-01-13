# 🚀 Guia Passo a Passo: GitHub + EasyPanel

## 📋 Resumo do Fluxo

**Você NÃO precisa gravar no banco manualmente!**

O fluxo é:
1. n8n gera devocional → Envia para webhook
2. Sistema recebe → **Salva automaticamente no banco**
3. Scheduler (06:00) → **Envia automaticamente para contatos**

---

## 🔧 PARTE 1: GitHub

### Passo 1: Criar Repositório no GitHub

1. Acesse: https://github.com/new
2. Preencha:
   - **Repository name**: `sistema-devocionais` (ou outro nome)
   - **Description**: "Sistema de envio automático de devocionais"
   - **Visibility**: Private (recomendado)
   - **NÃO** marque "Add README" (já temos arquivos)
3. Clique em **"Create repository"**

### Passo 2: Enviar Código para GitHub

Abra o **PowerShell** ou **Git Bash** na pasta do projeto:

```powershell
# Navegar para a pasta
cd "C:\Users\fred\OneDrive\Documentos\Imprensa"

# Verificar se já tem git
git status

# Se não tiver git inicializado:
git init

# Adicionar todos os arquivos
git add .

# Fazer commit
git commit -m "Sistema completo de devocionais"

# Adicionar remote (SUBSTITUA SEU_USUARIO)
git remote add origin https://github.com/SEU_USUARIO/sistema-devocionais.git

# Enviar para GitHub
git branch -M main
git push -u origin main
```

**Se pedir autenticação:**
- Use seu **token do GitHub** (não a senha)
- Ou configure SSH

### Passo 3: Verificar no GitHub

Acesse seu repositório e confirme que todos os arquivos estão lá.

---

## 🐳 PARTE 2: EasyPanel

### Passo 1: Criar Projeto

1. Acesse seu EasyPanel
2. Clique em **"New Project"** ou **"+"**
3. Escolha **"Application"**
4. Preencha:
   - **Name**: `devocionais-api`
   - **Source**: `GitHub`
   - **Repository**: Selecione `sistema-devocionais`
   - **Branch**: `main`

### Passo 2: Configurar Build

Na tela de configuração:

**Build Settings:**
- **Build Command**: (deixe **VAZIO** - usa Dockerfile)
- **Port**: `8000`
- **Dockerfile Path**: `Dockerfile` (deve estar na raiz)

**IMPORTANTE**: O Dockerfile já está criado na raiz do projeto!

### Passo 3: Criar Banco PostgreSQL

1. No projeto, clique em **"Add Service"** ou **"+"**
2. Escolha **"PostgreSQL"**
3. Configure:
   - **Name**: `devocionais-db`
   - **Version**: `15` (ou mais recente)
4. Clique em **"Create"**
5. **ANOTE** as credenciais que aparecerem:
   - Host: `devocionais-db` (ou similar)
   - Port: `5432`
   - Database: `postgres` (ou o nome que você escolher)
   - Username: `postgres` (ou o que aparecer)
   - Password: (anote essa senha!)

### Passo 4: Configurar Variáveis de Ambiente

No projeto, vá em **"Environment Variables"** ou **"Env"** e adicione:

```env
# Database (SUBSTITUA com as credenciais do banco)
DATABASE_URL=postgresql://postgres:SUA_SENHA@devocionais-db:5432/postgres

# Evolution API (SUBSTITUA com suas credenciais)
EVOLUTION_API_URL=http://sua-evolution-api:8080
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
DEVOCIONAL_WEBHOOK_SECRET=seu-secret-super-seguro-aqui
DEVOCIONAL_FETCH_MODE=webhook
```

**IMPORTANTE**: 
- Substitua `SUA_SENHA` pela senha do banco
- Substitua `sua-evolution-api` pela URL real da Evolution API
- Substitua `sua-chave-evolution` pela chave real

### Passo 5: Fazer Deploy

1. Clique em **"Deploy"** ou **"Save & Deploy"**
2. Aguarde o build (pode levar alguns minutos)
3. Acompanhe os logs

### Passo 6: Criar Tabelas no Banco

Após o deploy, você precisa executar o schema SQL:

**Opção A: Via Terminal do EasyPanel**

1. No projeto, vá em **"Terminal"** ou **"Console"**
2. Execute:
```bash
# Conectar no banco
psql $DATABASE_URL

# Ou se não funcionar:
psql -h devocionais-db -U postgres -d postgres
```

3. Cole o conteúdo de `database/devocionais_schema.sql`
4. Execute

**Opção B: Via Interface do EasyPanel**

1. Acesse o serviço do banco
2. Vá em **"Database"** ou **"SQL Editor"**
3. Cole o conteúdo de `database/devocionais_schema.sql`
4. Execute

### Passo 7: Verificar se Funcionou

1. Acesse a URL do seu projeto (ex: `https://seu-projeto.easypanel.app`)
2. Teste: `https://seu-projeto.easypanel.app/health`
3. Deve retornar: `{"status": "healthy"}`

---

## 🔗 PARTE 3: Configurar n8n

### Passo 1: Atualizar URL do Webhook

No seu workflow do n8n, atualize:

**Antes:**
```
http://localhost:8000/api/devocional/webhook
```

**Agora:**
```
https://seu-projeto.easypanel.app/api/devocional/webhook
```

### Passo 2: Adicionar Header de Segurança

No nó HTTP Request do webhook, adicione header:

```
X-Webhook-Secret: seu-secret-super-seguro-aqui
```

(Use o mesmo valor que colocou em `DEVOCIONAL_WEBHOOK_SECRET`)

---

## ✅ Checklist Completo

### GitHub:
- [ ] Repositório criado
- [ ] Código enviado (git push)
- [ ] Arquivos visíveis no GitHub

### EasyPanel:
- [ ] Projeto criado
- [ ] Conectado ao GitHub
- [ ] Banco PostgreSQL criado
- [ ] Variáveis de ambiente configuradas
- [ ] Deploy realizado
- [ ] Tabelas criadas no banco
- [ ] Health check funcionando

### n8n:
- [ ] URL do webhook atualizada
- [ ] Header de segurança adicionado
- [ ] Teste de envio realizado

---

## 🐛 Problemas Comuns

### "Cannot connect to database"
- Verifique `DATABASE_URL` (formato correto)
- Confirme que o nome do serviço está certo (`devocionais-db`)
- Verifique se o banco está rodando

### "Build failed"
- Verifique se o Dockerfile está na raiz
- Confirme que `requirements.txt` existe
- Veja os logs do build

### "Port 8000 already in use"
- Verifique se não há outro serviço na porta
- Confirme que a porta está configurada como 8000

---

**Pronto! Siga os passos na ordem e me avise se tiver alguma dúvida!** 🚀
