# 📋 Resumo: Prompt Melhorado + Estrutura PostgreSQL

## ✅ O que foi criado:

### 1. **Prompt Melhorado para n8n** (`PROMPT_MELHORADO_N8N.md`)
   - Versão completa com JSON estruturado
   - Versão simplificada (apenas texto)
   - Extrai metadados (versículos, tema, palavras-chave)
   - Validação de tamanho e formato

### 2. **Schema PostgreSQL Completo** (`database/devocionais_schema.sql`)
   - Tabela `devocionais` com campos estruturados
   - Tabela `devocional_contatos` 
   - Tabela `devocional_envios` (histórico)
   - Views úteis (`devocional_hoje`, `devocional_stats`)
   - Funções auxiliares
   - Índices otimizados
   - Full-text search em português

### 3. **Queries Úteis** (`database/example_queries.sql`)
   - 15 queries prontas para uso
   - Estatísticas, buscas, relatórios

## 🚀 Como Usar:

### Passo 1: Criar Banco de Dados

```bash
# Conecte no PostgreSQL e execute:
psql -U postgres -d seu_banco < database/devocionais_schema.sql
```

### Passo 2: Configurar n8n

Use o prompt do arquivo `PROMPT_MELHORADO_N8N.md`:

**Opção A - JSON Estruturado (Recomendado):**
- Retorna JSON com todos os campos
- Facilita armazenamento e busca

**Opção B - Apenas Texto:**
- Se a IA tiver dificuldade com JSON
- Sistema extrai informações do texto

### Passo 3: Configurar Webhook no n8n

Após gerar o devocional, envie para:

```
POST https://sua-api.com/api/devocional/webhook
Content-Type: application/json
X-Webhook-Secret: seu-secret

Body (se usar JSON estruturado):
{
  "text": "...",
  "title": "...",
  "date": "2026-01-07",
  "versiculo_principal": {
    "texto": "...",
    "referencia": "..."
  },
  "versiculo_apoio": {
    "texto": "...",
    "referencia": "..."
  },
  "metadata": {
    "autor": "Alex e Daniela Mantovani",
    "tema": "...",
    "palavras_chave": ["..."]
  }
}
```

### Passo 4: Sistema Salva Automaticamente

O sistema:
1. Recebe via webhook
2. Salva no PostgreSQL com todos os campos
3. Fica disponível para envio automático

## 📊 Estrutura da Tabela `devocionais`:

```sql
- id (SERIAL)
- title (VARCHAR) - Título sem emoji
- content (TEXT) - Texto completo formatado
- date (DATE) - Data do devocional
- versiculo_principal_texto (TEXT)
- versiculo_principal_referencia (VARCHAR)
- versiculo_apoio_texto (TEXT)
- versiculo_apoio_referencia (VARCHAR)
- source (VARCHAR) - 'n8n', 'api', 'manual'
- autor (VARCHAR)
- tema (VARCHAR)
- palavras_chave (TEXT[]) - Array
- sent (BOOLEAN) - Se foi enviado
- sent_at (TIMESTAMP)
- total_sent (INTEGER)
- metadata (JSONB) - Metadados extras
- created_at, updated_at (TIMESTAMP)
```

## 🔍 Queries Úteis:

```sql
-- Devocional de hoje
SELECT * FROM devocional_hoje;

-- Estatísticas
SELECT * FROM devocional_stats;

-- Contatos ativos
SELECT * FROM get_contatos_ativos();

-- Buscar por palavra-chave
SELECT * FROM devocionais 
WHERE 'guia' = ANY(palavras_chave);
```

## 🎯 Vantagens da Nova Estrutura:

1. **Versículos Separados**: Fácil buscar por versículo
2. **Metadados Estruturados**: Tema, palavras-chave, autor
3. **Full-Text Search**: Busca em português no conteúdo
4. **Performance**: Índices otimizados
5. **Histórico Completo**: Rastreamento de todos os envios
6. **Estatísticas**: Views prontas para relatórios

## 📝 Próximos Passos:

1. ✅ Execute o SQL no PostgreSQL
2. ✅ Atualize o prompt no n8n
3. ✅ Configure o webhook
4. ✅ Teste enviando um devocional
5. ✅ Verifique no banco: `SELECT * FROM devocionais;`

---

**Tudo pronto para uso!** 🚀
