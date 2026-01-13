-- =====================================================
-- Migração: Adicionar campos de status detalhado de mensagens
-- Rastreamento de delivered e read via webhook da Evolution API
-- =====================================================

-- Adicionar colunas para rastreamento de status detalhado
ALTER TABLE devocional_envios 
ADD COLUMN IF NOT EXISTS message_status VARCHAR(20) DEFAULT 'pending',
ADD COLUMN IF NOT EXISTS delivered_at TIMESTAMP,
ADD COLUMN IF NOT EXISTS read_at TIMESTAMP;

-- Criar índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_envios_message_status ON devocional_envios(message_status);
CREATE INDEX IF NOT EXISTS idx_envios_delivered_at ON devocional_envios(delivered_at);
CREATE INDEX IF NOT EXISTS idx_envios_read_at ON devocional_envios(read_at);
CREATE INDEX IF NOT EXISTS idx_envios_message_id ON devocional_envios(message_id);

-- Atualizar constraint de status para incluir novos status
-- (Nota: PostgreSQL não permite alterar constraint CHECK facilmente,
-- então vamos criar uma nova e remover a antiga se necessário)
ALTER TABLE devocional_envios 
DROP CONSTRAINT IF EXISTS devocional_envios_status_check;

ALTER TABLE devocional_envios
ADD CONSTRAINT devocional_envios_status_check 
CHECK (status IN ('pending', 'sent', 'failed', 'retrying', 'blocked'));

-- Comentários para documentação
COMMENT ON COLUMN devocional_envios.message_status IS 'Status detalhado: pending, sent, delivered, read, failed';
COMMENT ON COLUMN devocional_envios.delivered_at IS 'Timestamp de quando a mensagem foi entregue (via webhook Evolution API)';
COMMENT ON COLUMN devocional_envios.read_at IS 'Timestamp de quando a mensagem foi lida/visualizada (via webhook Evolution API)';

-- =====================================================
-- FIM DA MIGRAÇÃO
-- =====================================================
