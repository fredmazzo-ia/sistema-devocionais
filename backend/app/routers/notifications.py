"""
Rotas para gerenciamento de notificações
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List

from app.database import get_db, Notification, NewsArticle

router = APIRouter()


@router.get("/", response_model=List[dict])
async def get_notifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Lista todas as notificações"""
    notifications = db.query(Notification).order_by(
        desc(Notification.sent_at)
    ).offset(skip).limit(limit).all()
    
    result = []
    for notif in notifications:
        article = db.query(NewsArticle).filter(NewsArticle.id == notif.article_id).first()
        result.append({
            "id": notif.id,
            "article": {
                "id": article.id if article else None,
                "title": article.title if article else "Artigo não encontrado"
            },
            "recipient_name": notif.recipient_name,
            "recipient_phone": notif.recipient_phone,
            "status": notif.status,
            "sent_at": notif.sent_at
        })
    
    return result


@router.get("/stats")
async def get_notification_stats(db: Session = Depends(get_db)):
    """Estatísticas de notificações"""
    total = db.query(Notification).count()
    sent = db.query(Notification).filter(Notification.status == "sent").count()
    failed = db.query(Notification).filter(Notification.status == "failed").count()
    
    return {
        "total": total,
        "sent": sent,
        "failed": failed,
        "success_rate": (sent / total * 100) if total > 0 else 0
    }

