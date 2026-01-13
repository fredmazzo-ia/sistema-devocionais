# 📡 Endpoints da API - Guia Completo para n8n

## 🔗 Base URL

```
https://sua-api.com
```

## 🔐 Autenticação

Alguns endpoints requerem header:
```
X-Webhook-Secret: Fs142779
```

---

## 🚀 **ENVIOS E NOTIFICAÇÕES**

### **1. Enviar Devocional (via n8n Webhook)**

**Endpoint**: `POST /api/notifications/webhook`

**Headers**:
```
Content-Type: application/json
X-Webhook-Secret: Fs142779
```

**Body - Enviar Devocional**:
```json
{
  "event": "send_devocional",
  "devocional_id": 1,
  "delay": 3.0
}
```

**Body - Enviar com Mensagem Personalizada**:
```json
{
  "event": "send_devocional",
  "message": "Texto do devocional aqui...",
  "delay": 3.0
}
```

**Body - Enviar para Contatos Específicos**:
```json
{
  "event": "send_devocional",
  "devocional_id": 1,
  "contacts": [
    {"phone": "5516999999999", "name": "João"},
    {"phone": "5516888888888", "name": "Maria"}
  ],
  "delay": 3.0
}
```

**Response**:
```json
{
  "success": true,
  "message": "Envio concluído: 10 enviadas, 0 falharam",
  "data": {
    "total": 10,
    "sent": 10,
    "failed": 0,
    "results": [...]
  }
}
```

---

### **2. Enviar Teste**

**Endpoint**: `POST /api/notifications/webhook`

**Headers**:
```
Content-Type: application/json
X-Webhook-Secret: Fs142779
```

**Body**:
```json
{
  "event": "send_test",
  "phone": "5516999999999",
  "message": "Mensagem de teste"
}
```

---

### **3. Verificar Status das Instâncias**

**Endpoint**: `POST /api/notifications/webhook`

**Headers**:
```
Content-Type: application/json
X-Webhook-Secret: Fs142779
```

**Body**:
```json
{
  "event": "check_status"
}
```

**OU** (GET direto):

**Endpoint**: `GET /api/notifications/instances`

**Response**:
```json
{
  "total_instances": 4,
  "active_instances": 4,
  "instances": [
    {
      "name": "Devocional-1",
      "status": "active",
      "messages_sent_today": 45,
      "messages_sent_this_hour": 8
    }
  ]
}
```

---

## 📖 **DEVOCIONAIS**

### **4. Receber Devocional (Webhook n8n → API)**

**Endpoint**: `POST /api/devocional/webhook`

**Headers**:
```
Content-Type: application/json
X-Webhook-Secret: Fs142779 (opcional)
```

**Body**:
```json
{
  "text": "Texto do devocional formatado para WhatsApp",
  "title": "Título do Devocional",
  "date": "2024-01-15",
  "versiculo_principal": {
    "texto": "Versículo principal",
    "referencia": "João 3:16"
  },
  "versiculo_apoio": {
    "texto": "Versículo de apoio",
    "referencia": "Romanos 8:28"
  },
  "metadata": {
    "autor": "Alex e Daniela Mantovani",
    "tema": "Fé",
    "palavras_chave": ["fé", "esperança", "amor"]
  }
}
```

**Response**:
```json
{
  "success": true,
  "message": "Devocional recebido e salvo com sucesso",
  "devocional_id": 123,
  "date": "2024-01-15T00:00:00"
}
```

---

### **5. Enviar Devocional Manual**

**Endpoint**: `POST /api/devocional/send`

**Body**:
```json
{
  "message": "Texto do devocional aqui...",
  "delay": 3.0
}
```

**OU com devocional_id**:
```json
{
  "devocional_id": 1,
  "delay": 3.0
}
```

**OU para contato específico**:
```json
{
  "message": "Texto do devocional",
  "phone": "5516999999999",
  "delay": 3.0
}
```

---

### **6. Listar Devocionais**

**Endpoint**: `GET /api/devocional/devocionais?skip=0&limit=50`

**Query Parameters**:
- `skip`: Número de registros para pular (padrão: 0)
- `limit`: Número máximo de registros (padrão: 50)

---

### **7. Devocional de Hoje**

**Endpoint**: `GET /api/devocional/today`

**Response**:
```json
{
  "id": 123,
  "content": "Texto do devocional...",
  "title": "Título",
  "date": "2024-01-15",
  "sent": false
}
```

---

### **8. Verificar Horário**

**Endpoint**: `GET /api/devocional/horario`

**Response**:
```json
{
  "horario_sao_paulo": "2024-01-15 14:30:00 -03",
  "horario_utc": "2024-01-15 17:30:00 UTC",
  "saudacao_atual": "Boa tarde",
  "send_time_configurado": "06:00"
}
```

---

## 👥 **CONTATOS**

### **9. Listar Contatos**

**Endpoint**: `GET /api/devocional/contatos?active_only=true`

**Query Parameters**:
- `active_only`: Se true, retorna apenas contatos ativos (padrão: true)

---

### **10. Adicionar Contato**

**Endpoint**: `POST /api/devocional/contatos`

**Body**:
```json
{
  "phone": "5516999999999",
  "name": "João Silva"
}
```

