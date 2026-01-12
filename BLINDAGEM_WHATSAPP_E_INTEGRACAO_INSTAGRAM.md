# 🛡️ Ferramentas de Blindagem WhatsApp + 📸 Integração Instagram

## 📋 REVISÃO: FERRAMENTAS DE BLINDAGEM JÁ IMPLEMENTADAS

### ✅ 1. Rate Limiting (Limitação de Taxa)

**Status:** ✅ **IMPLEMENTADO**

**O que faz:**
- Controla quantidade de mensagens por hora e por dia
- Previne envio excessivo que pode causar bloqueio

**Configurações:**
- `DELAY_BETWEEN_MESSAGES`: Delay entre mensagens (padrão: 3.0 segundos)
- `MAX_MESSAGES_PER_HOUR`: Máximo por hora (padrão: 20)
- `MAX_MESSAGES_PER_DAY`: Máximo por dia (padrão: 200)

**Localização:**
- `backend/app/devocional_service.py`
- `backend/app/devocional_service_v2.py`
- `backend/app/config.py`

---

### ✅ 2. Multi-Instância (Distribuição de Carga)

**Status:** ✅ **IMPLEMENTADO**

**O que faz:**
- Distribui mensagens entre múltiplas instâncias Evolution API
- Reduz carga em cada número individual
- Failover automático se uma instância falhar

**Estratégias:**
- `round_robin`: Rotação circular
- `least_used`: Menos usada
- `priority`: Por prioridade
- `random`: Aleatória

**Localização:**
- `backend/app/instance_manager.py`
- `backend/app/devocional_service_v2.py`

---

### ✅ 3. Retry com Backoff Exponencial

**Status:** ✅ **IMPLEMENTADO**

**O que faz:**
- Tenta reenviar mensagens falhas automaticamente
- Aumenta delay entre tentativas (backoff exponencial)
- Evita spam de tentativas

**Configurações:**
- `MAX_RETRIES`: Máximo de tentativas (padrão: 3)
- `RETRY_DELAY`: Delay base entre tentativas (padrão: 5.0 segundos)
- Delay aumenta: `RETRY_DELAY * retry_count`

**Localização:**
- `backend/app/devocional_service.py`
- `backend/app/devocional_service_v2.py`

---

### ✅ 4. Health Check de Instâncias

**Status:** ✅ **IMPLEMENTADO**

**O que faz:**
- Verifica status das instâncias periodicamente
- Remove instâncias com erro do pool
- Detecta instâncias bloqueadas

**Localização:**
- `backend/app/instance_manager.py`

---

### ✅ 5. Personalização de Mensagens

**Status:** ✅ **IMPLEMENTADO**

**O que faz:**
- Adiciona saudação personalizada (Bom dia/Boa tarde/Boa noite)
- Inclui nome do destinatário
- Torna mensagens mais naturais e menos "spam"

**Localização:**
- `backend/app/devocional_service.py` - `_personalize_message()`
- `backend/app/devocional_service_v2.py`

---

### ✅ 6. vCard para Novos Contatos

**Status:** ✅ **IMPLEMENTADO**

**O que faz:**
- Envia vCard automaticamente para novos contatos
- Facilita que destinatários salvem o número
- Aumenta taxa de aceitação

**Configurações:**
- `SEND_VCARD_TO_NEW_CONTACTS`: Ativar/desativar (padrão: true)

**Localização:**
- `backend/app/vcard_service.py`
- `backend/app/devocional_service_v2.py`

---

### ✅ 7. Validação de Payload

**Status:** ✅ **IMPLEMENTADO**

**O que faz:**
- Valida telefone antes de enviar
- Valida tamanho da mensagem (máximo 4096 caracteres)
- Previne erros que podem causar bloqueio

**Localização:**
- `backend/app/devocional_service.py` - `_validate_payload()`
- `backend/app/devocional_service_v2.py`

---

### ✅ 8. Controle de Horário (Scheduler)

**Status:** ✅ **IMPLEMENTADO**

