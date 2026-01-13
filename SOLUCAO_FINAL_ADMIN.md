# 🔧 SOLUÇÃO FINAL - Criar Admin

## ⚡ **COMANDO DIRETO NO TERMINAL DO EASYPANEL**

Execute este comando **DIRETO** no terminal (copie tudo):

```bash
python3 -c "import sys; sys.path.insert(0, '/app'); from app.database import SessionLocal, User, init_db; from app.auth import get_password_hash, verify_password; init_db(); db = SessionLocal(); db.query(User).filter(User.email == 'fredmazzo@gmail.com').delete(); db.commit(); h = get_password_hash('admin123'); u = User(email='fredmazzo@gmail.com', name='Administrador', hashed_password=h, is_admin=True, is_active=True); db.add(u); db.commit(); db.refresh(u); t = verify_password('admin123', u.hashed_password); print('✅ SUCESSO!' if t else '❌ ERRO'); print(f'Email: {u.email}'); print(f'Senha testada: {t}')"
```

---

## 📝 **OU Execute o Script Python**

Se o comando acima não funcionar, execute:

```bash
python3 /app/database/criar_admin_direto.py
```

---

## 🔐 **Credenciais**

- **Email:** `fredmazzo@gmail.com`
- **Senha:** `admin123`

---

## ✅ **Isso Vai Funcionar!**

O script usa **EXATAMENTE** o mesmo código do backend, garantindo 100% de compatibilidade.