---

### **11. Ativar/Desativar Contato**

**Endpoint**: `PUT /api/devocional/contatos/{id}/toggle`

**Exemplo**: `PUT /api/devocional/contatos/1/toggle`

---

### **12. Remover Contato**

**Endpoint**: `DELETE /api/devocional/contatos/{id}`

**Exemplo**: `DELETE /api/devocional/contatos/1`

---

## 📊 **ESTATÍSTICAS**

### **13. Estatísticas do Serviço**

**Endpoint**: `GET /api/devocional/stats`

**Response**:
```json
{
  "stats": {
    "total_sent": 150,
    "total_failed": 2,
    "total_blocked": 0,
    "messages_sent_today": 45,
    "messages_sent_this_hour": 8
  },
  "instance_status": {
    "status": "connected"
  }
}
```

---

### **14. Histórico de Envios**

**Endpoint**: `GET /api/devocional/envios?skip=0&limit=50&status=sent`

**Query Parameters**:
- `skip`: Número de registros para pular
- `limit`: Número máximo de registros
- `status`: Filtrar por status (sent, failed, blocked, pending)

---

## 🤖 **CONTEXTO PARA IA (n8n)**

### **15. Contexto Histórico**

**Endpoint**: `GET /api/devocional/context/historico?days=30`

**Query Parameters**:
- `days`: Número de dias para buscar (padrão: 30)

**Response**:
```json
{
  "historico": "...",
  "versiculos_usados": [...],
  "temas_abordados": [...]
}
```

---

### **16. Contexto para IA**

**Endpoint**: `GET /api/devocional/context/para-ia?days=30`

**Query Parameters**:
- `days`: Número de dias para buscar (padrão: 30)

**Response**:
```json
{
  "contexto_historico": "...",
  "versiculos_usados": [...],
  "direcionamento_sugerido": "...",
  "conceito_central": "..."
}
```

---

### **17. Contexto Vazio (Primeiro Devocional)**

**Endpoint**: `GET /api/devocional/test/contexto-vazio`

**Uso**: Quando ainda não há devocionais no banco

---

## ✅ **HEALTH CHECK**

### **18. Root**

**Endpoint**: `GET /`

**Response**:
```json
{
  "message": "Sistema de Envio de Devocionais",
  "status": "online"
}
```

---

### **19. Health**

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy"
}
```

---

## 🔄 **WORKFLOW N8N RECOMENDADO**

### **Fluxo Completo de Envio Diário**

```
1. GET /api/devocional/context/para-ia?days=30
   → Buscar contexto histórico

2. OpenAI (Análise)
   → Usar: PROMPT_ANALISE_HISTORICO.md
   → Input: {{ $json }}

3. OpenAI (Geração)
   → Usar: PROMPT_GERADOR_MELHORADO.md
   → Input: contexto + direcionamento

4. POST /api/devocional/webhook
   → Salvar devocional no banco
   → Body: {{ $json }}

5. POST /api/notifications/webhook
   → Enviar para todos os contatos
   → Body: {
     "event": "send_devocional",
     "devocional_id": {{ $('Salvar Devocional').item.json.devocional_id }}
   }
```

---

## 📝 **EXEMPLOS DE USO NO N8N**

### **Exemplo 1: Enviar Devocional Gerado**

**HTTP Request Node**:
- Method: `POST`
- URL: `https://sua-api.com/api/notifications/webhook`
- Headers:
  - `Content-Type`: `application/json`
  - `X-Webhook-Secret`: `Fs142779`
- Body (JSON):
```json
{
  "event": "send_devocional",
  "devocional_id": {{ $json.id }}
}
```

---

### **Exemplo 2: Buscar Contexto para IA**

**HTTP Request Node**:
- Method: `GET`
- URL: `https://sua-api.com/api/devocional/context/para-ia?days=30`

**Próximo Node (OpenAI)**:
- Prompt: Use `PROMPT_ANALISE_HISTORICO.md`
- Input: `{{ $json }}`

---

### **Exemplo 3: Salvar Devocional do n8n**

**HTTP Request Node**:
- Method: `POST`
- URL: `https://sua-api.com/api/devocional/webhook`
- Headers:
  - `Content-Type`: `application/json`
  - `X-Webhook-Secret`: `Fs142779`
- Body (JSON):
```json
{
  "text": "{{ $json.texto }}",
  "title": "{{ $json.titulo }}",
  "date": "{{ $now.format('YYYY-MM-DD') }}",
  "versiculo_principal": {
    "texto": "{{ $json.versiculo_principal_texto }}",
    "referencia": "{{ $json.versiculo_principal_ref }}"
  },
  "metadata": {
    "autor": "Alex e Daniela Mantovani",
    "tema": "{{ $json.tema }}"
  }
}
```

---

## ⚠️ **IMPORTANTE**

1. **Headers**: Sempre inclua `Content-Type: application/json` em POST/PUT
2. **Webhook Secret**: Use `X-Webhook-Secret` quando configurado
3. **Delay**: Recomendado 3-5 segundos entre mensagens
4. **Rate Limits**: Respeite os limites configurados por instância

---

**Todos os endpoints estão prontos para uso no n8n! 🚀**

