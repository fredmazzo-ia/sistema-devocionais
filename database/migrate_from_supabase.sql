-- =====================================================
-- Script para migrar contatos do Supabase para PostgreSQL
-- Execute após criar as tabelas
-- =====================================================

-- Exemplo de como inserir contatos manualmente
-- Ou use o script Python fornecido

-- Inserir contatos exemplo
INSERT INTO devocional_contatos (phone, name, active) 
VALUES 
    ('5516996480805', 'Tadeu', TRUE),
    ('5511999999999', 'Maria', TRUE),
    ('5511888888888', 'João', TRUE)
ON CONFLICT (phone) DO UPDATE 
SET 
    name = EXCLUDED.name,
    active = EXCLUDED.active,
    updated_at = CURRENT_TIMESTAMP;

-- =====================================================
-- Query para verificar contatos
-- =====================================================

SELECT 
    id,
    phone,
    name,
    active,
    total_sent,
    last_sent,
    created_at
FROM devocional_contatos
ORDER BY name, phone;
