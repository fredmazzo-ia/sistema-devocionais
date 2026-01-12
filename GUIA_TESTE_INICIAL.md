# 🧪 Guia de Teste Inicial - Geração de Devocionais

## 📋 Objetivo

Testar a geração de devocionais sem contexto histórico (primeiros devocionais).

## 🎯 Passo a Passo

### 1. Testar Endpoint de Contexto Vazio

```bash
GET /api/devocional/test/contexto-vazio
```

**Resposta esperada:**
```json
{
  "contexto_historico": "Esta é uma das primeiras mensagens da série...",
  "versiculos_usados": [],
  "temas_abordados": [],
  "direcionamento_sugerido": "Inicie a jornada...",
  "conceito_central": "Expressar Jesus através da nossa caminhada diária"
}
```

### 2. Testar Personalização de Mensagem

```bash
GET /api/devocional/test/personalizacao?nome=Tadeu
```

**Resposta esperada:**
```json
{
  "original": "📅 Quarta-feira...",
  "personalizada": "Bom dia, *Tadeu*\n\n📅 Quarta-feira...",
  "nome_usado": "Tadeu",
  "saudacao": "Bom dia",
  "diferenca": {
    "tamanho_original": 500,
    "tamanho_personalizada": 520,
    "adicionado": 20
  }
}
```

### 3. Configurar n8n para Primeiro Devocional

#### Opção A: Usar Endpoint de Teste

**Nó 1: HTTP Request**
```
GET https://sua-api.com/api/devocional/test/contexto-vazio
```

**Nó 2: OpenAI / LangChain**
- **Prompt**: Use `PROMPT_GERADOR_SEM_CONTEXTO.md`
- **Input**: 
  ```json
  {
    "contexto_historico": "{{ $json.contexto_historico }}",
    "direcionamento_sugerido": "{{ $json.direcionamento_sugerido }}",
    "conceito_central": "{{ $json.conceito_central }}"
  }
  ```

**Nó 3: HTTP Request (Webhook)**
```
POST https://sua-api.com/api/devocional/webhook
Body: {{ $json }}
```

#### Opção B: Hardcode Contexto Vazio

**Nó: OpenAI / LangChain**
- **Prompt**: Use `PROMPT_GERADOR_SEM_CONTEXTO.md`
- **Input**: 
  ```json
  {
    "contexto_historico": "Esta é uma das primeiras mensagens da série. O tema central é 'Expressar Jesus Cristo' em nossa vida diária.",
    "direcionamento_sugerido": "Inicie a jornada apresentando como podemos expressar Jesus em nosso dia a dia, focando em aspectos práticos e transformadores.",
    "conceito_central": "Expressar Jesus através da nossa caminhada diária"
  }
  ```

### 4. Validar Formato do Devocional Gerado

O JSON retornado deve ter:

```json
{
  "text": "📅 [data]\n\n🌟 *Título*\n\n...",
  "title": "Título sem emoji",
  "date": "2026-01-07",
  "versiculo_principal": {
    "texto": "...",
    "referencia": "... ACF"
  },
  "versiculo_apoio": {
    "texto": "...",
    "referencia": "... ACF"
  },
  "metadata": {
    "autor": "Alex e Daniela Mantovani",
    "tema": "...",
    "conceito_central": "...",
    "palavras_chave": [...],
    "relacionado_expressar": "..."
  }
}
```

**✅ Checklist:**
- [ ] Campo `text` NÃO contém "Bom dia, *Nome*"
- [ ] Campo `text` começa com "📅 [data]"
- [ ] Dois versículos presentes
- [ ] Estrutura completa (título, versículos, reflexão, aplicação, oração)
- [ ] Assinatura: "Alex e Daniela Mantovani"

### 5. Testar Personalização no Envio

Após salvar no banco, teste o envio:

```bash
POST /api/devocional/send-single?phone=5516996480805&message=[texto_do_devocional]&name=Tadeu
```

**Verificar:**
- Mensagem recebida começa com "Bom dia, *Tadeu*" (ou "Boa tarde"/"Boa noite" conforme horário)
- Resto da mensagem está intacto
- Formatação preservada

## 🔄 Fluxo Completo de Teste

```
1. Gerar Primeiro Devocional
   ↓
2. Salvar via Webhook
   ↓
3. Verificar no Banco
   SELECT * FROM devocionais ORDER BY created_at DESC LIMIT 1;
   ↓
4. Testar Envio Personalizado
   POST /api/devocional/send-single
   ↓
5. Validar Mensagem Recebida
   - Saudação correta (Bom dia/tarde/noite)
   - Nome personalizado
   - Conteúdo completo
```

## 📝 Gerar Múltiplos Devocionais para Teste

Para criar contexto histórico:

1. **Gere 3-5 devocionais** usando `PROMPT_GERADOR_SEM_CONTEXTO.md`
2. **Salve todos** via webhook
3. **Verifique contexto:**
   ```bash
   GET /api/devocional/context/para-ia?days=30
   ```
4. **Gere próximo devocional** usando `PROMPT_GERADOR_MELHORADO.md` com contexto

## 🎯 Validações Importantes

### ✅ Formato Correto:
- Texto SEM saudação personalizada
- Começa com data formatada
- Estrutura completa presente
- JSON válido

### ❌ Erros Comuns:
- Incluir "Bom dia, *Nome*" no texto gerado
- Esquecer versículos
- Formato JSON inválido
- Tamanho excedendo 4000 caracteres

## 🚀 Próximos Passos Após Validação

1. ✅ Validar geração sem contexto
2. ✅ Validar personalização automática
3. ✅ Gerar 3-5 devocionais para criar histórico
4. ✅ Testar geração COM contexto
5. ✅ Validar progressão temática
6. ✅ Configurar envio automático

---

**Sistema pronto para testes!** 🧪
