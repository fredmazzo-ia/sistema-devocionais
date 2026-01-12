# 🔄 Refatoração Completa do Sistema de Instâncias

## 📋 O que foi feito

### **Problema Anterior:**
- Instâncias configuradas no `.env` (EVOLUTION_INSTANCES)
- Instâncias criadas dinamicamente não apareciam
- Conflito entre `.env` e criação dinâmica
- Lógica duplicada e confusa
- Instâncias não sincronizavam corretamente

### **Solução Implementada:**
- ✅ **Banco de dados como fonte única de verdade**
- ✅ **Busca direta da Evolution API**
- ✅ **Sincronização automática**
- ✅ **Lógica unificada e organizada**

## 🏗️ Nova Arquitetura

### **1. Modelo de Banco de Dados**

Criado `EvolutionInstanceConfig` no banco de dados:

```python
class EvolutionInstanceConfig(Base):
    name: str                    # Nome da instância na Evolution API
    api_url: str                 # URL (vem do .env)
    api_key: str                 # API Key (vem do .env)
    display_name: str            # Nome que aparece no WhatsApp
    status: str                  # active, inactive, error, blocked
    phone_number: str            # Número (obtido da API)
    max_messages_per_hour: int
    max_messages_per_day: int
    priority: int
    enabled: bool
    # ... estatísticas e timestamps
```

### **2. InstanceService**

Novo serviço unificado (`instance_service.py`):

- **Busca instâncias diretamente da Evolution API**
- **Sincroniza com banco de dados automaticamente**
- **Cria/atualiza configurações no banco**
- **Uma única fonte de verdade**

### **3. Endpoints Refatorados**

Novo router `instances_v2.py`:

- `GET /api/instances/` - Lista todas (sincroniza automaticamente)
- `POST /api/instances/create` - Cria instância na Evolution API + banco
- `POST /api/instances/{name}/qr` - Gera QR code
- `POST /api/instances/{name}/connect` - Verifica conexão
- `POST /api/instances/{name}/refresh` - Atualiza status
- `PUT /api/instances/{name}` - Atualiza configuração
- `DELETE /api/instances/{name}` - Remove do banco

### **4. InstanceManager Atualizado**

Agora aceita banco de dados:

```python
# Antes (legado)
manager = InstanceManager(instances_config)

# Agora (preferido)
manager = InstanceManager(db=db)
```

## 🔧 Configuração no .env

### **O que MUDOU:**

**ANTES (complexo):**
```env
EVOLUTION_INSTANCES=[{"name":"Devocional-1","api_url":"...","api_key":"...",...}]
```

**AGORA (simples):**
```env
# Apenas URL e API Key (usadas para todas as instâncias)
EVOLUTION_API_URL=https://imobmiq-evolution-api.90qhxz.easypanel.host
EVOLUTION_API_KEY=429683C4C977415CAAFCCE10F7D57E11
```

### **O que NÃO precisa mais:**
- ❌ `EVOLUTION_INSTANCES` (removido)
- ❌ Configurar instâncias manualmente no `.env`
- ❌ Editar JSON complexo

### **O que ainda funciona:**
- ✅ `EVOLUTION_API_URL` (obrigatório)
- ✅ `EVOLUTION_API_KEY` (obrigatório)
- ✅ Outras configurações (rate limits, etc.)

## 🚀 Como Funciona Agora

### **1. Primeira Carga:**
1. Sistema busca todas as instâncias da Evolution API
2. Cria registros no banco de dados automaticamente
3. Sincroniza status e informações

### **2. Criar Nova Instância:**
1. Usuário clica em "Nova Instância"
2. Preenche nome e configurações
3. Sistema cria na Evolution API
4. Salva configuração no banco
5. Gera QR code automaticamente
6. **Aparece imediatamente na lista**

### **3. Sincronização Automática:**
- Toda vez que lista instâncias, sincroniza com Evolution API
- Atualiza status, número de telefone, etc.
- Mantém banco de dados atualizado

### **4. Envio de Mensagens:**
- InstanceManager busca instâncias do banco
- Usa apenas instâncias ativas e habilitadas
- Distribui mensagens entre instâncias

## 📊 Fluxo de Dados

```
Evolution API
    ↓ (busca)
InstanceService
    ↓ (sincroniza)
Banco de Dados (EvolutionInstanceConfig)
    ↓ (carrega)
InstanceManager
    ↓ (usa)
DevocionalServiceV2
    ↓ (envia)
WhatsApp
```

## ✅ Benefícios

1. **Simplicidade**: Não precisa mais editar `.env` complexo
2. **Dinâmico**: Instâncias aparecem automaticamente
3. **Unificado**: Uma única fonte de verdade (banco)
4. **Sincronizado**: Sempre atualizado com Evolution API
5. **Organizado**: Lógica clara e separada

## 🔄 Migração

### **Para Usuários Existentes:**

1. **Faça deploy** da nova versão
2. **O sistema criará a tabela** `evolution_instance_configs` automaticamente
3. **Na primeira carga**, todas as instâncias da Evolution API serão sincronizadas
4. **Remova** `EVOLUTION_INSTANCES` do `.env` (opcional, não quebra se deixar)

### **Para Novos Usuários:**

1. Configure apenas `EVOLUTION_API_URL` e `EVOLUTION_API_KEY` no `.env`
2. Crie instâncias pela interface
3. Pronto!

## 🐛 Resolução de Problemas

### **Instância não aparece:**
- Clique em "Sincronizar" para forçar sincronização
- Verifique se a instância existe na Evolution API
- Verifique logs do backend

### **Erro 500 ao verificar:**
- Verifique se `EVOLUTION_API_URL` e `EVOLUTION_API_KEY` estão corretos
- Verifique se a Evolution API está acessível
- Veja logs do backend para detalhes

### **Instância não conecta:**
- Gere QR code novamente
- Verifique se escaneou corretamente
- Aguarde alguns segundos após escanear

## 📝 Notas Técnicas

- **Backward Compatible**: Código legado ainda funciona (usa `.env` se db não fornecido)
- **Auto-migração**: Tabela criada automaticamente no primeiro uso
- **Performance**: Sincronização é rápida (apenas busca lista da API)
- **Segurança**: API Key não é exposta no frontend

---

**Sistema completamente refatorado e unificado!** 🎉
