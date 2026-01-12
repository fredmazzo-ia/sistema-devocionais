-- Atualizar telefone do contato ID 1
-- Data: 2026-01-10
-- Descrição: Atualizar telefone do contato ID 1 para 5516996282630

UPDATE devocional_contatos
SET phone = '5516996282630'
WHERE id = 1;

-- Verificar atualização
SELECT id, phone, name, active, total_sent, last_sent
FROM devocional_contatos
WHERE id = 1;

