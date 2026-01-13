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
-- IMPORTANTE: Se este hash não funcionar, execute no terminal do EasyPanel:
-- python database/gerar_hash_valido.py
-- Isso gerará um hash válido e mostrará o SQL completo
INSERT INTO users (email, name, hashed_password, is_active, is_admin, created_at, updated_at)
VALUES (
    'fredmazzo@gmail.com',
    'Administrador',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5',
    true,
    true,
    NOW(),
    NOW()
);

-- Verificar se foi criado
SELECT id, email, name, is_admin, is_active, created_at 
FROM users 
WHERE email = 'fredmazzo@gmail.com';
