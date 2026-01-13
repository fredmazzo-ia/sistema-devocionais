-- Adicionar campo message_type na tabela devocional_envios
-- Para diferenciar entre devocionais agendados, devocionais manuais e mensagens personalizadas

ALTER TABLE devocional_envios 
ADD COLUMN IF NOT EXISTS message_type VARCHAR(20) DEFAULT 'devocional_agendado';

-- Valores possíveis:
-- 'devocional_agendado' - Devocional enviado pelo scheduler
-- 'devocional_manual' - Devocional enviado manualmente
-- 'mensagem_personalizada' - Mensagem personalizada enviada pela página Mensagens

-- Criar índice para melhor performance em consultas
CREATE INDEX IF NOT EXISTS idx_envios_message_type ON devocional_envios(message_type);

-- Atualizar registros existentes baseado em scheduled_for
UPDATE devocional_envios 
SET message_type = CASE 
    WHEN scheduled_for IS NOT NULL THEN 'devocional_agendado'
    WHEN devocional_id IS NOT NULL THEN 'devocional_manual'
    ELSE 'mensagem_personalizada'
END
WHERE message_type IS NULL OR message_type = 'devocional_agendado';
