-- Adicionar contato: Alex Mantovani
-- Execute este SQL no banco de dados

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

-- Verificar se foi inserido
SELECT * FROM devocional_contatos WHERE phone = '5516982115555';
