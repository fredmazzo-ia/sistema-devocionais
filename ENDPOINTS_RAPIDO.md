# ⚡ Endpoints Rápidos - Resumo

## 🎯 **Endpoints Principais para n8n**

### **1. Enviar Devocional (Principal)**
```
POST https://sua-api.com/api/notifications/webhook
Headers:
  Content-Type: application/json
  X-Webhook-Secret: Fs142779
Body:
{
  "event": "send_devocional",
  "devocional_id": 1
}
```

### **2. Receber Devocional do n8n**
```
POST https://sua-api.com/api/devocional/webhook
Headers:
  Content-Type: application/json
  X-Webhook-Secret: Fs142779
Body:
{
  "text": "Texto do devocional...",
  "title": "Título",
  "date": "2024-01-15"
}
```

### **3. Buscar Contexto para IA**
```
GET https://sua-api.com/api/devocional/context/para-ia?days=30
```

### **4. Verificar Status**
```
GET https://sua-api.com/api/notifications/instances
```

### **5. Enviar Teste**
```
POST https://sua-api.com/api/notifications/webhook
Headers:
  Content-Type: application/json
  X-Webhook-Secret: Fs142779
Body:
{
  "event": "send_test",
  "phone": "5516999999999",
  "message": "Teste"
}
```

---

## 📋 **Todos os Endpoints**

Veja o arquivo `ENDPOINTS_API_N8N.md` para documentação completa!

---

## 📦 **Postman Collection**

Importe o arquivo `postman_collection.json` no Postman para testar todos os endpoints!

