# 🔧 Solução: Erro "Nenhuma instância disponível"

## 🐛 Problema Identificado

O erro mostra:
```
Nenhuma instância disponível
status: "blocked"
instance: null
```

Isso significa que o sistema não está encontrando instâncias configuradas ou elas não estão sendo marcadas como ACTIVE.

## ✅ Correções Aplicadas

1. **Health Check Melhorado**: Agora verifica instâncias automaticamente antes de usar
2. **Logs Detalhados**: Mostra exatamente qual instância não foi encontrada e por quê
3. **Fallback**: Tenta usar instâncias INACTIVE se não houver ACTIVE
4. **Endpoint de Debug**: Criado para diagnosticar problemas

## 🔍 Como Diagnosticar

### **1. Usar Endpoint de Debug**

Acesse:
```
GET https://sua-api.com/api/notifications/instances/debug
```

Isso retorna:
- Configuração carregada
- Status de cada instância
- Erros detalhados
- Lista de instâncias disponíveis no Evolution API

### **2. Verificar Logs**

Os logs agora mostram:
- Nome da instância procurada
- Instâncias disponíveis no Evolution API
- Erro específico (se houver)

## 🔧 Possíveis Causas e Soluções

### **Causa 1: Nome da Instância Não Bate**

**Sintoma**: Log mostra "Instância não encontrada. Disponíveis: [...]"

**Solução**: 
1. Verifique o nome exato da instância no Evolution API
2. Use o endpoint de debug para ver os nomes disponíveis
3. Atualize o `.env` com o nome correto

**Exemplo**:
```env
# Se no Evolution API aparece "Devocional" mas você configurou "Devocional-1"
EVOLUTION_INSTANCES=[{"name":"Devocional",...}]
```

### **Causa 2: API Key Incorreta**

**Sintoma**: Log mostra "HTTP 401" ou "HTTP 403"

**Solução**:
1. Verifique a API Key no `.env`
2. Use a API Key do Manager (a secreta)
3. Teste a API Key manualmente:
   ```bash
   curl https://imobmiq-evolution-api.90qhxz.easypanel.host/instance/fetchInstances \
     -H "apikey: SUA_API_KEY"
   ```

### **Causa 3: URL Incorreta**

**Sintoma**: Log mostra "Erro de conexão" ou timeout

**Solução**:
1. Verifique a URL no `.env`
2. Teste se a URL está acessível
3. Use a URL completa: `https://imobmiq-evolution-api.90qhxz.easypanel.host`

### **Causa 4: Instância Não Conectada**

**Sintoma**: Log mostra estado diferente de "open" ou "connected"

**Solução**:
1. Acesse o Evolution API Manager
2. Verifique se a instância está conectada (status "Connected")
3. Se não estiver, reconecte escaneando o QR Code

### **Causa 5: JSON Malformado no .env**

**Sintoma**: Log mostra "Erro ao carregar configuração de instâncias"

**Solução**:
1. Verifique se o JSON está em **uma única linha**
2. Valide o JSON em: https://jsonlint.com
3. Certifique-se de que não há quebras de linha no JSON

## 📝 Configuração Correta

### **Para 1 Instância (Devocional-1)**

```env
EVOLUTION_INSTANCES=[{"name":"Devocional-1","api_url":"https://imobmiq-evolution-api.90qhxz.easypanel.host","api_key":"SUA_API_KEY_AQUI","display_name":"Devocional Diário","max_messages_per_hour":20,"max_messages_per_day":200,"priority":1,"enabled":true}]
```

**Importante**:
- `name`: Deve ser **exatamente** como aparece no Evolution API
- `api_key`: Use a API Key do Manager
- `api_url`: URL completa do Evolution API
- Tudo em **uma linha**!

## 🧪 Teste Passo a Passo

### **1. Verificar Configuração**

```bash
GET /api/notifications/instances/debug
```

Veja:
- Se as instâncias foram carregadas
- Status de cada uma
- Erros específicos

### **2. Verificar Status**

```bash
GET /api/notifications/instances
```

Deve mostrar:
- Total de instâncias
- Instâncias ativas
- Status de cada uma

### **3. Testar Envio**

```bash
POST /api/notifications/webhook
Body: {
  "event": "send_test",
  "phone": "5516999999999",
  "message": "Teste"
}
```

## 🔍 Logs para Verificar

Procure nos logs por:
- `"Instância X não encontrada na lista"`
- `"Instâncias disponíveis: [...]"`
- `"Erro HTTP ao verificar"`
- `"Erro de conexão"`

Esses logs mostram exatamente qual é o problema!

---

**Use o endpoint `/api/notifications/instances/debug` para diagnosticar o problema!** 🔍

