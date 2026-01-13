# 🔄 Workflow n8n Completo - Passo a Passo

## 🎯 Objetivo

Configurar workflow que:
1. Busca contexto histórico do banco
2. Analisa e sugere direcionamento (IA)
3. Gera devocional com contexto (IA)
4. Envia para webhook

## 📋 Estrutura do Workflow

```
1. Schedule Trigger (diário às 05:00)
   ↓
2. Buscar Contexto Histórico (HTTP Request)
   ↓
3. Analisar Histórico (IA - Opcional mas Recomendado)
   ↓
4. Gerar Devocional (IA)
   ↓
5. Extrair JSON (Code)
   ↓
6. Enviar para Webhook (HTTP Request)
```

## 🔧 Configuração Passo a Passo

### Passo 1: Schedule Trigger

**Nó: Schedule Trigger**

- **Trigger Times**: `05:00` (ou horário desejado)
- **Timezone**: `America/Sao_Paulo`

### Passo 2: Buscar Contexto Histórico

**Nó: HTTP Request**

- **Method**: `GET`
- **URL**: `https://imobmiq-devocional.90qhxz.easypanel.host/api/devocional/context/para-ia?days=30`
- **Authentication**: None

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

### Passo 3: Analisar Histórico (IA) - OPCIONAL mas RECOMENDADO

**Nó: OpenAI / LangChain**

- **Model**: `gpt-4` ou `gpt-3.5-turbo`
- **Temperature**: `0.7`
- **Max Tokens**: `1000`

**Prompt:**
```
Você é um especialista em análise de conteúdo devocional e jornadas espirituais.

Analise o histórico de devocionais fornecido e extraia:

1. **Temas já abordados**: Liste os principais temas/conceitos já trabalhados
2. **Versículos já usados**: Liste todas as referências bíblicas já utilizadas (para evitar repetição)
3. **Progressão temática**: Identifique a evolução do tema "Expressar" ao longo do tempo
4. **Palavras-chave recorrentes**: Identifique palavras/conceitos que aparecem frequentemente
5. **Gaps temáticos**: Sugira temas/conceitos relacionados a "Expressar" que ainda não foram explorados
6. **Próximo direcionamento**: Sugira o próximo passo na jornada espiritual, considerando:
   - O que já foi trabalhado
   - O que falta abordar
   - A progressão natural da fé
   - O tema central "Expressar"

## Histórico Fornecido:

Contexto: {{ $json.contexto_historico }}

Versículos já usados: {{ $json.versiculos_usados }}

Temas abordados: {{ $json.temas_abordados }}

## Formato de Saída (JSON):

Retorne APENAS um objeto JSON válido:

{
  "analise": {
    "temas_abordados": ["tema1", "tema2"],
    "versiculos_usados": ["referencia1", "referencia2"],
    "progressao": "Descrição da evolução temática",
    "palavras_chave": ["palavra1", "palavra2"]
  },
  "sugestao": {
    "tema_sugerido": "Tema para o próximo devocional",
    "conceito_central": "Conceito específico a ser trabalhado",
    "versiculos_sugeridos": ["referencia1", "referencia2"],
    "direcionamento": "Como este devocional deve avançar na jornada",
    "contexto_historico": "Resumo do que já foi trabalhado (máx 200 palavras)"
  }
}
```

**Input (se necessário):**
```json
{
  "historico": "{{ $json.contexto_historico }}",
  "versiculos": "{{ $json.versiculos_usados }}",
  "temas": "{{ $json.temas_abordados }}"
}
```

### Passo 4: Gerar Devocional (IA)

**Nó: OpenAI / LangChain**

- **Model**: `gpt-4` ou `gpt-3.5-turbo`
- **Temperature**: `0.8`
- **Max Tokens**: `2000`

