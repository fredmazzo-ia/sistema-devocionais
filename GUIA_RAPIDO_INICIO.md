# 🚀 Guia Rápido de Início

## Para Continuar o Projeto em Outro PC

### 1. Clonar Repositório

```bash
git clone https://github.com/fredmazzo-ia/sistema-devocionais.git
cd sistema-devocionais
```

### 2. Configurar Ambiente Local

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Ativar (Linux/Mac)
source venv/bin/activate

# Instalar dependências
cd backend
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Ambiente

```bash
# Copiar exemplo
cp env.example .env

# Editar .env com suas configurações
```

**Variáveis essenciais:**
```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/devocionais
EVOLUTION_API_URL=http://sua-evolution-api.com
EVOLUTION_API_KEY=sua-api-key
EVOLUTION_INSTANCE_NAME=Devocional
DEVOCIONAL_WEBHOOK_SECRET=seu-secret
DEVOCIONAL_SEND_TIME=06:00
```

### 4. Configurar Banco de Dados

```bash
# Criar banco
createdb devocionais

# Executar schema
psql -d devocionais -f ../database/devocionais_schema.sql
```

### 5. Executar

```bash
cd backend
uvicorn main:app --reload
```

## 📋 Checklist de Configuração

- [ ] Repositório clonado
- [ ] Ambiente virtual criado e ativado
- [ ] Dependências instaladas
- [ ] Arquivo `.env` configurado
- [ ] Banco de dados criado
- [ ] Schema SQL executado
- [ ] API rodando localmente
- [ ] Endpoint `/health` funcionando

## 🔗 URLs Importantes

- **API Local**: `http://localhost:8000`
- **API Produção**: `https://imobmiq-devocional.90qhxz.easypanel.host`
- **Docs API**: `http://localhost:8000/docs` (Swagger)

## 📚 Próximos Passos

1. Testar endpoints localmente
2. Configurar n8n (se necessário)
3. Adicionar contatos
4. Testar envio

---

**Pronto para continuar o desenvolvimento!** 🚀
