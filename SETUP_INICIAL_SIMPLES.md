# 🚀 Setup Inicial - Sem Terminal!

## ✅ Método Mais Simples (Recomendado)

### **Via Interface Web (Postman ou Navegador)**

Após o deploy no EasyPanel, acesse a URL do seu sistema e use o endpoint de setup:

**URL:** `https://imobmiq-devocional.90qhxz.easypanel.host/api/auth/setup-initial-admin`

**Método:** `POST`

**Body (JSON):**
```json
{
  "email": "fredmazzo@gmail.com",
  "password": "admin123",
  "name": "Administrador"
}
```

---

## 📋 Passo a Passo

### **1. Via Postman ou Insomnia**

1. Abra Postman/Insomnia
2. Crie nova requisição POST
3. URL: `https://imobmiq-devocional.90qhxz.easypanel.host/api/auth/setup-initial-admin`
4. Headers: `Content-Type: application/json`
5. Body (raw JSON):
   ```json
   {
     "email": "fredmazzo@gmail.com",
     "password": "admin123",
     "name": "Administrador"
   }
   ```
6. Envie a requisição

### **2. Via cURL (se tiver acesso)**

```bash
curl -X POST https://imobmiq-devocional.90qhxz.easypanel.host/api/auth/setup-initial-admin \
  -H "Content-Type: application/json" \
  -d '{
    "email": "fredmazzo@gmail.com",
    "password": "admin123",
    "name": "Administrador"
  }'
```

### **3. Via JavaScript no Navegador**

Abra o console do navegador (F12) e execute:

```javascript
fetch('https://imobmiq-devocional.90qhxz.easypanel.host/api/auth/setup-initial-admin', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'fredmazzo@gmail.com',
    password: 'admin123',
    name: 'Administrador'
  })
})
.then(res => res.json())
.then(data => console.log('✅ Sucesso:', data))
.catch(err => console.error('❌ Erro:', err));
```

---

## ✅ Verificação

Após executar, você receberá uma resposta como:

```json
{
  "id": 1,
  "email": "fredmazzo@gmail.com",
  "name": "Administrador",
  "is_admin": true,
  "message": "Usuário administrador criado com sucesso! Agora você pode fazer login."
}
```

Agora você pode fazer login na interface web com:
- **Email:** `fredmazzo@gmail.com`
- **Senha:** `admin123`

---

## 🔒 Segurança

⚠️ **IMPORTANTE:**
- Este endpoint **só funciona se não houver nenhum admin** no sistema
- Após criar o primeiro admin, este endpoint será bloqueado
- Use `/api/auth/create-user` (com autenticação) para criar mais usuários

---

## 🎯 Próximos Passos

1. ✅ Criar usuário admin (via endpoint acima)
2. ✅ Fazer login na interface web
3. ✅ Alterar senha padrão
4. ✅ Começar a usar o sistema!

---

**Pronto! Sem precisar de terminal!** 🎉

