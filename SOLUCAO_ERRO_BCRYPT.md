# 🔧 Solução: Erro bcrypt hash malformado

## ❌ Erro Encontrado

```
ValueError: malformed bcrypt hash (checksum must be exactly 31 chars)
```

## 🔍 Causa

O hash bcrypt no banco de dados está malformado. Isso pode acontecer se:
- O usuário foi criado manualmente no banco
- O hash foi inserido incorretamente
- O hash foi truncado ou corrompido

## ✅ Solução

### **Opção 1: Script Python (Recomendado)**

Execute o script para corrigir ou criar o usuário:

```bash
cd backend
python ../database/fix_user_password.py
```

O script irá:
1. ✅ Verificar se o usuário existe
2. ✅ Gerar um hash bcrypt correto
3. ✅ Atualizar ou criar o usuário

**Credenciais padrão:**
- Email: `admin@devocional.com`
- Senha: `admin123`

⚠️ **IMPORTANTE:** Altere a senha após o primeiro login!

---

### **Opção 2: Via SQL (Manual)**

1. **Conecte ao banco:**
   ```bash
   psql -h HOST -U USER -d DATABASE
   ```

2. **Delete o usuário atual (se existir):**
   ```sql
   DELETE FROM users WHERE email = 'admin@devocional.com';
   ```

3. **Execute o script Python:**
   ```bash
   python database/fix_user_password.py
   ```

---

### **Opção 3: Criar via API (Após corrigir backend)**

Se o endpoint `/api/auth/create-user` estiver disponível:

```bash
curl -X POST https://imobmiq-devocional.90qhxz.easypanel.host/api/auth/create-user \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@devocional.com",
    "password": "admin123",
    "is_admin": true
  }'
```

---

## 🔐 Gerar Hash Manualmente

Se precisar gerar um hash manualmente:

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hash = pwd_context.hash("sua_senha")
print(hash)
```

---

## ✅ Verificação

Após corrigir, teste o login:
- Email: `admin@devocional.com`
- Senha: `admin123`

---

**Próximo passo:** Execute o script Python para corrigir o hash!

