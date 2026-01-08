# ✅ Validação da Saída do n8n

## 📋 Análise da Saída Recebida

### ✅ Estrutura Geral: **CORRETA**

A saída está em formato de array com objeto contendo "output", que é normal no n8n quando a IA retorna JSON formatado.

### ✅ Campo `text`: **CORRETO**

- ✅ **Começa com data formatada**: `📅 Quinta-feira, 8 de janeiro de 2026`
- ✅ **NÃO tem saudação com nome**: Perfeito! O sistema adicionará automaticamente
- ✅ **Estrutura completa presente**:
  - Data formatada ✅
  - Título com emoji ✅
  - Versículo Principal ✅
  - Versículo de Apoio ✅
  - Reflexão (💬) ✅
  - Aplicação (🌱) ✅
  - Oração (🙏) ✅
  - Despedida e assinatura ✅

### ✅ Campo `title`: **CORRETO**
- "O Reflexo de Cristo em Nós" - Sem emoji, perfeito!

### ✅ Campo `date`: **CORRETO**
- "2026-01-08" - Formato ISO correto

### ✅ Versículos: **CORRETOS**
- Versículo Principal: Mateus 5:16 ACF ✅
- Versículo de Apoio: Colossenses 3:17 ACF ✅
- Ambos com texto completo e referência ✅

### ✅ Metadados: **CORRETOS**
- Autor: "Alex e Daniela Mantovani" ✅
- Tema: Relacionado a "Expressar" ✅
- Conceito central: Presente ✅
- Palavras-chave: Array válido ✅
- Relacionado_expressar: Explicação presente ✅

## ⚠️ Observação Importante

A saída está dentro de markdown code blocks:
```json
{
  "output": "```json\n{...}\n```"
}
```

**Isso é normal no n8n**, mas você precisa **extrair o JSON** antes de enviar ao webhook.

## 🔧 Como Processar no n8n

### Opção 1: Usar nó "Code" para extrair JSON (CORRIGIDO)

```javascript
// No nó Code do n8n
const output = $input.item.json.output;

// Remover prefixo "json\n" se existir (corrigido!)
let jsonString = output.replace(/^json\n?/i, '');

// Remover markdown code blocks se existirem
jsonString = jsonString
  .replace(/^```json\n?/gi, '')
  .replace(/^```\n?/g, '')
  .replace(/```\n?$/g, '')
  .trim();

// Parse do JSON
const devocional = JSON.parse(jsonString);

return devocional;
```

**OU versão mais robusta:**

```javascript
const output = $input.item.json.output;

// Buscar JSON dentro da string (procura por { ... })
const jsonMatch = output.match(/\{[\s\S]*\}/);

if (!jsonMatch) {
  throw new Error('JSON não encontrado na string');
}

// Parse do JSON encontrado
return JSON.parse(jsonMatch[0]);
```

### Opção 2: Usar Expressão no n8n

Se a IA retornar direto como JSON (sem code blocks), use:
```
{{ $json.output }}
```

Ou se estiver dentro de um objeto:
```
{{ JSON.parse($json.output.replace(/```json\n?/g, '').replace(/```\n?/g, '')) }}
```

### Opção 3: Configurar IA para retornar JSON puro

No prompt, adicione no final:
```
IMPORTANTE: Retorne APENAS o JSON válido, SEM markdown code blocks, SEM texto adicional antes ou depois.
```

## ✅ Checklist Final

- [x] Texto começa com data (sem saudação)
- [x] Estrutura completa presente
- [x] Dois versículos com referências ACF
- [x] Metadados completos
- [x] JSON válido
- [ ] Extrair JSON do code block antes de enviar ao webhook

## 🎯 Próximo Passo

Após extrair o JSON, envie para:
```
POST /api/devocional/webhook
Body: {{ $json }} (JSON extraído)
```

---

**Validação: ✅ APROVADO!**

Apenas certifique-se de extrair o JSON do code block antes de enviar ao webhook.
