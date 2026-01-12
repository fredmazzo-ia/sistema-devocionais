# 🔧 Código para Extrair JSON da Saída da IA

## Problema

A IA está retornando a saída dentro de uma estrutura como:
```json
{
  "output": {
    "text": "...",
    "title": "...",
    ...
  }
}
```

Ou com "output parser":
```
output: {...}
```

## ✅ Solução: Nó Code no n8n

Adicione um nó **Code** entre "Gerar Devocional" e "Enviar Webhook".

### Configuração do Nó Code

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
return {
  json: output
};
```

## 🔄 Fluxo Completo

```
1. Gerar Devocional (IA)
   ↓
2. Extrair JSON (Code) ← ADICIONE ESTE NÓ!
   ↓
3. Enviar Webhook (HTTP Request)
```

## ✅ Versão Simplificada (Se a IA retorna JSON direto)

Se a IA já retorna JSON limpo, use este código mais simples:

```javascript
// Extrair JSON do output
let output = $input.item.json.output || $input.item.json.text || $input.item.json;

// Se for string, fazer parse
if (typeof output === 'string') {
  // Remover markdown code blocks
  output = output
    .replace(/^```json\n?/gi, '')
    .replace(/^```\n?/g, '')
    .replace(/```\n?$/g, '')
    .trim();
  
  // Buscar JSON
  const jsonMatch = output.match(/\{[\s\S]*\}/);
  if (jsonMatch) {
    output = JSON.parse(jsonMatch[0]);
  }
}

return output;
```

## 🧪 Teste

Após adicionar o nó Code:

1. Execute o workflow
2. Verifique o output do nó Code
3. Deve mostrar o JSON limpo:
   ```json
   {
     "text": "...",
     "title": "...",
     "date": "...",
     ...
   }
   ```

---

**Adicione este nó Code entre a IA e o Webhook!** 🔧
