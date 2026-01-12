# Workflow n8n Melhorado para Geração de Devocionais

## 🎯 Visão Geral

Workflow em 3 etapas que usa o histórico do banco de dados para gerar devocionais mais coerentes e progressivos.

## 📋 Estrutura do Workflow

```
1. Buscar Contexto Histórico
   ↓
2. Analisar e Gerar Direcionamento (IA)
   ↓
3. Gerar Devocional com Contexto (IA)
   ↓
4. Enviar para Webhook
```

## 🔧 Configuração no n8n

### Etapa 1: Buscar Contexto Histórico

**Nó: HTTP Request**

- **Method**: `GET`
- **URL**: `https://sua-api.com/api/devocional/context/para-ia?days=30`
- **Authentication**: Se necessário, adicione headers

**Saída esperada:**
```json
{
  "contexto_historico": "...",
  "versiculos_usados": ["Salmos 48:14", ...],
  "temas_abordados": ["tema1", ...],
  "direcionamento_sugerido": "...",
  "conceito_central": "..."
}
```

### Etapa 2: Analisar e Gerar Direcionamento (Opcional mas Recomendado)

**Nó: OpenAI / LangChain**

- **Model**: `gpt-4` ou `gpt-3.5-turbo`
- **Prompt**: Use o prompt de `PROMPT_ANALISE_HISTORICO.md`
- **Input**: 
  ```json
  {
    "historico": "{{ $json.contexto_historico }}",
    "versiculos_usados": "{{ $json.versiculos_usados }}",
    "temas_abordados": "{{ $json.temas_abordados }}"
  }
  ```

**Saída esperada:**
```json
{
  "sugestao": {
    "tema_sugerido": "...",
    "conceito_central": "...",
    "versiculos_sugeridos": ["...", "..."],
    "direcionamento": "...",
    "contexto_historico": "..."
  }
}
```

### Etapa 3: Gerar Devocional

**Nó: OpenAI / LangChain**

- **Model**: `gpt-4` ou `gpt-3.5-turbo`
- **Prompt**: 
  - Se houver contexto: Use `PROMPT_GERADOR_MELHORADO.md`
  - Se for primeiro devocional: Use `PROMPT_GERADOR_SEM_CONTEXTO.md`
- **Input**: Combine contexto histórico + direcionamento
- **IMPORTANTE**: O prompt NÃO deve incluir saudação com nome. O sistema adiciona automaticamente.
  ```json
  {
    "contexto_historico": "{{ $('Analisar').item.json.sugestao.contexto_historico }}",
    "direcionamento_sugerido": "{{ $('Analisar').item.json.sugestao.direcionamento }}",
    "conceito_central": "{{ $('Analisar').item.json.sugestao.conceito_central }}",
    "versiculos_usados": "{{ $('Buscar Contexto').item.json.versiculos_usados }}",
    "data": "{{ $now.setZone('America/Sao_Paulo').toFormat('cccc, dd/MM/yyyy') }}"
  }
  ```

**Saída esperada:**
```json
{
  "text": "📅 Quarta-feira, 10 de dezembro de 2025\n\n🌟 *Título*\n\n...",
  "title": "...",
  "date": "2026-01-07",
  "versiculo_principal": {...},
  "versiculo_apoio": {...},
  "metadata": {...}
}
```

**NOTA**: O campo `text` NÃO deve incluir "Bom dia, *Nome*". O sistema adiciona automaticamente baseado no horário e contato.

### Etapa 4: Enviar para Webhook

**Nó: HTTP Request**

- **Method**: `POST`
- **URL**: `https://sua-api.com/api/devocional/webhook`
- **Headers**:
  ```
  Content-Type: application/json
  X-Webhook-Secret: seu-secret-aqui
  ```
- **Body**: 
  ```json
  {
    "text": "{{ $json.text }}",
    "title": "{{ $json.title }}",
    "date": "{{ $json.date }}",
    "versiculo_principal": {
      "texto": "{{ $json.versiculo_principal.texto }}",
      "referencia": "{{ $json.versiculo_principal.referencia }}"
    },
    "versiculo_apoio": {
      "texto": "{{ $json.versiculo_apoio.texto }}",
      "referencia": "{{ $json.versiculo_apoio.referencia }}"
    },
    "metadata": {{ $json.metadata }}
  }
  ```

## 🎨 Versão Simplificada (Sem Análise Intermediária)

Se preferir pular a etapa de análise:

### Etapa 1: Buscar Contexto
(Mesmo da versão completa)

### Etapa 2: Gerar Devocional Diretamente

Use o prompt melhorado, mas injete diretamente o contexto:

```json
{
  "contexto_historico": "{{ $json.contexto_historico }}",
  "versiculos_usados": "{{ $json.versiculos_usados }}",
  "direcionamento_sugerido": "{{ $json.direcionamento_sugerido }}",
  "conceito_central": "{{ $json.conceito_central }}"
}
```

## 📊 Variáveis do n8n

Configure estas variáveis no n8n:

- `API_URL`: `https://sua-api.com`
- `WEBHOOK_SECRET`: `seu-secret`
- `DAYS_HISTORICO`: `30` (dias de histórico para buscar)

## 🔄 Fluxo Completo

1. **Trigger**: Agendado diariamente (ex: 05:00)
2. **Buscar Contexto**: Obtém histórico do banco
3. **Analisar** (opcional): IA analisa e sugere direcionamento
4. **Gerar**: IA cria devocional com contexto
5. **Enviar**: Salva no banco via webhook
6. **Scheduler**: Sistema envia automaticamente às 06:00

## 🎯 Vantagens

1. **Coerência**: Usa histórico real do banco
2. **Progressão**: Avança na jornada espiritual
3. **Sem Repetição**: Evita versículos já usados
4. **Tema Central**: Mantém foco em "Expressar"
5. **Evolução**: Jornada espiritual progressiva

## 🐛 Troubleshooting

### Contexto vazio
- Verifique se há devocionais no banco
- Ajuste o parâmetro `days` se necessário

### Versículos repetidos
- Verifique se a lista de versículos está sendo passada corretamente
- Confirme que a IA está usando a lista

### Tema desconexo
- Ajuste o prompt de análise
- Verifique se o direcionamento está sendo usado

## 📝 Exemplo de Prompt Completo para n8n

```
Você é um Pastor experiente criando devocionais diários.

CONTEXTO DA JORNADA:
{{ $json.contexto_historico }}

Versículos já utilizados (NÃO REPETIR):
{{ $json.versiculos_usados }}

Direcionamento de hoje:
{{ $json.direcionamento_sugerido }}

Conceito a trabalhar:
{{ $json.conceito_central }}

Data: {{ $now.setZone('America/Sao_Paulo').toFormat('cccc, dd/MM/yyyy') }}

Crie um devocional seguindo a estrutura completa e retorne em JSON conforme especificado no prompt principal.
```

---

**Sistema completo e integrado!** 🚀
