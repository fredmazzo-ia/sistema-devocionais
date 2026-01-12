"""
Webhook para receber eventos da Evolution API
Status de mensagens: sent, delivered, read, etc.
"""
from fastapi import APIRouter, Request, HTTPException, Header, Depends
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel
from app.database import get_db, DevocionalEnvio
from app.shield_service import ShieldService
from app.config import settings
import logging
import json

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhook/evolution", tags=["webhook-evolution"])


class EvolutionWebhookEvent(BaseModel):
    """Modelo para eventos do webhook da Evolution API"""
    event: str  # message.ack, qrcode.updated, etc.
    instance: str  # Nome da instância
    data: Dict[str, Any]  # Dados do evento


@router.post("/message-status")
async def receive_message_status(
    request: Request,
    db: Session = Depends(get_db),
    x_webhook_secret: Optional[str] = Header(None, alias="X-Webhook-Secret")
):
    """
    Webhook para receber status de mensagens da Evolution API
    
    Eventos suportados:
    - message.ack: Confirmação de envio (sent, delivered, read)
    
    A Evolution API envia eventos quando:
    - Mensagem é enviada (ack: sent)
    - Mensagem é entregue (ack: delivered)
    - Mensagem é lida (ack: read)
    
    Formato esperado da Evolution API:
    {
        "event": "message.ack",
        "instance": "nome-instancia",
        "data": {
            "key": {
                "id": "message_id",
                "remoteJid": "5516999999999@s.whatsapp.net"
            },
            "ack": 1,  # 1=sent, 2=delivered, 3=read
            "timestamp": 1234567890
        }
    }
    """
    try:
        # Verificar secret se configurado
        if settings.DEVOCIONAL_WEBHOOK_SECRET:
            if not x_webhook_secret or x_webhook_secret != settings.DEVOCIONAL_WEBHOOK_SECRET:
                raise HTTPException(status_code=401, detail="Webhook secret inválido")
        
        # Obter dados do request
        try:
            body = await request.json()
        except Exception as e:
            logger.error(f"Erro ao parsear JSON do webhook: {e}")
            raise HTTPException(status_code=400, detail="JSON inválido")
        
        event = body.get("event", "")
        instance_name = body.get("instance", "")
        data = body.get("data", {})
        
        logger.info(f"Webhook recebido: event={event}, instance={instance_name}")
        
        # Processar apenas eventos de status de mensagem
        if event == "message.ack":
            await process_message_ack(db, instance_name, data)
        else:
            logger.debug(f"Evento ignorado: {event}")
        
        return {"success": True, "message": "Webhook processado"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao processar webhook da Evolution API: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")


async def process_message_ack(
    db: Session,
    instance_name: str,
    data: Dict[str, Any]
):
    """
    Processa evento de confirmação de mensagem (ACK)
    
    Args:
        db: Sessão do banco de dados
        instance_name: Nome da instância
        data: Dados do evento
    """
    try:
        # Extrair informações
        key = data.get("key", {})
        message_id = key.get("id")
        remote_jid = key.get("remoteJid", "")
        ack = data.get("ack", 0)  # 1=sent, 2=delivered, 3=read
        timestamp = data.get("timestamp")
        
        if not message_id:
            logger.warning("Webhook sem message_id, ignorando")
            return
        
        # Extrair telefone do remoteJid (formato: 5516999999999@s.whatsapp.net)
        phone = remote_jid.split("@")[0] if "@" in remote_jid else remote_jid
        
        # Buscar envio pelo message_id
        envio = db.query(DevocionalEnvio).filter(
            DevocionalEnvio.message_id == message_id
        ).first()
        
        if not envio:
            logger.debug(f"Envio não encontrado para message_id: {message_id}")
            return
        
        # Converter timestamp para datetime
        from app.timezone_utils import now_brazil_naive
        if timestamp:
            try:
                # Timestamp pode estar em segundos ou milissegundos
                if timestamp > 10**10:
                    timestamp = timestamp / 1000  # Converter de milissegundos
                event_time = datetime.fromtimestamp(timestamp)
            except:
                event_time = now_brazil_naive()
        else:
            event_time = now_brazil_naive()
        
        # Atualizar status baseado no ACK
        # ACK 1 = sent (enviado)
        # ACK 2 = delivered (entregue)
        # ACK 3 = read (lido/visualizado)
        
        updated = False
        
        if ack == 1:  # Sent
            if envio.message_status != "sent":
                envio.message_status = "sent"
                envio.status = "sent"
                updated = True
                logger.info(f"Mensagem {message_id} enviada para {phone}")
        
        elif ack == 2:  # Delivered
            if envio.message_status != "delivered":
                envio.message_status = "delivered"
                envio.delivered_at = event_time
                updated = True
                logger.info(f"Mensagem {message_id} entregue para {phone}")
        
        elif ack == 3:  # Read
            if envio.message_status != "read":
                envio.message_status = "read"
                envio.read_at = event_time
                # Se ainda não tinha delivered_at, marcar também
                if not envio.delivered_at:
                    envio.delivered_at = event_time
                updated = True
                logger.info(f"Mensagem {message_id} lida por {phone}")
                
                # Atualizar engajamento no ShieldService
                # Buscar instância do ShieldService (precisa ser injetada ou global)
                # Por enquanto, vamos atualizar via contato
                update_engagement_from_read(db, phone, True)
        
        if updated:
            db.commit()
            logger.debug(f"Status atualizado para message_id {message_id}: ack={ack}")
    
    except Exception as e:
        logger.error(f"Erro ao processar message.ack: {e}", exc_info=True)
        db.rollback()
        raise


def update_engagement_from_read(db: Session, phone: str, was_read: bool):
    """
    Atualiza score de engajamento baseado em visualização
    
    Args:
        db: Sessão do banco de dados
        phone: Número do telefone
        was_read: Se a mensagem foi lida
    """
    try:
        # Buscar serviço de devocionais para acessar o ShieldService
        # Criar instância do DevocionalServiceV2 que contém o ShieldService
        from app.devocional_service_v2 import DevocionalServiceV2
        
        devocional_service = DevocionalServiceV2(db=db)
        
        # Atualizar engajamento via ShieldService
        if devocional_service.shield:
            # Atualizar engajamento baseado em visualização
            devocional_service.shield.update_engagement(
                phone=phone,
                responded=False,  # Não é resposta, é visualização
                is_devocional=True,
                was_read=was_read
            )
            
            if was_read and phone in devocional_service.shield.engagement_data:
                data = devocional_service.shield.engagement_data[phone]
                logger.info(f"Engajamento atualizado para {phone}: score={data.engagement_score:.2f} (visualizou)")
        else:
            logger.warning("ShieldService não está habilitado, não é possível atualizar engajamento")
    
    except Exception as e:
        logger.error(f"Erro ao atualizar engajamento: {e}", exc_info=True)


@router.get("/test")
async def test_webhook():
    """Endpoint de teste para verificar se o webhook está acessível"""
    return {
        "success": True,
        "message": "Webhook da Evolution API está funcionando",
        "endpoint": "/webhook/evolution/message-status",
        "instructions": "Configure este endpoint na Evolution API como webhook para receber eventos de status de mensagens"
    }
