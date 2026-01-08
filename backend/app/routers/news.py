"""
Rotas para gerenciamento de notícias
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime

from app.database import get_db, NewsArticle
from app.schemas import NewsArticleResponse, NewsArticleCreate

router = APIRouter()


@router.get("/", response_model=List[NewsArticleResponse])
async def get_news(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    relevant_only: bool = Query(False),
    db: Session = Depends(get_db)
):
    """Lista todas as notícias"""
    query = db.query(NewsArticle)
    
    if relevant_only:
        query = query.filter(NewsArticle.is_relevant == True)
    
    articles = query.order_by(desc(NewsArticle.scraped_date)).offset(skip).limit(limit).all()
    return articles


@router.get("/{article_id}", response_model=NewsArticleResponse)
async def get_article(article_id: int, db: Session = Depends(get_db)):
    """Obtém uma notícia específica"""
    article = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="Notícia não encontrada")
    
    return article


@router.get("/relevant/count")
async def get_relevant_count(db: Session = Depends(get_db)):
    """Conta notícias relevantes"""
    count = db.query(NewsArticle).filter(NewsArticle.is_relevant == True).count()
    return {"count": count}


@router.post("/{article_id}/mark-processed")
async def mark_as_processed(article_id: int, db: Session = Depends(get_db)):
    """Marca uma notícia como processada"""
    article = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="Notícia não encontrada")
    
    article.processed = True
    db.commit()
    db.refresh(article)
    
    return {"message": "Notícia marcada como processada", "article": article}

