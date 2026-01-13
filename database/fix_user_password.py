#!/usr/bin/env python3
"""
Script para corrigir ou criar usuário admin com hash bcrypt correto
"""
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.database import SessionLocal
from app.auth import get_password_hash
from app.database import User

def fix_or_create_admin():
    """Corrige ou cria usuário admin"""
    db = SessionLocal()
    try:
        email = "fredmazzo@gmail.com"
        password = "admin123"  # Mude isso para uma senha segura!
        
        # Verificar se usuário existe
        user = db.query(User).filter(User.email == email).first()
        
        if user:
            print(f"✅ Usuário {email} encontrado")
            print(f"   Hash atual: {user.hashed_password[:50]}...")
            
            # Gerar novo hash correto
            new_hash = get_password_hash(password)
            user.hashed_password = new_hash
            user.is_active = True
            user.is_admin = True
            
            db.commit()
            print(f"✅ Hash corrigido!")
            print(f"   Novo hash: {new_hash[:50]}...")
        else:
            print(f"❌ Usuário {email} não encontrado")
            print(f"   Criando novo usuário...")
            
            # Criar novo usuário
            new_user = User(
                email=email,
                hashed_password=get_password_hash(password),
                is_active=True,
                is_admin=True
            )
            
            db.add(new_user)
            db.commit()
            print(f"✅ Usuário criado com sucesso!")
        
        print(f"\n📋 Credenciais:")
        print(f"   Email: {email}")
        print(f"   Senha: {password}")
        print(f"\n⚠️  IMPORTANTE: Altere a senha após o primeiro login!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erro: {e}")
        return 1
    finally:
        db.close()
    
    return 0

if __name__ == "__main__":
    exit(fix_or_create_admin())

