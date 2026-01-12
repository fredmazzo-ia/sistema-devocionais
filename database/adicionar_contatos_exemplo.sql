-- Script para adicionar contatos de exemplo
-- Execute este SQL no banco de dados

-- Adicionar Frederico Mazzo
INSERT INTO devocional_contatos (phone, name, active, created_at, updated_at)
VALUES (
    '5516996480805',
    'Frederico Mazzo',
    true,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
)
ON CONFLICT (phone) 
DO UPDATE SET
    name = EXCLUDED.name,
    active = true,
    updated_at = CURRENT_TIMESTAMP;

-- Adicionar Alex Mantovani
INSERT INTO devocional_contatos (phone, name, active, created_at, updated_at)
VALUES (
    '5516982115555',
    'Alex Mantovani',
    true,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
)
ON CONFLICT (phone) 
DO UPDATE SET
    name = EXCLUDED.name,
    active = true,
    updated_at = CURRENT_TIMESTAMP;

-- Verificar contatos ativos
SELECT 
    id,
    phone,
    name,
    active,
    total_sent,
    last_sent,
    created_at
FROM devocional_contatos
WHERE active = true
ORDER BY name;
