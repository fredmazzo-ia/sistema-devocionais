-- Criar tabela para rastrear agendamentos de envio de devocionais
CREATE TABLE IF NOT EXISTS agendamento_envios (
    id SERIAL PRIMARY KEY,
    devocional_id INTEGER,
    contato_id INTEGER,
    scheduled_for TIMESTAMP NOT NULL,
    sent_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',
    error_message TEXT,
    recipient_phone VARCHAR(20) NOT NULL,
    recipient_name VARCHAR(100),
    message_text TEXT,
    instance_name VARCHAR(100),
    agendamento_type VARCHAR(20) DEFAULT 'automatico',
    metadata_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar índices
CREATE INDEX IF NOT EXISTS idx_agendamento_envios_devocional_id ON agendamento_envios(devocional_id);
CREATE INDEX IF NOT EXISTS idx_agendamento_envios_contato_id ON agendamento_envios(contato_id);
CREATE INDEX IF NOT EXISTS idx_agendamento_envios_scheduled_for ON agendamento_envios(scheduled_for);
CREATE INDEX IF NOT EXISTS idx_agendamento_envios_sent_at ON agendamento_envios(sent_at);
CREATE INDEX IF NOT EXISTS idx_agendamento_envios_status ON agendamento_envios(status);
CREATE INDEX IF NOT EXISTS idx_agendamento_envios_created_at ON agendamento_envios(created_at);

-- Adicionar coluna created_at na tabela devocional_envios se não existir
ALTER TABLE devocional_envios 
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

