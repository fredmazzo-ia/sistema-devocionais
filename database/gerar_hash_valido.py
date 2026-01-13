#!/usr/bin/env python3
"""
Script para gerar hash bcrypt válido
Execute no terminal do EasyPanel: python database/gerar_hash_valido.py
"""
import bcrypt

password = "admin123"
email = "fredmazzo@gmail.com"
name = "Administrador"

# Gerar hash bcrypt (12 rounds)
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
hashed_str = hashed.decode('utf-8')

print("=" * 80)
print("SQL PARA CRIAR/ATUALIZAR USUÁRIO ADMIN")
print("=" * 80)
print()
print("-- Execute este SQL no PostgreSQL do EasyPanel:")
print()
print("-- Deletar usuário existente")
print(f"DELETE FROM users WHERE email = '{email}';")
print()
print("-- Inserir novo usuário admin")
print("INSERT INTO users (email, name, hashed_password, is_active, is_admin, created_at, updated_at)")
print("VALUES (")
print(f"    '{email}',")
print(f"    '{name}',")
print(f"    '{hashed_str}',")
print("    true,")
print("    true,")
print("    NOW(),")
print("    NOW()")
print(");")
print()
print("-- Verificar")
print(f"SELECT id, email, name, is_admin, is_active, created_at FROM users WHERE email = '{email}';")
print()
print("=" * 80)
print("CREDENCIAIS:")
print(f"Email: {email}")
print(f"Senha: {password}")
print("=" * 80)
print()
print("Hash gerado:")
print(hashed_str)

