-- =====================================================
-- Queries Úteis para o Sistema de Devocionais
-- =====================================================

-- 1. Buscar devocional de hoje
SELECT * FROM devocional_hoje;

-- 2. Buscar devocional por data
SELECT * FROM devocionais 
WHERE date = '2026-01-07';

-- 3. Listar devocionais não enviados
SELECT 
    id,
    title,
    date,
    created_at,
    source
FROM devocionais
WHERE sent = FALSE
ORDER BY date DESC;

-- 4. Estatísticas gerais
SELECT * FROM devocional_stats;

-- 5. Contatos ativos
SELECT * FROM get_contatos_ativos();

-- 6. Envios de hoje
SELECT 
    e.id,
    e.recipient_name,
    e.recipient_phone,
    e.status,
    e.sent_at,
    d.title as devocional_title
FROM devocional_envios e
LEFT JOIN devocionais d ON d.id = e.devocional_id
WHERE DATE(e.sent_at) = CURRENT_DATE
ORDER BY e.sent_at DESC;

-- 7. Taxa de sucesso por dia
SELECT 
    DATE(sent_at) as data,
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE status = 'sent') as sucesso,
    COUNT(*) FILTER (WHERE status = 'failed') as falha,
    ROUND(100.0 * COUNT(*) FILTER (WHERE status = 'sent') / COUNT(*), 2) as taxa_sucesso
FROM devocional_envios
WHERE sent_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY DATE(sent_at)
ORDER BY data DESC;

-- 8. Top 10 contatos que mais receberam
SELECT 
    c.name,
    c.phone,
    c.total_sent,
    c.last_sent
FROM devocional_contatos c
WHERE c.active = TRUE
ORDER BY c.total_sent DESC
LIMIT 10;

-- 9. Devocionais por fonte
SELECT 
    source,
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE sent = TRUE) as enviados
FROM devocionais
GROUP BY source
ORDER BY total DESC;

-- 10. Buscar devocionais por palavra-chave
SELECT 
    id,
    title,
    date,
    palavras_chave
FROM devocionais
WHERE 'guia' = ANY(palavras_chave)  -- Substitua 'guia' pela palavra desejada
ORDER BY date DESC;

-- 11. Buscar em conteúdo (full-text search)
SELECT 
    id,
    title,
    date,
    ts_rank(to_tsvector('portuguese', content), query) as rank
FROM devocionais, to_tsquery('portuguese', 'Deus & guia') query
WHERE to_tsvector('portuguese', content) @@ query
ORDER BY rank DESC;

-- 12. Últimos 10 devocionais
SELECT 
    id,
    title,
    date,
    source,
    sent,
    sent_at,
    total_sent
FROM devocionais
ORDER BY created_at DESC
LIMIT 10;

-- 13. Contatos que não receberam hoje
SELECT 
    c.id,
    c.name,
    c.phone,
    c.last_sent
FROM devocional_contatos c
WHERE c.active = TRUE
AND (
    c.last_sent IS NULL 
    OR DATE(c.last_sent) < CURRENT_DATE
)
ORDER BY c.name;

-- 14. Erros recentes
SELECT 
    e.id,
    e.recipient_phone,
    e.recipient_name,
    e.error_message,
    e.retry_count,
    e.sent_at
FROM devocional_envios e
WHERE e.status = 'failed'
AND e.sent_at >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY e.sent_at DESC;

-- 15. Marcar devocional como enviado
SELECT marcar_devocional_enviado(1);  -- Substitua 1 pelo ID do devocional