**O que faz:**
- Envia em horário específico (06:00)
- Evita envios em horários suspeitos
- Usa timezone de São Paulo

**Configurações:**
- `DEVOCIONAL_SEND_TIME`: Horário de envio (padrão: "06:00")

**Localização:**
- `backend/app/devocional_scheduler.py`

---

## 🚀 FERRAMENTAS DE BLINDAGEM PROPOSTAS (NÃO IMPLEMENTADAS)

### 🔄 1. Variação de Delay Aleatório

**O que faz:**
- Adiciona variação aleatória ao delay entre mensagens
- Torna padrão de envio menos previsível
- Simula comportamento humano

**Implementação:**
```python
import random

def get_randomized_delay(base_delay: float, variation: float = 0.3) -> float:
    """
    Retorna delay com variação aleatória
    
    Args:
        base_delay: Delay base (ex: 3.0 segundos)
        variation: Variação percentual (ex: 0.3 = 30%)
    
    Returns:
        Delay aleatório entre base_delay * (1 - variation) e base_delay * (1 + variation)
    """
    min_delay = base_delay * (1 - variation)
    max_delay = base_delay * (1 + variation)
    return random.uniform(min_delay, max_delay)
```

**Configuração:**
- `DELAY_VARIATION`: Variação percentual (padrão: 0.3 = 30%)

**Benefício:**
- ✅ Reduz detecção de padrão automatizado
- ✅ Simula comportamento humano

---

### 📊 2. Análise de Taxa de Resposta

**O que faz:**
- Monitora taxa de resposta dos destinatários
- Reduz frequência para contatos que não respondem
- Aumenta frequência para contatos engajados

**Implementação:**
```python
class EngagementTracker:
    def __init__(self):
        self.contact_engagement = {}  # {phone: engagement_score}
    
    def update_engagement(self, phone: str, responded: bool):
        """Atualiza score de engajamento"""
        if phone not in self.contact_engagement:
            self.contact_engagement[phone] = 0.5  # Score inicial
        
        if responded:
            self.contact_engagement[phone] = min(1.0, 
                self.contact_engagement[phone] + 0.1)
        else:
            self.contact_engagement[phone] = max(0.0,
                self.contact_engagement[phone] - 0.05)
    
    def should_send(self, phone: str) -> bool:
        """Decide se deve enviar baseado no engajamento"""
        score = self.contact_engagement.get(phone, 0.5)
        return score > 0.3  # Só envia se engajamento > 30%
```

**Benefício:**
- ✅ Reduz envios para contatos inativos
- ✅ Melhora taxa de resposta
- ✅ Reduz risco de bloqueio

---

### 🎲 3. Rotação de Conteúdo

**O que faz:**
- Varia formato das mensagens
- Alterna entre mensagens curtas e longas
- Adiciona emojis variados

**Implementação:**
```python
def format_message_variation(message: str, variation: str = "standard") -> str:
    """
    Aplica variações no formato da mensagem
    
    Args:
        message: Mensagem original
        variation: Tipo de variação (standard, short, long, emoji)
    
    Returns:
        Mensagem formatada
    """
    if variation == "short":
        # Versão resumida
        return message[:500] + "..." if len(message) > 500 else message
    elif variation == "emoji":
        # Adiciona emojis estratégicos
        return f"🙏 {message}"
    elif variation == "long":
        # Versão expandida
        return f"{message}\n\nQue Deus abençoe seu dia! 🙏"
    else:
        return message
```

**Benefício:**
- ✅ Reduz detecção de padrão
- ✅ Mantém mensagens naturais

---

### ⏸️ 4. Pausas Estratégicas

**O que faz:**
- Adiciona pausas maiores a cada X mensagens
- Simula "descanso" humano
- Reduz carga contínua

**Implementação:**
```python
def should_take_break(message_count: int, break_interval: int = 50) -> bool:
    """
    Decide se deve fazer pausa
    
    Args:
        message_count: Número de mensagens enviadas
        break_interval: Intervalo para pausa (ex: a cada 50 mensagens)
    
    Returns:
        True se deve fazer pausa
    """
    return message_count % break_interval == 0

def get_break_duration(base_delay: float) -> float:
    """Retorna duração da pausa (5-10x o delay normal)"""
    return random.uniform(base_delay * 5, base_delay * 10)
```