**Prompt:**
```
Você é um Pastor experiente, cheio de unção e sabedoria, especializado em pregação bíblica poderosa, inspiradora e transformadora.

## CONTEXTO DA JORNADA:

{{ $('Analisar Histórico').item.json.sugestao.contexto_historico || $('Buscar Contexto').item.json.contexto_historico }}

**Tema Central da Série**: Expressar Jesus Cristo em nossa vida diária
**Direcionamento de Hoje**: {{ $('Analisar Histórico').item.json.sugestao.direcionamento || $('Buscar Contexto').item.json.direcionamento_sugerido }}
**Conceito a Trabalhar**: {{ $('Analisar Histórico').item.json.sugestao.conceito_central || $('Buscar Contexto').item.json.conceito_central }}

## SUA MISSÃO:

Criar UM devocional diário que:
1. Avança na jornada espiritual de forma coerente
2. Trabalha o conceito sugerido de forma natural e prática
3. Conecta com o tema "Expressar" sem repetição excessiva
4. Usa versículos INÉDITOS (não repetir: {{ $('Buscar Contexto').item.json.versiculos_usados }})
5. Mantém continuidade com devocionais anteriores

## ESTRUTURA DO DEVOCIONAL:

**IMPORTANTE**: NÃO inclua saudação personalizada com nome. O sistema adicionará automaticamente "Bom dia/Boa tarde/Boa noite, *[Nome]*" baseado no horário e contato.

### 1. Data Formatada
- "📅 [Dia da semana], [dia] de [mês] de [ano]\n\n"
- Exemplo: "📅 Quarta-feira, 10 de dezembro de 2025\n\n"
- Data de hoje: {{ $now.setZone('America/Sao_Paulo').toFormat('cccc, dd/MM/yyyy') }}

### 2. Título Inspirador
- "🌟 *[Título]*\n\n"
- Curto, conectado ao(s) versículo(s) e ao conceito do dia
- Relacionado ao tema "Expressar" de forma sutil

### 3. Versículos (DOIS, sempre inéditos)
- "📖 *Versículo Principal:*\n\"[versículo completo]\" ([referência] ACF)\n\n"
- "📖 *Versículo de Apoio:*\n\"[versículo completo]\" ([referência] ACF)\n\n"
- Ambos da Almeida Corrigida Fiel (ACF) - Português Brasil
- Devem se complementar e aprofundar o conceito
- NUNCA repetir versículos já usados: {{ $('Buscar Contexto').item.json.versiculos_usados }}

### 4. Reflexão (💬)
- 3-4 parágrafos bem estruturados
- Explique como os versículos se complementam
- Mostre como o conceito se aplica ao "Expressar Jesus"
- Seja prático, contextual e envolvente
- Conecte com a jornada espiritual em andamento
- Evite repetir frases ou ideias de devocionais anteriores

### 5. Aplicação Prática (🌱)
- "🌱 *Aplicação:*\n"
- Sugestão concreta e prática para o dia
- Relacionada ao conceito trabalhado
- Focada em como "Expressar" isso na vida

### 6. Oração (🙏)
- "🙏 *Oração:*\n"
- Curta, sincera, baseada na reflexão
- Relacionada ao conceito do dia

### 7. Despedida e Assinatura
- Despedida calorosa (varie)
- "Alex e Daniela Mantovani" (sem títulos)

## ESTILO E TOM:

- **Tom**: Cativante, afetuoso, inspirador, esperançoso, levemente bem humorado, simples e acolhedor
- **Linguagem**: Simples, compreensível, envolvente e única
- **Emojis**: Use apenas os especificados (📅 🌟 📖 💬 🌱 🙏)
- **Formatação**: 
  - Use *itálico* apenas em títulos de seções e palavras-chave importantes (máx 2-3 por parágrafo)
  - NUNCA use **negrito**
  - Quebras de linha: \n\n entre seções, \n em parágrafos longos

## REGRAS CRÍTICAS:

1. **Versículos ÚNICOS**: NUNCA repita versículos já usados
2. **Progressão Natural**: Avance na jornada, não repita conceitos recentes
3. **Tema "Expressar"**: Trabalhe de forma sutil, não repetitiva
4. **Continuidade**: Mantenha coerência com a jornada espiritual
5. **Originalidade**: Cada devocional deve trazer nova revelação
6. **Versão Bíblica**: Sempre ACF (Almeida Corrigida Fiel)
7. **Tamanho**: Máximo 4000 caracteres (WhatsApp permite 4096)
8. **Assinatura**: Apenas "Alex e Daniela Mantovani" (sem títulos)

## FORMATO DE SAÍDA (JSON):

Retorne APENAS um objeto JSON válido, SEM markdown code blocks:

{
  "text": "[texto completo formatado para WhatsApp, SEM saudação personalizada. Comece direto com a data formatada: 📅 ...]",
  "title": "[título sem emoji]",
  "date": "{{ $now.setZone('America/Sao_Paulo').toFormat('yyyy-MM-dd') }}",
  "versiculo_principal": {
    "texto": "[texto completo do versículo]",
    "referencia": "[referência bíblica] ACF"
  },
  "versiculo_apoio": {
    "texto": "[texto completo do versículo]",
    "referencia": "[referência bíblica] ACF"
  },
  "metadata": {
    "autor": "Alex e Daniela Mantovani",
    "tema": "[tema/conceito trabalhado]",
    "conceito_central": "[conceito específico do dia]",
    "palavras_chave": ["palavra1", "palavra2", "palavra3"],
    "relacionado_expressar": "[como se relaciona com Expressar]"
  }
}
```

