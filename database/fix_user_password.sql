-- Script SQL para corrigir usuário admin
-- Execute este script se o Python não funcionar

-- Primeiro, vamos ver o usuário atual
SELECT id, email, hashed_password, is_active, is_admin 
FROM users 
WHERE email = 'fredmazzo@gmail.com';

-- Para corrigir, você precisa gerar um hash bcrypt correto
-- Use o script Python: python database/fix_user_password.py
-- Ou gere um hash manualmente e substitua abaixo:

-- Exemplo de hash bcrypt válido (senha: admin123)
-- $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5Y
-- (Este é apenas um exemplo, gere um novo hash!)

-- Para deletar e recriar (CUIDADO!):
-- DELETE FROM users WHERE email = 'fredmazzo@gmail.com';

-- Depois execute o script Python para criar com hash correto

