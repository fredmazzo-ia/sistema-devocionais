# Guia de Instalação

## Pré-requisitos

- Python 3.9 ou superior
- Node.js 18 ou superior
- npm ou yarn

## Instalação do Backend

1. Navegue até a pasta do backend:
```bash
cd backend
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
   - **Windows (PowerShell):**
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **Windows (CMD):**
     ```cmd
     venv\Scripts\activate.bat
     ```
   - **Linux/Mac:**
     ```bash
     source venv/bin/activate
     ```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

5. Configure as variáveis de ambiente (opcional):
   - Copie `env.example` para `.env`
   - Edite `.env` com suas configurações do WhatsApp (se necessário)

6. Execute o servidor:
```bash
python main.py
```

Ou usando uvicorn diretamente:
```bash
uvicorn main:app --reload
```

O backend estará disponível em `http://localhost:8000`

## Instalação do Frontend

1. Navegue até a pasta do frontend:
```bash
cd frontend
```

2. Instale as dependências:
```bash
npm install
```

3. Execute o servidor de desenvolvimento:
```bash
npm run dev
```

O frontend estará disponível em `http://localhost:3000`

## Configuração Inicial

### 1. Configurar Portais de Notícias

Edite o arquivo `backend/app/config.py` e adicione os portais que deseja monitorar:

```python
NEWS_PORTALS: List[Dict[str, str]] = [
    {
        "name": "Nome do Portal",
        "url": "https://exemplo.com.br/noticias",
        "selectors": {
            "article": ".classe-do-artigo",
            "title": "h2",
            "link": "a",
            "date": ".data",
            "content": ".conteudo"
        }
    },
]
```

**Dica:** Use as ferramentas de desenvolvedor do navegador para identificar os seletores CSS corretos.

### 2. Configurar Responsáveis

No mesmo arquivo `backend/app/config.py`, configure os responsáveis:

```python
RESPONSIBLES: List[Dict[str, str]] = [
    {
        "name": "Nome do Responsável",
        "phone": "+5511999999999",  # Formato internacional
        "area": "CRAS"  # ou "CREAS", "Cadastro Único", etc.
    },
]
```

### 3. Configurar WhatsApp (Opcional)

Para habilitar notificações via WhatsApp:

1. Obtenha credenciais da API do WhatsApp Business
2. Configure no arquivo `.env`:
   ```
   WHATSAPP_ENABLED=true
   WHATSAPP_API_URL=https://graph.facebook.com/v18.0
   WHATSAPP_API_KEY=sua_chave_aqui
   WHATSAPP_PHONE_ID=seu_phone_id_aqui
   ```

3. Habilite no `config.py`:
   ```python
   WHATSAPP_ENABLED: bool = True
   ```

## Primeiros Passos

1. Inicie o backend e frontend
2. Acesse `http://localhost:3000`
3. Vá para a página "Monitoramento" e clique em "Executar Monitoramento Agora"
4. Verifique as notícias na página "Notícias"
5. Configure os portais reais que deseja monitorar

## Estrutura de Diretórios

```
Imprensa/
├── backend/
│   ├── app/
│   │   ├── routers/      # Endpoints da API
│   │   ├── scraper.py    # Módulo de raspagem
│   │   ├── analyzer.py   # Análise de notícias
│   │   ├── whatsapp_service.py  # Notificações
│   │   └── scheduler.py  # Agendamento
│   ├── main.py           # Ponto de entrada
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # Componentes React
│   │   └── services/     # Serviços de API
│   └── package.json
└── README.md
```

## Solução de Problemas

### Backend não inicia
- Verifique se o Python está instalado: `python --version`
- Verifique se todas as dependências foram instaladas: `pip list`
- Verifique se o ambiente virtual está ativado

### Frontend não conecta ao backend
- Verifique se o backend está rodando na porta 8000
- Verifique o proxy no `vite.config.ts`
- Verifique o CORS no `main.py`

### Raspagem não funciona
- Verifique os seletores CSS no `config.py`
- Alguns sites podem bloquear requisições automatizadas
- Considere usar Selenium para sites com JavaScript

## Próximos Passos

- [ ] Configurar portais reais de notícias
- [ ] Ajustar palavras-chave de detecção
- [ ] Configurar integração WhatsApp
- [ ] Personalizar mensagens de notificação
- [ ] Adicionar mais funcionalidades ao dashboard

