# Sistema de Envio de Devocionais - Guia Completo

## 📋 Visão Geral

Sistema robusto e profissional para envio automático de devocionais via Evolution API, com proteções avançadas contra bloqueio do WhatsApp.

## 🛡️ Proteções Implementadas

### 1. **Validação de Payload**
- Valida telefone antes de enviar
- Verifica se mensagem não está vazia
- Limite de caracteres (4096)
- Garante que propriedade `text` está presente (resolve o erro que você estava tendo)

### 2. **Rate Limiting**
- **Delay entre mensagens**: 3-5 segundos (configurável)
- **Limite horário**: 15-25 mensagens/hora (configurável)
- **Limite diário**: 150-250 mensagens/dia (configurável)
- Contadores automáticos que resetam

### 3. **Retry Logic**
- Tentativas automáticas em caso de falha
- Backoff exponencial (aumenta delay a cada tentativa)
- Não tenta novamente se mensagem foi bloqueada

### 4. **Tratamento de Erros**
- Captura erros de conexão, timeout, HTTP
- Identifica bloqueios (403, 429)
- Logging detalhado de todos os erros
- Registra falhas no banco de dados

### 5. **Monitoramento**
- Estatísticas em tempo real
- Histórico de envios
- Status da instância Evolution API
- Controle de contatos ativos/inativos

## 🚀 Como Usar

### 1. Configuração Inicial

Crie um arquivo `.env` no diretório `backend/` com:

```env
EVOLUTION_API_URL=http://localhost:8080
EVOLUTION_API_KEY=sua_chave_api_aqui
EVOLUTION_INSTANCE_NAME=Devocional

# Rate Limiting (ajuste conforme necessário)
DELAY_BETWEEN_MESSAGES=3.0
MAX_MESSAGES_PER_HOUR=20
MAX_MESSAGES_PER_DAY=200

# Retry
MAX_RETRIES=3
RETRY_DELAY=5.0

# Horário de envio automático
DEVOCIONAL_SEND_TIME=06:00
```

### 2. Adicionar Contatos

#### Via API:

```bash
POST /api/devocional/contatos
{
  "phone": "5516996480805",
  "name": "Tadeu"
}
```

#### Via código (config.py):

```python
DEVOCIONAL_CONTACTS: List[Dict[str, str]] = [
    {"phone": "5516996480805", "name": "Tadeu"},
    {"phone": "5511999999999", "name": "Maria"},
]
```

### 3. Enviar Devocional

#### Envio Manual (via API):

```bash
POST /api/devocional/send
{
  "message": "Seu texto do devocional aqui...",
  "delay": 3.0  # opcional
}
```

#### Envio para um contato específico:

```bash
POST /api/devocional/send-single?phone=5516996480805&message=Seu texto&name=Tadeu
```

### 4. Envio Automático

O sistema envia automaticamente todos os dias no horário configurado (`DEVOCIONAL_SEND_TIME`).

**Importante**: Você precisa implementar a função `get_devocional_message()` em `devocional_scheduler.py` para obter o texto do devocional do dia.

Exemplo:

```python
def get_devocional_message() -> Optional[str]:
    # Buscar de uma API externa
    # Ou de um banco de dados
    # Ou de um arquivo
    response = requests.get("https://sua-api-de-devocionais.com/daily")
    return response.json().get("message")
```

## 📊 Endpoints da API

### Envio
- `POST /api/devocional/send` - Envia para todos os contatos ativos
- `POST /api/devocional/send-single` - Envia para um contato específico

### Contatos
- `GET /api/devocional/contatos` - Lista todos os contatos
- `POST /api/devocional/contatos` - Adiciona novo contato
- `PUT /api/devocional/contatos/{id}/toggle` - Ativa/desativa contato
- `DELETE /api/devocional/contatos/{id}` - Remove contato

### Monitoramento
- `GET /api/devocional/stats` - Estatísticas e status
- `GET /api/devocional/envios` - Histórico de envios

## 🔧 Configurações Recomendadas

### Para evitar bloqueio:

| Configuração | Valor Conservador | Valor Moderado | Valor Agressivo |
|-------------|------------------|----------------|-----------------|
| Delay entre mensagens | 5-10s | 3-5s | 2-3s |
| Máx. por hora | 15-20 | 20-25 | 25-30 |
| Máx. por dia | 150-200 | 200-250 | 250-300 |

**Recomendação inicial**: Use valores conservadores e vá ajustando conforme necessário.

### Sinais de que precisa reduzir:

- Erros 429 (Too Many Requests)
- Erros 403 (Forbidden)
- Mensagens não sendo entregues
- Avisos de spam no WhatsApp

## 🐛 Resolução de Problemas

### Erro: "instance requires property 'text'"

**Causa**: Payload malformado sem a propriedade `text`.

**Solução**: O sistema agora valida automaticamente antes de enviar. Se ainda ocorrer, verifique:
- Mensagem não está vazia
- Formato do payload está correto

### Número cai sistematicamente

**Possíveis causas**:
1. Envio muito rápido (reduza `DELAY_BETWEEN_MESSAGES`)
2. Muitas mensagens por hora (reduza `MAX_MESSAGES_PER_HOUR`)
3. Mensagens idênticas (varie o conteúdo)
4. Contatos não salvaram seu número

**Soluções**:
- Aumente os delays
- Reduza limites
- Adicione personalização (nome do destinatário)
- Peça para contatos salvarem seu número

### Mensagens não estão sendo enviadas

1. Verifique status da instância: `GET /api/devocional/stats`
2. Verifique logs do servidor
3. Confirme que contatos estão ativos
4. Verifique rate limits

## 📈 Melhores Práticas

1. **Comece conservador**: Use valores baixos inicialmente
2. **Monitore sempre**: Acompanhe estatísticas regularmente
3. **Varie conteúdo**: Não envie mensagens idênticas
4. **Personalize**: Use o nome do destinatário
5. **Horários**: Envie em horários de menor tráfego (manhã cedo)
6. **Teste primeiro**: Envie para poucos contatos antes de escalar
7. **Backup**: Mantenha backup da lista de contatos

## 🔄 Integração com sua Automação Atual

Se você já tem uma automação (como n8n), pode:

1. **Usar a API**: Chame os endpoints da API
2. **Manter sua automação**: Use apenas para gerar o texto do devocional
3. **Híbrido**: Sua automação gera o texto → API envia

Exemplo de integração:

```python
# Sua automação gera o texto
devocional_texto = sua_automacao.gerar_devocional()

# Chama a API para enviar
requests.post(
    "http://localhost:8000/api/devocional/send",
    json={"message": devocional_texto}
)
```

## 📝 Logs

Todos os envios são registrados no banco de dados:
- Status (sent, failed, blocked)
- Timestamp
- Erros (se houver)
- Número de tentativas

Acesse via: `GET /api/devocional/envios`

## 🎯 Próximos Passos

1. Configure suas credenciais da Evolution API
2. Adicione seus contatos
3. Ajuste rate limits conforme necessário
4. Implemente `get_devocional_message()` para obter devocionais
5. Teste com poucos contatos primeiro
6. Monitore estatísticas e ajuste

## ⚠️ Avisos Importantes

- **Nunca** envie mais de 30 mensagens/hora
- **Sempre** mantenha delay mínimo de 2-3 segundos
- **Monitore** bloqueios e ajuste imediatamente
- **Teste** antes de enviar para muitos contatos
- **Respeite** os limites do WhatsApp

---

**Desenvolvido com foco em segurança e estabilidade para evitar bloqueios do WhatsApp.**

