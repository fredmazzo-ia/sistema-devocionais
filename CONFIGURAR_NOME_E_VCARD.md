# Como Configurar Nome e vCard Automático

## Problema
Quando você envia mensagens, o destinatário pode ver apenas o número ao invés de "Devocional Diário", e o contato não é salvo automaticamente.

## Solução

### 1. Configurar o Nome do Perfil (Display Name)

O sistema agora configura automaticamente o nome do perfil na inicialização. Mas você pode configurar manualmente também:

#### Via API (Recomendado)
```bash
# Configurar perfil de uma instância específica
POST https://seu-dominio.com/api/notifications/instances/Devocional-1/setup-profile

# Configurar perfil de todas as instâncias
POST https://seu-dominio.com/api/notifications/instances/setup-all-profiles
```

#### Via n8n
Use um nó HTTP Request após iniciar o sistema:
- **URL**: `https://seu-dominio.com/api/notifications/instances/setup-all-profiles`
- **Method**: POST
- **Headers**: (nenhum necessário)

### 2. Ativar Envio Automático de vCard

Para que os contatos sejam salvos automaticamente quando receberem a primeira mensagem:

#### No arquivo `.env` (EasyPanel):
```env
# Enviar vCard automaticamente para novos contatos
SEND_VCARD_TO_NEW_CONTACTS=true

# Enviar mensagem pedindo para salvar contato (opcional)
SEND_CONTACT_REQUEST=false
```

#### O que cada opção faz:

- **`SEND_VCARD_TO_NEW_CONTACTS=true`**: 
  - Envia automaticamente um vCard (cartão de contato) para novos contatos
  - O vCard permite que o destinatário salve seu contato facilmente
  - Só envia no primeiro envio para cada contato

- **`SEND_CONTACT_REQUEST=false`**: 
  - Se `true`, envia uma mensagem de texto pedindo para salvar o contato
  - Geralmente não é necessário se o vCard estiver ativado

### 3. Verificar se Está Funcionando

#### Verificar status das instâncias:
```bash
GET https://seu-dominio.com/api/notifications/instances
```

#### Verificar debug completo:
```bash
GET https://seu-dominio.com/api/notifications/instances/debug
```

### 4. Como Funciona

1. **Na inicialização**: O sistema tenta configurar o perfil de todas as instâncias automaticamente
2. **Ao enviar mensagem**: Se `SEND_VCARD_TO_NEW_CONTACTS=true` e é o primeiro envio para aquele contato, o vCard é enviado automaticamente
3. **Obtenção do número**: O sistema tenta obter o número da instância automaticamente via health check

### 5. Troubleshooting

#### Nome não aparece mesmo após configurar:
- Verifique se a instância está conectada no Evolution API Manager
- Tente configurar manualmente via API: `POST /api/notifications/instances/{nome}/setup-profile`
- Verifique os logs para erros

#### vCard não está sendo enviado:
- Verifique se `SEND_VCARD_TO_NEW_CONTACTS=true` no `.env`
- Reinicie o aplicativo após alterar o `.env`
- Verifique se é realmente o primeiro envio para aquele contato
- Verifique os logs para mensagens de erro

#### Estado "unknown" na instância:
- Isso é normal! O sistema funciona mesmo com estado "unknown"
- Se a mensagem foi enviada com sucesso, a instância será marcada como ACTIVE automaticamente
- O health check pode não conseguir determinar o estado, mas isso não impede o envio

### 6. Exemplo de Configuração Completa no `.env`

```env
# Multi-Instância Evolution API
EVOLUTION_INSTANCES=[{"name":"Devocional-1","api_url":"https://seu-evolution-api.com","api_key":"sua-key","display_name":"Devocional Diário","max_messages_per_hour":20,"max_messages_per_day":200,"priority":1,"enabled":true}]

EVOLUTION_DISPLAY_NAME=Devocional Diário
EVOLUTION_INSTANCE_STRATEGY=round_robin

# Ativar vCard automático
SEND_VCARD_TO_NEW_CONTACTS=true
SEND_CONTACT_REQUEST=false
```

### 7. Teste Rápido

1. Configure o `.env` com `SEND_VCARD_TO_NEW_CONTACTS=true`
2. Reinicie o aplicativo
3. Configure o perfil: `POST /api/notifications/instances/setup-all-profiles`
4. Envie uma mensagem de teste para um número novo
5. Verifique se o vCard foi enviado e se o nome aparece

## Notas Importantes

- O nome do perfil precisa ser configurado **após** a instância estar conectada no WhatsApp
- O vCard só é enviado para contatos que ainda não receberam nenhuma mensagem (total_sent == 0)
- O número da instância é obtido automaticamente, mas pode levar alguns segundos na primeira vez
- Se o número não estiver disponível, o vCard será enviado na próxima vez que o health check conseguir obtê-lo

