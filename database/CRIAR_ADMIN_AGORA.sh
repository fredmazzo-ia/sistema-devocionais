#!/bin/bash
# Execute este script no terminal do EasyPanel
# bash database/CRIAR_ADMIN_AGORA.sh

python3 << 'PYEOF'
import sys
sys.path.insert(0, '/app')

import bcrypt
from app.database import SessionLocal, User, init_db

init_db()
db = SessionLocal()

email = "fredmazzo@gmail.com"
password = "admin123"
name = "Administrador"

try:
    # Deletar existente
    db.query(User).filter(User.email == email).delete()
    db.commit()
    
    # Gerar hash com bcrypt DIRETO (evita problema do passlib)
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt(12))
    hashed_str = hashed.decode('utf-8')
    
    # Criar usuário
    user = User(
        email=email,
        name=name,
        hashed_password=hashed_str,
        is_admin=True,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # TESTAR se funciona
    test_user = db.query(User).filter(User.email == email).first()
    test_pass = bcrypt.checkpw(password_bytes, test_user.hashed_password.encode('utf-8'))
    
    print("=" * 80)
    if test_pass:
        print("SUCESSO! Usuario criado e senha verificada!")
    else:
        print("ERRO! Senha nao confere!")
    print("=" * 80)
    print(f"ID: {user.id}")
    print(f"Email: {user.email}")
    print(f"Teste senha: {test_pass}")
    print()
    print("CREDENCIAIS:")
    print(f"Email: {email}")
    print(f"Senha: {password}")
    print("=" * 80)
    
except Exception as e:
    db.rollback()
    print(f"ERRO: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
PYEOF

