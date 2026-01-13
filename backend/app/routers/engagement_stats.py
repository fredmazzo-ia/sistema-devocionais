"""
Endpoints para visualizar estatísticas de engajamento
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.database import get_db, DevocionalEnvio, DevocionalContato
from app.devocional_service_v2 import DevocionalServiceV2
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/engagement", tags=["engagement"])


class EngagementStatsResponse(BaseModel):
    """Estatísticas de engajamento de um contato"""
    phone: str
    name: Optional[str]
    total_sent: int
    total_delivered: int
    total_read: int
    delivery_rate: float  # % de entregues
    read_rate: float  # % de lidas
    engagement_score: float  # Score calculado (0.0 a 1.0)
    last_sent: Optional[str]
    last_read: Optional[str]
    consecutive_not_read: int  # Quantas mensagens seguidas não foram lidas


@router.get("/stats", response_model=List[EngagementStatsResponse])
async def get_engagement_stats(
    days: int = 30,
    min_score: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """
    Retorna estatísticas de engajamento de todos os contatos
    
    Args:
        days: Período em dias para análise (padrão: 30)
        min_score: Filtrar apenas contatos com score >= min_score
    """
    try:
        # Calcular data limite
        from app.timezone_utils import now_brazil_naive
        date_limit = now_brazil_naive() - timedelta(days=days)
        
        # Buscar todos os contatos
        contatos = db.query(DevocionalContato).all()
        
        stats_list = []
        
        for contato in contatos:
            # Buscar envios do contato no período
            envios = db.query(DevocionalEnvio).filter(
                DevocionalEnvio.recipient_phone == contato.phone,
                DevocionalEnvio.sent_at >= date_limit
            ).all()
            
            total_sent = len(envios)
            total_delivered = sum(1 for e in envios if e.message_status in ['delivered', 'read'])
            total_read = sum(1 for e in envios if e.message_status == 'read')
            
            delivery_rate = (total_delivered / total_sent * 100) if total_sent > 0 else 0.0
            read_rate = (total_read / total_sent * 100) if total_sent > 0 else 0.0
            
            # Calcular score de engajamento baseado em visualizações
            # Score = taxa de leitura (0.0 a 1.0)
            engagement_score = read_rate / 100.0 if total_sent > 0 else 0.5
            
            # Contar mensagens consecutivas não lidas
            consecutive_not_read = 0
            for envio in reversed(envios):  # Do mais recente para o mais antigo
                if envio.message_status != 'read':
                    consecutive_not_read += 1
                else:
                    break
            
            # Filtrar por score mínimo se especificado
            if min_score is not None and engagement_score < min_score:
                continue
            
            # Último envio e última leitura
            last_sent = max((e.sent_at for e in envios), default=None)
            last_read = max((e.read_at for e in envios if e.read_at), default=None)
            
            stats_list.append(EngagementStatsResponse(
                phone=contato.phone,
                name=contato.name,
                total_sent=total_sent,
                total_delivered=total_delivered,
                total_read=total_read,
                delivery_rate=round(delivery_rate, 2),
                read_rate=round(read_rate, 2),
                engagement_score=round(engagement_score, 3),
                last_sent=last_sent.isoformat() if last_sent else None,
                last_read=last_read.isoformat() if last_read else None,
                consecutive_not_read=consecutive_not_read
            ))
        
        # Ordenar por score (maior primeiro)
        stats_list.sort(key=lambda x: x.engagement_score, reverse=True)
        
        return stats_list
    
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas de engajamento: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")


@router.get("/stats/{phone}", response_model=EngagementStatsResponse)
async def get_contact_engagement_stats(
    phone: str,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """
    Retorna estatísticas de engajamento de um contato específico
    """
    try:
        # Buscar contato
        contato = db.query(DevocionalContato).filter(
            DevocionalContato.phone == phone
        ).first()
        
        if not contato:
            raise HTTPException(status_code=404, detail=f"Contato {phone} não encontrado")
        
        # Calcular data limite
        from app.timezone_utils import now_brazil_naive
        date_limit = now_brazil_naive() - timedelta(days=days)
        
        # Buscar envios do contato no período
        envios = db.query(DevocionalEnvio).filter(
            DevocionalEnvio.recipient_phone == phone,
            DevocionalEnvio.sent_at >= date_limit
        ).all()
        
        total_sent = len(envios)
        total_delivered = sum(1 for e in envios if e.message_status in ['delivered', 'read'])
        total_read = sum(1 for e in envios if e.message_status == 'read')
        
        delivery_rate = (total_delivered / total_sent * 100) if total_sent > 0 else 0.0
        read_rate = (total_read / total_sent * 100) if total_sent > 0 else 0.0
        
        # Calcular score de engajamento
        engagement_score = read_rate / 100.0 if total_sent > 0 else 0.5
        
        # Contar mensagens consecutivas não lidas
        consecutive_not_read = 0
        for envio in reversed(envios):
            if envio.message_status != 'read':
                consecutive_not_read += 1
            else:
                break
        
        # Último envio e última leitura
        last_sent = max((e.sent_at for e in envios), default=None)
        last_read = max((e.read_at for e in envios if e.read_at), default=None)
        
        return EngagementStatsResponse(
            phone=contato.phone,
            name=contato.name,
            total_sent=total_sent,
            total_delivered=total_delivered,
            total_read=total_read,
            delivery_rate=round(delivery_rate, 2),
            read_rate=round(read_rate, 2),
            engagement_score=round(engagement_score, 3),
            last_sent=last_sent.isoformat() if last_sent else None,
            last_read=last_read.isoformat() if last_read else None,
            consecutive_not_read=consecutive_not_read
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas do contato: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")
