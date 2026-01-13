# ⚡ Resumo Rápido: GitHub + EasyPanel

## 🎯 Esclarecimento Importante

**Você NÃO precisa gravar no banco manualmente!**

O fluxo é automático:
1. n8n → Webhook → **Sistema salva automaticamente no banco**
2. Scheduler (06:00) → **Envia automaticamente para contatos**

---

## 🚀 PARTE 1: GitHub (5 minutos)

### 1. Criar Repositório
- Acesse: https://github.com/new
- Nome: `sistema-devocionais`
- Clique em "Create repository"

### 2. Enviar Código

Abra **PowerShell** na pasta do projeto:

```powershell
cd "C:\Users\fred\OneDrive\Documentos\Imprensa"

# Se não tiver git inicializado:
git init
git add .
git commit -m "Sistema completo de devocionais"

# Adicionar GitHub (SUBSTITUA SEU_USUARIO)
git remote add origin https://github.com/SEU_USUARIO/sistema-devocionais.git

# Enviar
git branch -M main
git push -u origin main
```

**Pronto!** ✅

---

## 🐳 PARTE 2: EasyPanel (10 minutos)

### 1. Criar Projeto
- EasyPanel → "New Project" → "Application"
- Source: GitHub → Selecione seu repositório
- Port: `8000`
- Build Command: (deixe vazio - usa Dockerfile)

### 2. Criar Banco
- "Add Service" → PostgreSQL
- Name: `devocionais-db`
- **ANOTE** as credenciais!

### 3. Variáveis de Ambiente

Adicione estas variáveis (SUBSTITUA os valores):

```env
DATABASE_URL=postgresql://postgres:SUA_SENHA@devocionais-db:5432/postgres
EVOLUTION_API_URL=http://sua-evolution-api:8080
EVOLUTION_API_KEY=sua-chave
EVOLUTION_INSTANCE_NAME=Devocional
DELAY_BETWEEN_MESSAGES=3.0
MAX_MESSAGES_PER_HOUR=20
MAX_MESSAGES_PER_DAY=200
MAX_RETRIES=3
RETRY_DELAY=5.0
DEVOCIONAL_SEND_TIME=06:00
DEVOCIONAL_WEBHOOK_SECRET=seu-secret-aqui
DEVOCIONAL_FETCH_MODE=webhook
```

### 4. Deploy
- Clique em "Deploy"
- Aguarde build completar

### 5. Criar Tabelas

Após deploy, execute o SQL:
- Acesse o banco no EasyPanel
- Vá em "SQL Editor" ou "Database"
- Cole o conteúdo de `database/devocionais_schema.sql`
- Execute

### 6. Testar
- Acesse: `https://seu-projeto.easypanel.app/health`
- Deve retornar: `{"status": "healthy"}`

---

## 🔗 PARTE 3: Atualizar n8n (2 minutos)

No n8n, atualize o webhook:

**URL:**
```
https://seu-projeto.easypanel.app/api/devocional/webhook
```

**Header:**
```
X-Webhook-Secret: seu-secret-aqui
```

---

## ✅ Checklist

- [ ] Repositório no GitHub criado
- [ ] Código enviado (git push)
- [ ] Projeto no EasyPanel criado
- [ ] Banco PostgreSQL criado
- [ ] Variáveis configuradas
- [ ] Deploy realizado
- [ ] Tabelas criadas
- [ ] Health check OK
- [ ] n8n atualizado

---

**Pronto! Siga na ordem e me avise se precisar de ajuda!** 🚀