**Configuração:**
- `BREAK_INTERVAL`: Mensagens entre pausas (padrão: 50)
- `BREAK_DURATION_MULTIPLIER`: Multiplicador do delay (padrão: 5-10x)

**Benefício:**
- ✅ Simula comportamento humano
- ✅ Reduz carga contínua

---

### 🔍 5. Detecção de Bloqueio Proativo

**O que faz:**
- Monitora respostas da API
- Detecta sinais de bloqueio antes que aconteça
- Pausa envios automaticamente

**Implementação:**
```python
class BlockDetector:
    def __init__(self):
        self.error_patterns = []
        self.consecutive_errors = 0
    
    def analyze_response(self, response: dict) -> bool:
        """
        Analisa resposta da API para detectar bloqueio
        
        Returns:
            True se detectar bloqueio
        """
        # Padrões que indicam possível bloqueio
        error_messages = [
            "blocked",
            "rate limit",
            "too many requests",
            "forbidden",
            "unauthorized"
        ]
        
        error_text = str(response.get("error", "")).lower()
        
        for pattern in error_messages:
            if pattern in error_text:
                self.consecutive_errors += 1
                
                # Se 3 erros consecutivos, pode ser bloqueio
                if self.consecutive_errors >= 3:
                    return True
        
        # Reset se sucesso
        if response.get("status") == "success":
            self.consecutive_errors = 0
        
        return False
    
    def should_pause(self) -> bool:
        """Decide se deve pausar envios"""
        return self.consecutive_errors >= 3
```

**Benefício:**
- ✅ Detecta bloqueio antes que seja permanente
- ✅ Permite ação corretiva

---

### 📈 6. Limites Adaptativos

**O que faz:**
- Ajusta limites automaticamente baseado em taxa de sucesso
- Reduz limites se houver muitos erros
- Aumenta limites se tudo estiver OK

**Implementação:**
```python
class AdaptiveLimits:
    def __init__(self, base_hourly: int = 20, base_daily: int = 200):
        self.base_hourly = base_hourly
        self.base_daily = base_daily
        self.current_hourly = base_hourly
        self.current_daily = base_daily
        self.success_rate = 1.0  # 100% inicial
    
    def update_success_rate(self, success_count: int, total_count: int):
        """Atualiza taxa de sucesso"""
        if total_count > 0:
            self.success_rate = success_count / total_count
    
    def adjust_limits(self):
        """Ajusta limites baseado na taxa de sucesso"""
        if self.success_rate < 0.8:  # Menos de 80% de sucesso
            # Reduzir limites em 20%
            self.current_hourly = int(self.base_hourly * 0.8)
            self.current_daily = int(self.base_daily * 0.8)
        elif self.success_rate > 0.95:  # Mais de 95% de sucesso
            # Aumentar limites em 10% (cuidado!)
            self.current_hourly = int(self.base_hourly * 1.1)
            self.current_daily = int(self.base_daily * 1.1)
        else:
            # Manter limites base
            self.current_hourly = self.base_hourly
            self.current_daily = self.base_daily
```

**Benefício:**
- ✅ Adapta-se automaticamente
- ✅ Otimiza envios

---

### 🕐 7. Janelas de Envio Inteligentes

**O que faz:**
- Envia apenas em horários de maior engajamento
- Evita horários suspeitos (madrugada)
- Distribui envios ao longo do dia

