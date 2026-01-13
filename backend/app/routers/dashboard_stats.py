"""
Endpoint robusto de estatísticas do Dashboard
Extrai métricas reais do banco de dados
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, case
from typing import Dict, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
from app.database import (
    get_db,
    DevocionalEnvio,
    DevocionalContato,
    Devocional,
    ContactConsent,
    WebhookEvent,
    ContactEngagement,
    EvolutionInstanceConfig
)
from app.timezone_utils import now_brazil_naive
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


class DashboardStatsResponse(BaseModel):
    """Resposta com todas as estatísticas do dashboard"""
    
    # Mensagens
    messages: Dict
    # Contatos
    contacts: Dict
    # Consentimentos
    consents: Dict
    # Devocionais
    devocionais: Dict
    # Webhooks
    webhooks: Dict
    # Engajamento
    engagement: Dict
    # Instâncias
    instances: Dict
    # Períodos (hoje, semana, mês)
    periods: Dict


@router.get("/stats", response_model=DashboardStatsResponse)
async def get_dashboard_stats(
    db: Session = Depends(get_db)
):
    """
    Retorna estatísticas completas do dashboard extraídas do banco de dados
    """
    try:
        now = now_brazil_naive()
        today_start = datetime.combine(now.date(), datetime.min.time())
        week_start = today_start - timedelta(days=7)
        month_start = today_start - timedelta(days=30)
        
        # ============================================
        # MENSAGENS (devocional_envios)
        # ============================================
        
        # Total geral
        total_messages = db.query(func.count(DevocionalEnvio.id)).scalar() or 0
        
        # Por status
        messages_by_status = db.query(
            DevocionalEnvio.status,
            func.count(DevocionalEnvio.id).label('count')
        ).group_by(DevocionalEnvio.status).all()
        
        status_counts = {status: count for status, count in messages_by_status}
        
        # Por message_status (sent, delivered, read)
        messages_by_message_status = db.query(
            DevocionalEnvio.message_status,
            func.count(DevocionalEnvio.id).label('count')
        ).group_by(DevocionalEnvio.message_status).all()
        
        message_status_counts = {status: count for status, count in messages_by_message_status}
        
        # Mensagens enviadas (status = 'sent')
        total_sent = status_counts.get('sent', 0)
        
        # Mensagens entregues (message_status = 'delivered' ou 'read')
        total_delivered = message_status_counts.get('delivered', 0) + message_status_counts.get('read', 0)
        
        # Mensagens lidas (message_status = 'read')
        total_read = message_status_counts.get('read', 0)
        
        # Mensagens falhadas (status = 'failed')
        total_failed = status_counts.get('failed', 0)
        
        # Mensagens bloqueadas (status = 'blocked')
        total_blocked = status_counts.get('blocked', 0)
        
        # Retries
        total_retries = db.query(func.sum(DevocionalEnvio.retry_count)).scalar() or 0
        
        # Taxa de entrega
        delivery_rate = (total_delivered / total_sent * 100) if total_sent > 0 else 0.0
        
        # Taxa de leitura
        read_rate = (total_read / total_sent * 100) if total_sent > 0 else 0.0
        
        # Taxa de sucesso
        success_rate = ((total_sent - total_failed - total_blocked) / total_sent * 100) if total_sent > 0 else 0.0
        
        # Por período
        messages_today = db.query(func.count(DevocionalEnvio.id)).filter(
            DevocionalEnvio.sent_at >= today_start
        ).scalar() or 0
        
        messages_week = db.query(func.count(DevocionalEnvio.id)).filter(
            DevocionalEnvio.sent_at >= week_start
        ).scalar() or 0
        
        messages_month = db.query(func.count(DevocionalEnvio.id)).filter(
            DevocionalEnvio.sent_at >= month_start
        ).scalar() or 0
        
        # Última mensagem enviada
        last_message = db.query(DevocionalEnvio).order_by(
            DevocionalEnvio.sent_at.desc()
        ).first()
        
        messages_data = {
            "total": total_messages,
            "sent": total_sent,
            "delivered": total_delivered,
            "read": total_read,
            "failed": total_failed,
            "blocked": total_blocked,
            "retries": int(total_retries),
            "delivery_rate": round(delivery_rate, 2),
            "read_rate": round(read_rate, 2),
            "success_rate": round(success_rate, 2),
            "today": messages_today,
            "week": messages_week,
            "month": messages_month,
            "last_sent_at": last_message.sent_at.isoformat() if last_message else None,
            "by_status": status_counts,
            "by_message_status": message_status_counts
        }
        
        # ============================================
        # CONTATOS (devocional_contatos)
        # ============================================
        
        total_contacts = db.query(func.count(DevocionalContato.id)).scalar() or 0
        
        active_contacts = db.query(func.count(DevocionalContato.id)).filter(
            DevocionalContato.active == True
        ).scalar() or 0
        
        inactive_contacts = total_contacts - active_contacts
        
        # Contatos que receberam mensagens
        contacts_with_messages = db.query(
            func.count(func.distinct(DevocionalEnvio.recipient_phone))
        ).scalar() or 0
        
        # Contatos novos hoje/semana/mês
        contacts_today = db.query(func.count(DevocionalContato.id)).filter(
            DevocionalContato.created_at >= today_start
        ).scalar() or 0
        
        contacts_week = db.query(func.count(DevocionalContato.id)).filter(
            DevocionalContato.created_at >= week_start
        ).scalar() or 0
        
        contacts_month = db.query(func.count(DevocionalContato.id)).filter(
            DevocionalContato.created_at >= month_start
        ).scalar() or 0
        
        contacts_data = {
            "total": total_contacts,
            "active": active_contacts,
            "inactive": inactive_contacts,
            "with_messages": contacts_with_messages,
            "today": contacts_today,
            "week": contacts_week,
            "month": contacts_month
        }
        
        # ============================================
        # CONSENTIMENTOS (contact_consent)
        # ============================================
        
        total_consents = db.query(func.count(ContactConsent.id)).scalar() or 0
        
        consents_accepted = db.query(func.count(ContactConsent.id)).filter(
            ContactConsent.consented == True
        ).scalar() or 0
        
        consents_denied = db.query(func.count(ContactConsent.id)).filter(
            ContactConsent.consented == False
        ).scalar() or 0
        
        consents_pending = db.query(func.count(ContactConsent.id)).filter(
            ContactConsent.consented == None
        ).scalar() or 0
        
        # Consentimentos com mensagem enviada mas sem resposta
        consents_awaiting_response = db.query(func.count(ContactConsent.id)).filter(
            and_(
                ContactConsent.consent_message_sent == True,
                ContactConsent.response_received == False,
                ContactConsent.consented == None
            )
        ).scalar() or 0
        
        consents_data = {
            "total": total_consents,
            "accepted": consents_accepted,
            "denied": consents_denied,
            "pending": consents_pending,
            "awaiting_response": consents_awaiting_response,
            "acceptance_rate": round((consents_accepted / total_consents * 100) if total_consents > 0 else 0.0, 2)
        }
        
        # ============================================
        # DEVOCIONAIS (devocionais)
        # ============================================
        
        total_devocionais = db.query(func.count(Devocional.id)).scalar() or 0
        
        devocionais_sent = db.query(func.count(Devocional.id)).filter(
            Devocional.sent == True
        ).scalar() or 0
        
        devocionais_pending = total_devocionais - devocionais_sent
        
        # Devocionais criados hoje/semana/mês
        devocionais_today = db.query(func.count(Devocional.id)).filter(
            Devocional.created_at >= today_start
        ).scalar() or 0
        
        devocionais_week = db.query(func.count(Devocional.id)).filter(
            Devocional.created_at >= week_start
        ).scalar() or 0
        
        devocionais_month = db.query(func.count(Devocional.id)).filter(
            Devocional.created_at >= month_start
        ).scalar() or 0
        
        # Último devocional criado
        last_devocional = db.query(Devocional).order_by(
            Devocional.created_at.desc()
        ).first()
        
        devocionais_data = {
            "total": total_devocionais,
            "sent": devocionais_sent,
            "pending": devocionais_pending,
            "today": devocionais_today,
            "week": devocionais_week,
            "month": devocionais_month,
            "last_created_at": last_devocional.created_at.isoformat() if last_devocional else None
        }
        
        # ============================================
        # WEBHOOKS (webhook_events)
        # ============================================
        
        total_webhooks = db.query(func.count(WebhookEvent.id)).scalar() or 0
        
        webhooks_processed = db.query(func.count(WebhookEvent.id)).filter(
            WebhookEvent.processed == True
        ).scalar() or 0
        
        webhooks_pending = total_webhooks - webhooks_processed
        
        # Por tipo de evento
        webhooks_by_type = db.query(
            WebhookEvent.event_type,
            func.count(WebhookEvent.id).label('count')
        ).group_by(WebhookEvent.event_type).all()
        
        webhooks_by_type_dict = {event_type: count for event_type, count in webhooks_by_type}
        
        # Webhooks hoje/semana/mês
        webhooks_today = db.query(func.count(WebhookEvent.id)).filter(
            WebhookEvent.received_at >= today_start
        ).scalar() or 0
        
        webhooks_week = db.query(func.count(WebhookEvent.id)).filter(
            WebhookEvent.received_at >= week_start
        ).scalar() or 0
        
        webhooks_month = db.query(func.count(WebhookEvent.id)).filter(
            WebhookEvent.received_at >= month_start
        ).scalar() or 0
        
        # Último webhook recebido
        last_webhook = db.query(WebhookEvent).order_by(
            WebhookEvent.received_at.desc()
        ).first()
        
        webhooks_data = {
            "total": total_webhooks,
            "processed": webhooks_processed,
            "pending": webhooks_pending,
            "processing_rate": round((webhooks_processed / total_webhooks * 100) if total_webhooks > 0 else 0.0, 2),
            "today": webhooks_today,
            "week": webhooks_week,
            "month": webhooks_month,
            "by_type": webhooks_by_type_dict,
            "last_received_at": last_webhook.received_at.isoformat() if last_webhook else None
        }
        
        # ============================================
        # ENGAJAMENTO (contact_engagement)
        # ============================================
        
        total_engagement_records = db.query(func.count(ContactEngagement.id)).scalar() or 0
        
        if total_engagement_records > 0:
            avg_engagement_score = db.query(func.avg(ContactEngagement.engagement_score)).scalar() or 0.0
            avg_engagement_score = round(float(avg_engagement_score), 2)
            
            # Total de respostas
            total_responses = db.query(func.sum(ContactEngagement.total_responded)).scalar() or 0
            
            # Total de lidas
            total_read_engagement = db.query(func.sum(ContactEngagement.total_read)).scalar() or 0
            
            # Total de entregues
            total_delivered_engagement = db.query(func.sum(ContactEngagement.total_delivered)).scalar() or 0
            
            # Contatos com baixo engajamento (score < 30)
            low_engagement = db.query(func.count(ContactEngagement.id)).filter(
                ContactEngagement.engagement_score < 30.0
            ).scalar() or 0
            
            # Contatos com alto engajamento (score >= 70)
            high_engagement = db.query(func.count(ContactEngagement.id)).filter(
                ContactEngagement.engagement_score >= 70.0
            ).scalar() or 0
        else:
            avg_engagement_score = 0.0
            total_responses = 0
            total_read_engagement = 0
            total_delivered_engagement = 0
            low_engagement = 0
            high_engagement = 0
        
        engagement_data = {
            "total_records": total_engagement_records,
            "avg_score": avg_engagement_score,
            "total_responses": int(total_responses),
            "total_read": int(total_read_engagement),
            "total_delivered": int(total_delivered_engagement),
            "low_engagement_count": low_engagement,
            "high_engagement_count": high_engagement
        }
        
        # ============================================
        # INSTÂNCIAS (evolution_instance_configs)
        # ============================================
        
        total_instances = db.query(func.count(EvolutionInstanceConfig.id)).scalar() or 0
        
        active_instances = db.query(func.count(EvolutionInstanceConfig.id)).filter(
            and_(
                EvolutionInstanceConfig.enabled == True,
                EvolutionInstanceConfig.status == 'active'
            )
        ).scalar() or 0
        
        inactive_instances = db.query(func.count(EvolutionInstanceConfig.id)).filter(
            EvolutionInstanceConfig.status == 'inactive'
        ).scalar() or 0
        
        error_instances = db.query(func.count(EvolutionInstanceConfig.id)).filter(
            EvolutionInstanceConfig.status == 'error'
        ).scalar() or 0
        
        # Total de mensagens enviadas hoje por todas as instâncias
        total_messages_today_instances = db.query(
            func.sum(EvolutionInstanceConfig.messages_sent_today)
        ).scalar() or 0
        
        # Total de mensagens enviadas nesta hora
        total_messages_hour_instances = db.query(
            func.sum(EvolutionInstanceConfig.messages_sent_this_hour)
        ).scalar() or 0
        
        instances_data = {
            "total": total_instances,
            "active": active_instances,
            "inactive": inactive_instances,
            "error": error_instances,
            "messages_today": int(total_messages_today_instances),
            "messages_this_hour": int(total_messages_hour_instances)
        }
        
        # ============================================
        # RESUMO POR PERÍODO
        # ============================================
        
        periods_data = {
            "today": {
                "messages": messages_today,
                "contacts": contacts_today,
                "devocionais": devocionais_today,
                "webhooks": webhooks_today
            },
            "week": {
                "messages": messages_week,
                "contacts": contacts_week,
                "devocionais": devocionais_week,
                "webhooks": webhooks_week
            },
            "month": {
                "messages": messages_month,
                "contacts": contacts_month,
                "devocionais": devocionais_month,
                "webhooks": webhooks_month
            }
        }
        
        return DashboardStatsResponse(
            messages=messages_data,
            contacts=contacts_data,
            consents=consents_data,
            devocionais=devocionais_data,
            webhooks=webhooks_data,
            engagement=engagement_data,
            instances=instances_data,
            periods=periods_data
        )
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas do dashboard: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro ao obter estatísticas: {str(e)}")
