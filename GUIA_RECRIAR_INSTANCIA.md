# 🔄 Guia: Recriar Instância Evolution API

## 📋 Quando Recriar?

Recrie a instância se:
- ✅ Estado sempre aparece como "unknown" mesmo estando conectada
- ✅ QR Code não funciona
- ✅ Instância não é reconhecida pelo sistema
- ✅ Erros persistentes de conexão

## 🗑️ Passo 1: Excluir Instância Antiga

### No Evolution API Manager:

1. Acesse: `https://imobmiq-evolution-api.90qhxz.easypanel.host`
2. Vá em **Instances**
3. Encontre a instância **"Devocional-1"**
4. Clique no botão **"Delete"** (vermelho)
5. Confirme a exclusão

## ➕ Passo 2: Criar Nova Instância

### Opção A: Via Evolution API Manager (Recomendado)

1. No Evolution API Manager, clique em **"Instance+"** (botão verde)
2. Preencha:
   - **Instance Name**: `Devocional-1` (ou o nome que preferir)
   - **Integration**: `WHATSAPP-BAILEYS`
   - **QR Code**: Marque para gerar QR code
3. Clique em **Criar**
4. **Escaneie o QR Code** com o WhatsApp
5. Aguarde conectar (status deve ficar "Connected" ou "open")

### Opção B: Via API (Alternativa)

```bash
curl -X POST https://imobmiq-evolution-api.90qhxz.easypanel.host/instance/create \
  -H "apikey: 429683C4C977415CAAFCCE10F7D57E11" \
  -H "Content-Type: application/json" \
  -d '{
    "instanceName": "Devocional-1",
    "qrcode": true,
    "integration": "WHATSAPP-BAILEYS"
  }'
```

## ✅ Passo 3: Verificar Conexão

### No Evolution API Manager:
- Status deve aparecer como **"Connected"** (verde)
- Deve mostrar o número de telefone
- Deve mostrar estatísticas (usuários, mensagens)

### Via API:
```bash
curl https://imobmiq-evolution-api.90qhxz.easypanel.host/instance/fetchInstances \
  -H "apikey: 429683C4C977415CAAFCCE10F7D57E11"
```

Procure por `"instanceName": "Devocional-1"` e verifique o `"state"`.

## 🔧 Passo 4: Atualizar .env (se necessário)

Se você mudou o nome da instância, atualize o `.env` no EasyPanel:

```env
EVOLUTION_INSTANCES=[{"name":"Devocional-1","api_url":"https://imobmiq-evolution-api.90qhxz.easypanel.host","api_key":"429683C4C977415CAAFCCE10F7D57E11","display_name":"Devocional Diário","max_messages_per_hour":20,"max_messages_per_day":200,"priority":1,"enabled":true}]
```

**⚠️ IMPORTANTE**: O nome em `"name"` deve bater EXATAMENTE com o nome da instância no Evolution API Manager.

## 🚀 Passo 5: Fazer Deploy

1. Após atualizar o `.env`, faça **redeploy** no EasyPanel
2. Aguarde o sistema reiniciar
3. Verifique os logs - deve aparecer:
   ```
   ✅ Instância 'Devocional-1' encontrada na API como 'Devocional-1' (match: exata, estado: open)
   ✅ Instância Devocional-1 marcada como ACTIVE (estado: open)
   ```

## 🧪 Passo 6: Testar

1. **No Frontend**: Vá em "Instâncias"
   - Deve aparecer como **"Ativa"** (verde)
   - Deve mostrar o número de telefone
   - Botão "Verificar" deve confirmar conexão

2. **Teste de Envio**:
   - Vá em "Envios"
   - Envie uma mensagem de teste
   - Deve funcionar sem erros

## 🐛 Se Ainda Não Funcionar

### Verificar Logs:
```bash
# No EasyPanel, veja os logs do backend
# Procure por:
- "Instância 'Devocional-1' encontrada"
- "estado: open" ou "estado: connected"
- Qualquer erro relacionado
```

### Verificar Nome:
```bash
# Teste manual da API
curl https://imobmiq-evolution-api.90qhxz.easypanel.host/instance/fetchInstances \
  -H "apikey: 429683C4C977415CAAFCCE10F7D57E11" | grep -i devocional
```

### Verificar API Key:
- Certifique-se de que a API Key está correta
- Use a API Key principal do Manager (não o token da instância)

## 💡 Dicas

1. **Nome Consistente**: Use sempre o mesmo nome em todos os lugares
2. **Aguardar Conexão**: Após escanear QR code, aguarde alguns segundos para conectar
3. **Verificar Status**: Sempre verifique o status no Evolution API Manager antes de testar
4. **Logs Detalhados**: O sistema agora mostra logs muito detalhados - use-os para debug

## ✅ Checklist Final

- [ ] Instância excluída no Evolution API Manager
- [ ] Nova instância criada
- [ ] QR Code escaneado e conectado
- [ ] Status mostra "Connected" no Manager
- [ ] .env atualizado (se necessário)
- [ ] Deploy feito no EasyPanel
- [ ] Logs mostram instância como ACTIVE
- [ ] Teste de envio funcionando

---

**Após recriar, o sistema deve reconhecer automaticamente!** 🎉
