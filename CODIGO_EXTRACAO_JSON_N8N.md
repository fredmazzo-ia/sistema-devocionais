# 🔧 Código Corrigido para Extração de JSON no n8n

## ❌ Problema Identificado

A string começa com `json\n` literalmente, não com backticks markdown. O código atual não remove esse prefixo.

**Input atual:**
```
json\n {\n "text": "Quinta-feira...
```

## ✅ Código Corrigido

Use este código no nó **Code** do n8n:

```javascript
// Extrair JSON do output
const output = $input.item.json.output;

// Remover prefixo "json\n" se existir
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

## 🎯 Versão Mais Robusta (Recomendada)

Esta versão trata vários casos:

```javascript
// Extrair JSON do output
const output = $input.item.json.output;

let jsonString = output;

// Remover prefixo "json\n" ou "json" (case insensitive)
jsonString = jsonString.replace(/^json\n?/i, '');

// Remover markdown code blocks (várias variações)
jsonString = jsonString
  .replace(/^```json\n?/gi, '')      // Remove ```json no início
  .replace(/^```\n?/g, '')           // Remove ``` no início
  .replace(/```\n?$/g, '')            // Remove ``` no final
  .replace(/^`/g, '')                 // Remove ` solto no início
  .replace(/`$/g, '')                 // Remove ` solto no final
  .trim();

// Parse do JSON
try {
  const devocional = JSON.parse(jsonString);
  return devocional;
} catch (error) {
  // Se falhar, tenta encontrar JSON dentro da string
  const jsonMatch = jsonString.match(/\{[\s\S]*\}/);
  if (jsonMatch) {
    return JSON.parse(jsonMatch[0]);
  }
  throw new Error(`Erro ao parsear JSON: ${error.message}. String: ${jsonString.substring(0, 100)}...`);
}
```

## 🔍 Versão Simplificada (Se a anterior não funcionar)

Se ainda tiver problemas, use esta versão que busca o JSON dentro da string:

```javascript
const output = $input.item.json.output;

// Buscar o JSON dentro da string (procura por { ... })
const jsonMatch = output.match(/\{[\s\S]*\}/);

if (!jsonMatch) {
  throw new Error('JSON não encontrado na string');
}

// Parse do JSON encontrado
const devocional = JSON.parse(jsonMatch[0]);

return devocional;
```

## ✅ Teste Rápido

Para testar, adicione um nó de log após o Code:

```javascript
// No nó Code, retorne também informações de debug
return {
  ...devocional,
  _debug: {
    original_length: output.length,
    cleaned_length: jsonString.length,
    first_chars: jsonString.substring(0, 50)
  }
};
```

## 🎯 Solução Mais Simples (Recomendada)

Se a IA sempre retorna no mesmo formato, use esta versão específica:

```javascript
const output = $input.item.json.output;

// Remove "json\n" do início
let jsonString = output.replace(/^json\n?/i, '').trim();

// Parse
return JSON.parse(jsonString);
```

---

**Use a versão mais robusta para garantir que funcione em todos os casos!**
