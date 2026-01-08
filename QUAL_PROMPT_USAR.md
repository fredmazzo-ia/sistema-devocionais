# 📋 Qual Prompt Usar? - Guia Definitivo

## ✅ Resposta Rápida

**Você NÃO precisa mais do prompt de formatação!**

Use apenas:
- **`PROMPT_GERADOR_MELHORADO.md`** - Para devocionais com contexto histórico
- **`PROMPT_GERADOR_SEM_CONTEXTO.md`** - Para primeiros devocionais/testes

## 🔄 Comparação dos Prompts

### ❌ `PROMPT_MELHORADO_N8N.md` (NÃO USE MAIS)
- **Função**: Apenas formatação
- **Input**: Texto já gerado (precisa de outro prompt antes)
- **Output**: Texto formatado
- **Problema**: Ainda menciona saudação com nome (desatualizado)
- **Status**: ⚠️ **OBSOLETO** - Não use mais

### ✅ `PROMPT_GERADOR_MELHORADO.md` (USE ESTE)
- **Função**: Gera E formata tudo de uma vez
- **Input**: Contexto histórico + direcionamento
- **Output**: JSON completo com texto já formatado
- **Vantagem**: Tudo em um passo, já formatado
- **Status**: ✅ **ATIVO** - Use quando houver histórico

### ✅ `PROMPT_GERADOR_SEM_CONTEXTO.md` (USE PARA TESTES)
- **Função**: Gera E formata tudo de uma vez (sem contexto)
- **Input**: Apenas direcionamento básico
- **Output**: JSON completo com texto já formatado
- **Vantagem**: Para primeiros devocionais
- **Status**: ✅ **ATIVO** - Use para primeiros devocionais

## 🎯 Workflow Simplificado

### Antes (2 etapas):
```
1. Gerar conteúdo (prompt antigo)
   ↓
2. Formatar (PROMPT_MELHORADO_N8N.md)
   ↓
3. Enviar
```

### Agora (1 etapa):
```
1. Gerar conteúdo JÁ FORMATADO (PROMPT_GERADOR_MELHORADO.md)
   ↓
2. Enviar
```

## 📝 Como Usar no n8n

### Para Primeiros Devocionais:
```
Nó: OpenAI / LangChain
Prompt: PROMPT_GERADOR_SEM_CONTEXTO.md
Input: {
  "contexto_historico": "Esta é uma das primeiras mensagens...",
  "direcionamento_sugerido": "Inicie a jornada...",
  "conceito_central": "Expressar Jesus através da nossa caminhada diária"
}
```

### Para Devocionais com Contexto:
```
Nó 1: HTTP Request
GET /api/devocional/context/para-ia

Nó 2: OpenAI / LangChain
Prompt: PROMPT_GERADOR_MELHORADO.md
Input: {
  "contexto_historico": "{{ $json.contexto_historico }}",
  "direcionamento_sugerido": "{{ $json.direcionamento_sugerido }}",
  "conceito_central": "{{ $json.conceito_central }}",
  "versiculos_usados": "{{ $json.versiculos_usados }}"
}
```

## ✅ Checklist

- [ ] Remover `PROMPT_MELHORADO_N8N.md` do workflow
- [ ] Usar apenas `PROMPT_GERADOR_MELHORADO.md` ou `PROMPT_GERADOR_SEM_CONTEXTO.md`
- [ ] Verificar que o output já vem formatado
- [ ] Confirmar que não há saudação com nome no texto gerado

## 🎯 Resumo

| Prompt | Quando Usar | Status |
|--------|------------|--------|
| `PROMPT_MELHORADO_N8N.md` | ❌ Nunca mais | OBSOLETO |
| `PROMPT_GERADOR_MELHORADO.md` | ✅ Com histórico | ATIVO |
| `PROMPT_GERADOR_SEM_CONTEXTO.md` | ✅ Primeiros devocionais | ATIVO |

---

**Use apenas os prompts geradores! Eles já fazem tudo formatado!** 🚀
