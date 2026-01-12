# Guia de Integração - n8n + EasyPanel + PostgreSQL

## 📋 Visão Geral

Este guia mostra como integrar sua automação n8n com o sistema de devocionais e fazer deploy no EasyPanel usando PostgreSQL.

## 🏗️ Arquitetura

```
n8n (IA gera devocional) 
    ↓
Webhook → API Python (salva no PostgreSQL)
    ↓
Scheduler (envia automaticamente via Evolution API)
    ↓
WhatsApp
```

## 🔧 Configuração PostgreSQL

### 1. No EasyPanel

1. Crie um novo banco de dados PostgreSQL
2. Anote as credenciais:
   - Host
   - Port
   - Database name
   - Username
   - Password

### 2. Configurar no `.env`

```env
# Database - PostgreSQL
DATABASE_URL=postgresql://usuario:senha@host:porta/nome_do_banco

# Exemplo:
# DATABASE_URL=postgresql://postgres:senha123@db.easypanel.app:5432/devocional_db
```

### 3. Migração de Dados (se tiver no Supabase)

Se você já tem contatos no Supabase, pode migrar:

```python
# Script de migração (criar arquivo migrate_from_supabase.py)
import requests
from app.database import SessionLocal, DevocionalContato

# Suas credenciais do Supabase
SUPABASE_URL = "https://seu-projeto.supabase.co"
SUPABASE_KEY = "sua-chave"

def migrate_contacts():
    # Buscar do Supabase
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/contatos",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        }
    )
    
    contacts = response.json()
    
    # Salvar no PostgreSQL local
    db = SessionLocal()
    try:
        for contact in contacts:
            existing = db.query(DevocionalContato).filter(
                DevocionalContato.phone == contact['phone']
            ).first()
            
            if not existing:
                db_contact = DevocionalContato(
                    phone=contact['phone'],
                    name=contact.get('name'),
                    active=contact.get('active', True)
                )
                db.add(db_contact)
        
        db.commit()
        print(f"Migrados {len(contacts)} contatos")
    finally:
        db.close()
```

## 🔗 Integração com n8n

### Opção 1: Webhook (Recomendado)

No n8n, após gerar o devocional com IA:

1. **Adicione um nó HTTP Request**
2. **Configure:**
   - Method: `POST`
   - URL: `https://seu-dominio.com/api/devocional/webhook`
   - Headers:
     ```
     Content-Type: application/json
     X-Webhook-Secret: seu-secret-aqui (se configurado)
     ```
   - Body (JSON):
     ```json
     {
       "text": "{{ $json.texto_formatado }}",
       "title": "{{ $json.titulo }}",
       "metadata": {
         "versiculo": "{{ $json.versiculo }}",
         "autor": "{{ $json.autor }}"
       }
     }
     ```

### Opção 2: API Externa

Se preferir que o sistema busque da sua API:

1. **No n8n**, crie um endpoint que retorna o devocional:
   - Exemplo: `https://seu-n8n.com/api/devocional/today`

2. **Configure no `.env`:**
   ```env
   DEVOCIONAL_FETCH_MODE=api
   DEVOCIONAL_API_URL=https://seu-n8n.com/api/devocional/today
   DEVOCIONAL_API_KEY=sua-chave-api
   ```

3. **Formato esperado da resposta:**
   ```json
   {
     "text": "Seu devocional formatado aqui...",
     "title": "Título (opcional)",
     "metadata": {
       "versiculo": "...",
       "autor": "..."
     }
   }
   ```

## 🚀 Deploy no EasyPanel

### 1. Preparar Repositório

1. **Crie um repositório no GitHub** com seu código
2. **Adicione arquivos necessários:**

#### `Dockerfile`
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

#### `.dockerignore`
```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
*.db
*.sqlite
.git
.gitignore
README.md
```

#### `docker-compose.yml` (opcional, para desenvolvimento)
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/devocional
      - EVOLUTION_API_URL=http://evolution:8080
      - EVOLUTION_API_KEY=sua-chave
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=devocional
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### 2. Deploy no EasyPanel

1. **Criar novo projeto**
   - Tipo: `Application`
   - Source: `GitHub`
   - Repositório: Seu repositório

2. **Configurar Build**
   - Build Command: (deixe vazio, usa Dockerfile)
   - Port: `8000`

3. **Adicionar Banco de Dados**
   - Tipo: `PostgreSQL`
   - Anote as credenciais