### Passo 5: Extrair JSON (Code)

**Nó: Code**

**Language**: `JavaScript`

**Code:**
```javascript
// Extrair JSON do output da IA
let output = $input.item.json;

// Se tiver estrutura "output" ou "output parser"
if (output.output) {
  output = output.output;
}

// Se for string, tentar fazer parse
if (typeof output === 'string') {
  // Remover prefixos comuns
  let jsonString = output
    .replace(/^output\s*:\s*/i, '')
    .replace(/^json\n?/i, '')
    .trim();
  
  // Remover markdown code blocks se existirem
  jsonString = jsonString
    .replace(/^```json\n?/gi, '')
    .replace(/^```\n?/g, '')
    .replace(/```\n?$/g, '')
    .trim();
  
  // Buscar JSON dentro da string (procura por { ... })
  const jsonMatch = jsonString.match(/\{[\s\S]*\}/);
  
  if (jsonMatch) {
    try {
      output = JSON.parse(jsonMatch[0]);
    } catch (e) {
      throw new Error(`Erro ao fazer parse do JSON: ${e.message}`);
    }
  } else {
    throw new Error('JSON não encontrado na string');
  }
}

// Verificar se tem a estrutura esperada
if (!output.text && !output.title) {
  // Tentar encontrar em sub-objetos
  if (output.data) {
    output = output.data;
  } else if (output.result) {
    output = output.result;
  } else if (output.content) {
    output = output.content;
  }
}

// Retornar o objeto limpo
return output;
```

### Passo 6: Enviar para Webhook

**Nó: HTTP Request**

- **Method**: `POST`
- **URL**: `https://imobmiq-devocional.90qhxz.easypanel.host/api/devocional/webhook`
- **Headers**:
  - `Content-Type`: `application/json`
  - `X-Webhook-Secret`: `Fs142779`
- **Body**:
  - **Send Body**: ✅ ON
  - **Body Content Type**: `JSON`
  - **Specify Body**: `Using JSON`
  - **JSON**: `{{ $json }}`

## 🎨 Versão Simplificada (Sem Análise Intermediária)

Se preferir pular a etapa de análise (Passo 3):

### Passo 3 Alternativo: Gerar Diretamente

Use o mesmo prompt do Passo 4, mas ajuste as variáveis:

```
{{ $('Buscar Contexto').item.json.contexto_historico }}
{{ $('Buscar Contexto').item.json.direcionamento_sugerido }}
{{ $('Buscar Contexto').item.json.conceito_central }}
{{ $('Buscar Contexto').item.json.versiculos_usados }}
```

## ✅ Checklist

- [ ] Schedule Trigger configurado
- [ ] HTTP Request para buscar contexto
- [ ] IA de análise configurada (opcional)
- [ ] IA de geração configurada
- [ ] Code para extrair JSON
- [ ] HTTP Request para webhook
- [ ] Headers configurados corretamente
- [ ] Teste completo do workflow

## 🧪 Testar Workflow

1. Execute manualmente o workflow
2. Verifique cada etapa
3. Confirme que o devocional foi salvo no banco
4. Verifique se está disponível para envio

---

**Workflow completo configurado!** 🚀
