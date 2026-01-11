#!/usr/bin/env python3
"""
Script para criar admin usando MESMO código do backend
Execute: python3 /app/database/criar_admin_direto.py
"""
import sys
sys.path.insert(0, '/app')

from app.database import SessionLocal, User, init_db
from app.auth import get_password_hash, verify_password
from sqlalchemy.exc import IntegrityError

# Inicializar
init_db()
db = SessionLocal()

email = "fredmazzo@gmail.com"
password = "admin123"
name = "Administrador"

try:
    # Deletar existente
    db.query(User).filter(User.email == email).delete()
    db.commit()
    
    # Criar novo
    hashed = get_password_hash(password)
    user = User(
        email=email,
        name=name,
        hashed_password=hashed,
        is_admin=True,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # TESTAR se funciona
    test_user = db.query(User).filter(User.email == email).first()
    test_pass = verify_password(password, test_user.hashed_password)
    
    print("=" * 80)
    if test_pass:
        print("✅ SUCESSO! Usuário criado e senha verificada!")
    else:
        print("❌ ERRO! Senha não confere após criar!")
    print("=" * 80)
    print(f"ID: {user.id}")
    print(f"Email: {user.email}")
    print(f"Hash: {user.hashed_password[:50]}...")
    print(f"Teste senha: {test_pass}")
    print()
    print("CREDENCIAIS:")
    print(f"Email: {email}")
    print(f"Senha: {password}")
    
except Exception as e:
    db.rollback()
    print(f"❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