**Implementação:**
```python
def is_safe_send_time(hour: int) -> bool:
    """
    Verifica se é horário seguro para envio
    
    Args:
        hour: Hora do dia (0-23)
    
    Returns:
        True se é horário seguro
    """
    # Horários seguros: 6h-22h
    safe_hours = list(range(6, 23))
    return hour in safe_hours

def get_optimal_send_times(total_contacts: int) -> List[int]:
    """
    Calcula horários ótimos para distribuir envios
    
    Args:
        total_contacts: Total de contatos
    
    Returns:
        Lista de horários (em horas)
    """
    # Distribuir entre 6h e 22h
    safe_hours = list(range(6, 23))
    
    # Se poucos contatos, enviar em horário único
    if total_contacts < 50:
        return [6]  # 06:00
    
    # Se muitos contatos, distribuir
    num_windows = min(4, total_contacts // 50)  # Máximo 4 janelas
    return [safe_hours[i * len(safe_hours) // num_windows] 
            for i in range(num_windows)]
```

**Benefício:**
- ✅ Aumenta taxa de resposta
- ✅ Reduz risco de bloqueio

---

### 📝 8. Template de Mensagens Variados

**O que faz:**
- Usa templates diferentes para variar formato
- Alterna entre estilos de mensagem
- Mantém conteúdo mas varia apresentação

**Implementação:**
```python
MESSAGE_TEMPLATES = [
    {
        "name": "standard",
        "format": "{greeting}, *{name}*\n\n{message}"
    },
    {
        "name": "warm",
        "format": "{greeting}, {name}! 🙏\n\n{message}"
    },
    {
        "name": "simple",
        "format": "{greeting}!\n\n{message}\n\nQue Deus abençoe seu dia!"
    }
]

def get_template_variation(contact_id: int) -> str:
    """Seleciona template baseado no contato (para consistência)"""
    template_index = contact_id % len(MESSAGE_TEMPLATES)
    return MESSAGE_TEMPLATES[template_index]["name"]
```

**Benefício:**
- ✅ Varia formato sem mudar conteúdo
- ✅ Mantém naturalidade

---

## 📸 INTEGRAÇÃO COM INSTAGRAM

### 🎯 Objetivo

Postar devocional automaticamente no Instagram quando:
1. n8n gera o devocional
2. Sistema recebe via webhook
3. Ou manualmente pelo frontend

### 🔧 Opção 1: Via n8n (Recomendado Inicialmente)

**Fluxo:**
```
n8n gera devocional
    ↓
n8n envia para webhook da API (salva no banco)
    ↓
n8n → Instagram Graph API (postar)
```

**Vantagens:**
- ✅ Já está no n8n
- ✅ Fácil de configurar
- ✅ Não precisa mudar backend

**Desvantagens:**
- ⚠️ Depende do n8n estar rodando
- ⚠️ Precisa configurar no n8n

---

### 🔧 Opção 2: Via Sistema (Backend)

**Fluxo:**
```
n8n gera devocional
    ↓
n8n envia para webhook da API (salva no banco)
    ↓
API detecta novo devocional
    ↓
API → Instagram Graph API (postar automaticamente)
```

**Vantagens:**
- ✅ Automático, sem depender n8n
- ✅ Mais controle
- ✅ Pode agendar

**Desvantagens:**
- ⚠️ Precisa implementar no backend
- ⚠️ Precisa gerenciar tokens Instagram

---

### 📋 Implementação: Instagram Graph API

#### **1. Pré-requisitos**

1. **Conta Instagram Business ou Creator**
   - Não funciona com conta pessoal
   - Precisa ter página do Facebook vinculada

