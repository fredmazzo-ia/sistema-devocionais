-- Migração: Corrigir tabela agendamento_envios para corresponder ao modelo Python
-- Adiciona coluna 'sent' se não existir

-- Verificar e adicionar coluna 'sent' se não existir
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'agendamento_envios' 
        AND column_name = 'sent'
    ) THEN
        ALTER TABLE agendamento_envios 
        ADD COLUMN sent BOOLEAN DEFAULT FALSE;
        
        CREATE INDEX IF NOT EXISTS idx_agendamento_envios_sent ON agendamento_envios(sent);
        
        RAISE NOTICE 'Coluna sent adicionada à tabela agendamento_envios';
    ELSE
        RAISE NOTICE 'Coluna sent já existe na tabela agendamento_envios';
    END IF;
END $$;

-- Verificar se sent_at existe (deve existir, mas vamos garantir)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'agendamento_envios' 
        AND column_name = 'sent_at'
    ) THEN
        ALTER TABLE agendamento_envios 
        ADD COLUMN sent_at TIMESTAMP;
        
        CREATE INDEX IF NOT EXISTS idx_agendamento_envios_sent_at ON agendamento_envios(sent_at);
        
        RAISE NOTICE 'Coluna sent_at adicionada à tabela agendamento_envios';
    ELSE
        RAISE NOTICE 'Coluna sent_at já existe na tabela agendamento_envios';
    END IF;
END $$;

-- Remover colunas que não existem no modelo Python (se existirem)
-- Estas colunas podem ter sido criadas em versões anteriores mas não estão no modelo atual
DO $$
BEGIN
    -- Remover contato_id se existir (não está no modelo)
    IF EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'agendamento_envios' 
        AND column_name = 'contato_id'
    ) THEN
        ALTER TABLE agendamento_envios DROP COLUMN contato_id;
        RAISE NOTICE 'Coluna contato_id removida da tabela agendamento_envios';
    END IF;
    
    -- Remover recipient_phone se existir (não está no modelo)
    IF EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'agendamento_envios' 
        AND column_name = 'recipient_phone'
    ) THEN
        ALTER TABLE agendamento_envios DROP COLUMN recipient_phone;
        RAISE NOTICE 'Coluna recipient_phone removida da tabela agendamento_envios';
    END IF;
    
    -- Remover recipient_name se existir (não está no modelo)
    IF EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'agendamento_envios' 
        AND column_name = 'recipient_name'
    ) THEN
        ALTER TABLE agendamento_envios DROP COLUMN recipient_name;
        RAISE NOTICE 'Coluna recipient_name removida da tabela agendamento_envios';
    END IF;
    
    -- Remover message_text se existir (não está no modelo)
    IF EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'agendamento_envios' 
        AND column_name = 'message_text'
    ) THEN
        ALTER TABLE agendamento_envios DROP COLUMN message_text;
        RAISE NOTICE 'Coluna message_text removida da tabela agendamento_envios';
    END IF;
    
    -- Remover status se existir (não está no modelo)
    IF EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'agendamento_envios' 
        AND column_name = 'status'
    ) THEN
        ALTER TABLE agendamento_envios DROP COLUMN status;
        RAISE NOTICE 'Coluna status removida da tabela agendamento_envios';
    END IF;
    
    -- Remover agendamento_type se existir (não está no modelo)
    IF EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'agendamento_envios' 
        AND column_name = 'agendamento_type'
    ) THEN
        ALTER TABLE agendamento_envios DROP COLUMN agendamento_type;
        RAISE NOTICE 'Coluna agendamento_type removida da tabela agendamento_envios';
    END IF;
    
    -- Remover error_message se existir (não está no modelo)
    IF EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'agendamento_envios' 
        AND column_name = 'error_message'
    ) THEN
        ALTER TABLE agendamento_envios DROP COLUMN error_message;
        RAISE NOTICE 'Coluna error_message removida da tabela agendamento_envios';
    END IF;
    
    -- Remover instance_name se existir (não está no modelo)
    IF EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'agendamento_envios' 
        AND column_name = 'instance_name'
    ) THEN
        ALTER TABLE agendamento_envios DROP COLUMN instance_name;
        RAISE NOTICE 'Coluna instance_name removida da tabela agendamento_envios';
    END IF;
END $$;

SELECT '✅ Migração concluída: tabela agendamento_envios atualizada' AS status;
