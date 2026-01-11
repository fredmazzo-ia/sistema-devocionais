# 👤 Como Criar Usuário Admin - Passo a Passo

## 🚀 Método Mais Simples (SEM TERMINAL!)

### **Via HTTP (Postman, Insomnia ou Navegador)**

Após o deploy no EasyPanel, use este endpoint:

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

**⚠️ IMPORTANTE:** Este endpoint só funciona se não houver nenhum admin no sistema!

---

## 📋 Como Usar

### **Opção 1: Postman/Insomnia (Recomendado)**

1. Abra Postman ou Insomnia
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

### **Opção 2: JavaScript no Navegador**

Abra o console do navegador (F12) e execute:

```javascript
fetch('https://imobmiq-devocional.90qhxz.easypanel.host/api/auth/setup-initial-admin', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
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

## 🔧 Método Alternativo (Terminal - Apenas se necessário)

Se o endpoint HTTP não funcionar, use o terminal do EasyPanel:

```bash
cd /app
python database/create_admin_user_auto.py
```

---

## 📝 Método Interativo

Execute e preencha os dados:

```bash
cd /app
python database/create_admin_user.py
```

Siga as instruções na tela.

---

## 🗄️ Via SQL (Alternativo)

Se preferir criar diretamente no banco:

```sql
-- Hash da senha "admin123" (bcrypt)
-- Você pode gerar um novo hash executando em Python:
-- from app.auth import get_password_hash
-- print(get_password_hash("sua-senha"))

INSERT INTO users (email, name, hashed_password, is_admin, is_active)
VALUES (
  'fredmazzo@gmail.com',
  'Administrador',
  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJ5q5q5q5q',  -- admin123
  true,
  true
);
```

---

## ✅ Verificar se Funcionou

Teste o login via API:

```bash
curl -X POST https://imobmiq-devocional.90qhxz.easypanel.host/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "fredmazzo@gmail.com",
    "password": "admin123"
  }'
```

Se retornar um token, está funcionando! ✅

---

## 🔒 IMPORTANTE

**⚠️ Altere a senha padrão após o primeiro login!**

Para criar mais usuários, use o endpoint (após fazer login como admin):

```bash
POST /api/auth/create-user
Authorization: Bearer <seu-token-admin>
{
  "email": "novo@usuario.com",
  "password": "senha123",
  "name": "Novo Usuário",
  "is_admin": false
}
```

