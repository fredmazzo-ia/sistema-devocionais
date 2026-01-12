#!/usr/bin/env python3
"""
Script para criar usuário admin via Python (usa mesmo código do backend)
Execute no terminal do EasyPanel: python3 database/criar_admin_via_python.py
"""
import sys
import os

# Adicionar backend ao path
sys.path.insert(0, '/app')
sys.path.insert(0, '/app/backend')

try:
    from app.database import SessionLocal, User, init_db
    from app.auth import get_password_hash
    from sqlalchemy.exc import IntegrityError
    
    # Inicializar banco
    init_db()
    
    # Criar sessão
    db = SessionLocal()
    
    email = "fredmazzo@gmail.com"
    password = "admin123"
    name = "Administrador"
    
    try:
        # Verificar se usuário existe
        existing_user = db.query(User).filter(User.email == email).first()
        
        if existing_user:
            print(f"✅ Usuário {email} já existe. Atualizando...")
            # Atualizar senha e tornar admin
            existing_user.hashed_password = get_password_hash(password)
            existing_user.is_admin = True
            existing_user.is_active = True
            existing_user.name = name
            db.commit()
            db.refresh(existing_user)
            print(f"✅ Usuário atualizado com sucesso!")
            print(f"   ID: {existing_user.id}")
            print(f"   Email: {existing_user.email}")
            print(f"   Nome: {existing_user.name}")
            print(f"   Admin: {existing_user.is_admin}")
        else:
            print(f"✅ Criando novo usuário admin...")
            # Criar novo usuário
            hashed_password = get_password_hash(password)
            new_user = User(
                email=email,
                name=name,
                hashed_password=hashed_password,
                is_admin=True,
                is_active=True
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            print(f"✅ Usuário criado com sucesso!")
            print(f"   ID: {new_user.id}")
            print(f"   Email: {new_user.email}")
            print(f"   Nome: {new_user.name}")
            print(f"   Admin: {new_user.is_admin}")
        
        print()
        print("=" * 80)
        print("CREDENCIAIS:")
        print(f"Email: {email}")
        print(f"Senha: {password}")
        print("=" * 80)
        print()
        print("✅ Agora você pode fazer login no frontend!")
        
    except IntegrityError as e:
        db.rollback()
        print(f"❌ Erro de integridade: {e}")
        sys.exit(1)
    except Exception as e:
        db.rollback()
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()
        
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    print()
    print("Tente executar de dentro do container/app:")
    print("  python3 /app/database/criar_admin_via_python.py")
    print()
    print("Ou execute este comando inline:")
    print("  python3 -c \"import sys; sys.path.insert(0, '/app'); from app.database import SessionLocal, User, init_db; from app.auth import get_password_hash; init_db(); db = SessionLocal(); u = db.query(User).filter(User.email == 'fredmazzo@gmail.com').first(); h = get_password_hash('admin123'); u.hashed_password = h if u else None; u.is_admin = True if u else None; u.is_active = True if u else None; db.commit() if u else db.add(User(email='fredmazzo@gmail.com', name='Administrador', hashed_password=h, is_admin=True, is_active=True)); db.commit(); print('OK')\"")
    sys.exit(1)

