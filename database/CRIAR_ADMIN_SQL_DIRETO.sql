-- ============================================================
-- SCRIPT SQL PARA CRIAR USUÁRIO ADMIN DIRETAMENTE NO BANCO
-- ============================================================
-- Execute este script no terminal do PostgreSQL do EasyPanel
-- ou via interface do EasyPanel (Database > SQL Editor)
--
-- CREDENCIAIS:
-- Email: fredmazzo@gmail.com
-- Senha: admin123
-- ============================================================

-- Deletar usuário existente (se houver)
DELETE FROM users WHERE email = 'fredmazzo@gmail.com';

-- Inserir novo usuário admin
-- Hash bcrypt gerado para senha: admin123 (12 rounds)
-- Este hash foi gerado com: bcrypt.hashpw(b'admin123', bcrypt.gensalt(12))
INSERT INTO users (email, name, hashed_password, is_active, is_admin, created_at, updated_at)
VALUES (
    'fredmazzo@gmail.com',
    'Administrador',
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
    true,
    true,
    NOW(),
    NOW()
);

-- Verificar se foi criado
SELECT id, email, name, is_admin, is_active, created_at 
FROM users 
WHERE email = 'fredmazzo@gmail.com';
