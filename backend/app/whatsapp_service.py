"""
Serviço de notificações via WhatsApp
"""
import logging
from typing import Dict, List, Optional
from app.config import settings

logger = logging.getLogger(__name__)


class WhatsAppService:
    """Classe para envio de notificações via WhatsApp"""
    
    def __init__(self):
        self.enabled = settings.WHATSAPP_ENABLED
        self.api_url = settings.WHATSAPP_API_URL
        self.api_key = settings.WHATSAPP_API_KEY
        self.phone_id = settings.WHATSAPP_PHONE_ID
    
    def format_notification_message(self, article: Dict, responsible: Dict) -> str:
        """
        Formata mensagem de notificação
        
        Args:
            article: Dados do artigo
            responsible: Dados do responsável
            
        Returns:
            Mensagem formatada
        """
        message = f"""🚨 *Nova Notícia Detectada - Assistência Social*

📰 *Título:* {article.get('title', 'N/A')}

📍 *Escopo:* {article.get('scope', 'Geral')}
🏢 *Área Responsável:* {article.get('responsible_area', 'N/A')}

📅 *Data:* {article.get('published_date', 'N/A')}
🔗 *Fonte:* {article.get('source', 'N/A')}

📋 *Resumo:*
{article.get('content', 'Sem resumo disponível')[:300]}...

🔗 *Link:* {article.get('url', 'N/A')}

---
*Responsável:* {responsible.get('name', 'N/A')}
*Área de Atuação:* {responsible.get('area', 'N/A')}
"""
        return message
    
    def send_notification(self, article: Dict, responsible: Dict) -> bool:
        """
        Envia notificação via WhatsApp
        
        Args:
            article: Dados do artigo
            responsible: Dados do responsável
            
        Returns:
            True se enviado com sucesso
        """
        if not self.enabled:
            logger.warning("WhatsApp não está habilitado nas configurações")
            return False
        
        try:
            message = self.format_notification_message(article, responsible)
            phone = responsible.get('phone')
            
            # Aqui você implementaria a chamada real à API do WhatsApp
            # Exemplo com WhatsApp Business API:
            # response = requests.post(
            #     f"{self.api_url}/messages",
            #     headers={"Authorization": f"Bearer {self.api_key}"},
            #     json={
            #         "messaging_product": "whatsapp",
            #         "to": phone,
            #         "type": "text",
            #         "text": {"body": message}
            #     }
            # )
            
            logger.info(f"Notificação enviada para {responsible.get('name')} ({phone})")
            logger.debug(f"Mensagem: {message[:100]}...")
            
            # Por enquanto, apenas log
            return True
            
        except Exception as e:
            logger.error(f"Erro ao enviar notificação WhatsApp: {e}")
            return False
    
    def notify_responsibles(self, article: Dict) -> List[Dict]:
        """
        Notifica todos os responsáveis relevantes
        
        Args:
            article: Dados do artigo
            
        Returns:
            Lista de resultados de notificação
        """
        results = []
        responsible_area = article.get('responsible_area')
        
        # Filtrar responsáveis pela área
        relevant_responsibles = [
            r for r in settings.RESPONSIBLES
            if r.get('area') == responsible_area or responsible_area == "Coordenação Geral"
        ]
        
        # Se não houver responsável específico, notificar todos
        if not relevant_responsibles:
            relevant_responsibles = settings.RESPONSIBLES
        
        for responsible in relevant_responsibles:
            success = self.send_notification(article, responsible)
            results.append({
                'responsible': responsible.get('name'),
                'phone': responsible.get('phone'),
                'success': success
            })
        
        return results

