# Sistema de Monitoramento de Notícias - Secretaria da Assistência Social

Aplicação web interativa para monitoramento e raspagem de portais de notícias, com detecção automática de notícias relacionadas à Secretaria da Assistência Social e envio de notificações via WhatsApp.

## 🚀 Funcionalidades

- **Raspagem Automática**: Monitoramento contínuo de portais de notícias da cidade
- **Detecção Inteligente**: Identificação automática de notícias sobre a Secretaria da Assistência Social
- **Processamento de Dados**: Extração e organização de informações relevantes
- **Notificações WhatsApp**: Envio automático de alertas com instruções e dados para responsáveis

## 📁 Estrutura do Projeto

```
Imprensa/
├── backend/          # API FastAPI com lógica de raspagem e processamento
├── frontend/         # Interface React/TypeScript
├── README.md
└── .gitignore
```

## 🛠️ Tecnologias

### Backend
- Python 3.9+
- FastAPI
- BeautifulSoup4 / Scrapy (web scraping)
- SQLAlchemy (banco de dados)
- python-whatsapp-api ou similar

### Frontend
- React 18+
- TypeScript
- Axios (comunicação com API)

## 📦 Instalação

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## 🚀 Execução

### Backend

```bash
cd backend
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm start
```

## 📝 Configuração

1. Configure os portais de notícias a serem monitorados em `backend/config.py`
2. Configure as credenciais do WhatsApp em `backend/.env`
3. Defina os responsáveis e seus números de WhatsApp em `backend/config.py`

## 🔧 Próximos Passos

- [ ] Configurar portais de notícias específicos
- [ ] Implementar sistema de classificação de notícias
- [ ] Configurar integração WhatsApp
- [ ] Criar dashboard de visualização
- [ ] Implementar sistema de alertas e notificações