4. **Variáveis de Ambiente**
   ```
   DATABASE_URL=postgresql://user:pass@db-host:5432/dbname
   EVOLUTION_API_URL=http://evolution:8080
   EVOLUTION_API_KEY=sua-chave-evolution
   EVOLUTION_INSTANCE_NAME=Devocional
   DELAY_BETWEEN_MESSAGES=3.0
   MAX_MESSAGES_PER_HOUR=20
   MAX_MESSAGES_PER_DAY=200
   DEVOCIONAL_WEBHOOK_SECRET=seu-secret-aqui
   DEVOCIONAL_FETCH_MODE=webhook
   ```

5. **Deploy!**

## 📡 Endpoints Disponíveis

### Webhook (para n8n)
```
POST /api/devocional/webhook
Content-Type: application/json
X-Webhook-Secret: seu-secret (opcional)

Body:
{
  "text": "Seu devocional formatado...",
  "title": "Título (opcional)",
  "metadata": {}
}
```

### Enviar Devocional
```
POST /api/devocional/send
{
  "message": "Texto do devocional",
  "delay": 3.0
}
```

### Buscar Devocional de Hoje
```
GET /api/devocional/today
```

### Estatísticas
```
GET /api/devocional/stats
```

## 🔄 Fluxo Completo

### 1. n8n gera devocional
```javascript
// No n8n, após gerar com IA
const devocional = {
  text: $json.texto_formatado,
  title: $json.titulo,
  metadata: {
    versiculo: $json.versiculo,
    autor: "Alex e Daniela Mantovani"
  }
};

// Enviar via webhook
await $http.post('https://sua-api.com/api/devocional/webhook', {
  headers: {
    'X-Webhook-Secret': 'seu-secret'
  },
  body: devocional
});
```

### 2. Sistema salva no PostgreSQL
- Devocional é salvo na tabela `devocionais`
- Fica disponível para envio

### 3. Scheduler envia automaticamente
- No horário configurado (`DEVOCIONAL_SEND_TIME`)
- Busca devocional do banco
- Envia para todos os contatos ativos
- Com rate limiting e proteções

## 🧪 Testando a Integração

### 1. Testar Webhook
```bash
curl -X POST https://sua-api.com/api/devocional/webhook \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Secret: seu-secret" \
  -d '{
    "text": "Teste de devocional",
    "title": "Teste"
  }'
```

### 2. Verificar se foi salvo
```bash
curl https://sua-api.com/api/devocional/today
```

### 3. Enviar manualmente
```bash
curl -X POST https://sua-api.com/api/devocional/send \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Teste de envio"
  }'
```

## 🔐 Segurança

### Webhook Secret
Configure um secret para proteger o webhook:

```env
DEVOCIONAL_WEBHOOK_SECRET=seu-secret-super-seguro-aqui
```

No n8n, adicione no header:
```
X-Webhook-Secret: seu-secret-super-seguro-aqui
```

### API Key (se usar modo API)
```env
DEVOCIONAL_API_KEY=sua-chave-api
```

## 📊 Monitoramento

### Ver estatísticas
```bash
GET /api/devocional/stats
```

Retorna:
- Mensagens enviadas hoje/hora
- Taxa de sucesso
- Status da instância Evolution
- Limites configurados

### Ver histórico
```bash
GET /api/devocional/envios?limit=50
GET /api/devocional/devocionais?limit=50
```

## 🐛 Troubleshooting

### Erro de conexão com PostgreSQL
- Verifique `DATABASE_URL` no `.env`
- Confirme que o banco está acessível
- Teste conexão: `psql $DATABASE_URL`

### Webhook não recebe
- Verifique `X-Webhook-Secret` (se configurado)
- Confirme que a URL está correta
- Veja logs: `docker logs seu-container`

### Devocional não é enviado
- Verifique se há devocional para hoje: `GET /api/devocional/today`
- Confirme contatos ativos: `GET /api/devocional/contatos`
- Veja logs do scheduler

## 📝 Checklist de Deploy

- [ ] Repositório no GitHub criado
- [ ] Dockerfile configurado
- [ ] Banco PostgreSQL criado no EasyPanel
- [ ] Variáveis de ambiente configuradas
- [ ] Webhook do n8n configurado
- [ ] Secret do webhook configurado
- [ ] Evolution API acessível
- [ ] Contatos migrados (se necessário)
- [ ] Teste de webhook funcionando
- [ ] Scheduler configurado
- [ ] Monitoramento ativo

## 🎯 Próximos Passos

1. **Configure o webhook no n8n** após gerar o devocional
2. **Teste enviando um devocional** manualmente
3. **Monitore as estatísticas** para ajustar rate limits
4. **Ajuste horário de envio** conforme necessário
5. **Adicione mais contatos** conforme cresce

---

**Sistema pronto para produção com integração completa n8n + EasyPanel + PostgreSQL!** 🚀
