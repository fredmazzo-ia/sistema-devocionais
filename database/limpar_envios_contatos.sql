-- Script para limpar envios dos contatos atuais e zerar contadores
-- ATENÇÃO: Este script é DESTRUTIVO e não pode ser revertido!

BEGIN;

-- 1. Deletar todos os envios (devocional_envios)
DELETE FROM devocional_envios;

-- 2. Zerar contadores de envios dos contatos
UPDATE devocional_contatos 
SET 
    total_sent = 0,
    last_sent = NULL;

-- 3. Limpar histórico de engajamento (opcional - descomente se quiser)
-- DELETE FROM engagement_history;

-- 4. Resetar scores de engajamento para 100 (opcional - descomente se quiser)
-- UPDATE contact_engagement 
-- SET 
--     engagement_score = 100.0,
--     total_sent = 0,
--     total_responded = 0,
--     total_read = 0,
--     total_delivered = 0,
--     consecutive_no_response = 0,
--     consecutive_not_read = 0,
--     consecutive_not_delivered = 0,
--     last_response_date = NULL,
--     last_sent_date = NULL,
--     last_read_date = NULL,
--     last_delivered_date = NULL;

-- 5. Limpar eventos de webhook (opcional - descomente se quiser)
-- DELETE FROM webhook_events;

-- 6. Limpar consentimentos (opcional - descomente se quiser)
-- DELETE FROM contact_consent;

COMMIT;

-- Verificar resultado
SELECT 
    (SELECT COUNT(*) FROM devocional_envios) as total_envios,
    (SELECT COUNT(*) FROM devocional_contatos) as total_contatos,
    (SELECT SUM(total_sent) FROM devocional_contatos) as total_sent_sum;