2. **App Facebook Developer**
   - Criar app em [Facebook for Developers](https://developers.facebook.com/)
   - Obter App ID e App Secret

3. **Permissões Necessárias**
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_read_engagement` (se usar página)

4. **Tokens de Acesso**
   - Access Token de longo prazo
   - Page Access Token (se usar página)

#### **2. Estrutura de Código**

**Arquivo:** `backend/app/instagram_service.py`

```python
"""
Serviço para postar devocionais no Instagram
"""
import logging
import requests
from typing import Optional, Dict
from app.config import settings

logger = logging.getLogger(__name__)


class InstagramService:
    """Serviço para integração com Instagram Graph API"""
    
    def __init__(self):
        self.api_version = "v18.0"
        self.base_url = f"https://graph.facebook.com/{self.api_version}"
        self.access_token = settings.INSTAGRAM_ACCESS_TOKEN
        self.instagram_account_id = settings.INSTAGRAM_ACCOUNT_ID
    
    def create_image_caption(self, devocional_text: str, max_length: int = 2200) -> str:
        """
        Cria legenda para Instagram baseada no devocional
        
        Args:
            devocional_text: Texto do devocional
            max_length: Tamanho máximo da legenda (Instagram: 2200 caracteres)
        
        Returns:
            Legenda formatada para Instagram
        """
        # Remover emojis de WhatsApp que não funcionam bem no Instagram
        # Adaptar formatação
        # Adicionar hashtags relevantes
        
        caption = devocional_text[:max_length]
        
        # Adicionar hashtags
        hashtags = "#devocional #palavra #jesus #biblia #fe #cristo"
        if len(caption) + len(hashtags) + 1 <= max_length:
            caption = f"{caption}\n\n{hashtags}"
        
        return caption
    
    def upload_image(self, image_url: str) -> Optional[str]:
        """
        Faz upload de imagem para Instagram
        
        Args:
            image_url: URL da imagem ou caminho local
        
        Returns:
            Container ID ou None se falhar
        """
        try:
            # Passo 1: Criar container
            url = f"{self.base_url}/{self.instagram_account_id}/media"
            
            params = {
                "image_url": image_url,
                "caption": "Uploading...",  # Será atualizado depois
                "access_token": self.access_token
            }
            
            response = requests.post(url, params=params)
            response.raise_for_status()
            
            container_id = response.json().get("id")
            logger.info(f"Container criado: {container_id}")
            
            return container_id
        
        except Exception as e:
            logger.error(f"Erro ao fazer upload de imagem: {e}")
            return None
    
    def publish_post(self, container_id: str, caption: str) -> Optional[Dict]:
        """
        Publica post no Instagram
        
        Args:
            container_id: ID do container criado
            caption: Legenda do post
        
        Returns:
            Dados do post publicado ou None se falhar
        """
        try:
            url = f"{self.base_url}/{self.instagram_account_id}/media_publish"
            
            params = {
                "creation_id": container_id,
                "access_token": self.access_token
            }
            
            response = requests.post(url, params=params)
            response.raise_for_status()
            
            media_id = response.json().get("id")
            
            # Atualizar legenda
            if media_id:
                self.update_caption(media_id, caption)
            
            logger.info(f"Post publicado: {media_id}")
            
            return {
                "media_id": media_id,
                "success": True
            }
        
        except Exception as e:
            logger.error(f"Erro ao publicar post: {e}")
            return None
    
    def update_caption(self, media_id: str, caption: str) -> bool:
        """
        Atualiza legenda do post
        
        Args:
            media_id: ID do post
            caption: Nova legenda
        """
        try:
            url = f"{self.base_url}/{media_id}"
            
            params = {
                "caption": caption,
                "access_token": self.access_token
            }
            
            response = requests.post(url, params=params)
            response.raise_for_status()
            
            return True
        
        except Exception as e:
            logger.error(f"Erro ao atualizar legenda: {e}")
            return False
    
    def post_devocional(
        self,
        devocional_text: str,
        image_url: Optional[str] = None
    ) -> Dict:
        """
        Posta devocional completo no Instagram
        
        Args:
            devocional_text: Texto do devocional
            image_url: URL da imagem (opcional)
        
        Returns:
            Resultado do post
        """
        try:
            # Criar legenda
            caption = self.create_image_caption(devocional_text)
            
            # Se não tiver imagem, usar imagem padrão ou texto apenas
            if not image_url:
                # Opção: Gerar imagem com texto usando biblioteca (Pillow, etc)
                # Ou usar imagem padrão
                image_url = settings.INSTAGRAM_DEFAULT_IMAGE_URL
            
            # Upload de imagem
            container_id = self.upload_image(image_url)
            if not container_id:
                return {
                    "success": False,
                    "error": "Falha ao fazer upload de imagem"
                }
            
            # Publicar
            result = self.publish_post(container_id, caption)
            
            if result:
                return {
                    "success": True,
                    "media_id": result.get("media_id"),
                    "message": "Devocional postado com sucesso no Instagram"
                }
            else:
                return {
                    "success": False,
                    "error": "Falha ao publicar post"
                }
        
        except Exception as e:
            logger.error(f"Erro ao postar devocional: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }
```

#### **3. Configurações (.env)**

```env
# Instagram Integration
INSTAGRAM_ENABLED=true
INSTAGRAM_ACCESS_TOKEN=seu_token_aqui
INSTAGRAM_ACCOUNT_ID=seu_account_id
INSTAGRAM_DEFAULT_IMAGE_URL=https://exemplo.com/imagem-padrao.jpg
INSTAGRAM_AUTO_POST=true  # Postar automaticamente quando receber devocional
```

#### **4. Integração no Router**

**Arquivo:** `backend/app/routers/devocional.py`

```python
from app.instagram_service import InstagramService

instagram_service = InstagramService()

@router.post("/webhook")
async def receive_devocional_webhook(...):
    # ... código existente para salvar devocional ...
    
    # Se Instagram estiver habilitado e auto-post ativo
    if settings.INSTAGRAM_ENABLED and settings.INSTAGRAM_AUTO_POST:
        try:
            result = instagram_service.post_devocional(
                devocional_text=content,
                image_url=None  # Ou URL de imagem se disponível
            )
            
            if result.get("success"):
                logger.info(f"Devocional postado no Instagram: {result.get('media_id')}")
            else:
                logger.warning(f"Falha ao postar no Instagram: {result.get('error')}")
        
        except Exception as e:
            logger.error(f"Erro ao postar no Instagram: {e}")
            # Não falhar o webhook se Instagram falhar
    
    return {"success": True, ...}
```

#### **5. Endpoint Manual**

```python
@router.post("/{devocional_id}/post-instagram")
async def post_to_instagram(
    devocional_id: int,
    db: Session = Depends(get_db)
):
    """Posta devocional específico no Instagram"""
    devocional = db.query(Devocional).filter(
        Devocional.id == devocional_id
    ).first()
    
    if not devocional:
        raise HTTPException(status_code=404, detail="Devocional não encontrado")
    
    result = instagram_service.post_devocional(devocional.content)
    
    return result
```

---

### 📱 Opção 3: Via n8n (Workflow)

**Configuração no n8n:**

1. **Após receber devocional:**
   - Nó: HTTP Request (recebe webhook)
   - Nó: Instagram Graph API (postar)

2. **Workflow:**
```
Schedule Trigger (03:30)
    ↓
Buscar Contexto
    ↓
Gerar Devocional (IA)
    ↓
Enviar Webhook API (salvar)
    ↓
Instagram Graph API (postar)
```

**Vantagens:**
- ✅ Tudo em um lugar (n8n)
- ✅ Fácil de visualizar
- ✅ Pode adicionar lógica extra

---

## 🎯 RECOMENDAÇÃO FINAL

### **Para Blindagem WhatsApp:**

**Prioridade Alta:**
1. ✅ Variação de Delay Aleatório
2. ✅ Pausas Estratégicas
3. ✅ Janelas de Envio Inteligentes

**Prioridade Média:**
4. ✅ Análise de Taxa de Resposta
5. ✅ Limites Adaptativos
6. ✅ Detecção de Bloqueio Proativo

**Prioridade Baixa:**
7. ✅ Rotação de Conteúdo
8. ✅ Template de Mensagens Variados

### **Para Instagram:**

**Recomendação:** Começar com **Opção 1 (n8n)** para testar, depois implementar **Opção 2 (Sistema)** para automação completa.

---

## 📝 PRÓXIMOS PASSOS

1. **Implementar ferramentas de blindagem prioritárias**
2. **Configurar Instagram Graph API**
3. **Testar integração Instagram via n8n**
4. **Implementar postagem automática no sistema**
5. **Adicionar no frontend controle de postagem Instagram**

---

**Tudo pronto para implementar!** 🚀

