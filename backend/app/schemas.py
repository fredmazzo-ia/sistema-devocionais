"""
Schemas Pydantic para validação de dados
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NewsArticleBase(BaseModel):
    title: str
    content: Optional[str] = None
    url: str
    source: str
    published_date: Optional[datetime] = None


class NewsArticleCreate(NewsArticleBase):
    pass


class NewsArticleResponse(NewsArticleBase):
    id: int
    scraped_date: datetime
    is_relevant: bool
    relevance_score: int
    processed: bool
    notified: bool
    scope: Optional[str] = None
    responsible_area: Optional[str] = None
    
    class Config:
        from_attributes = True


class NotificationResponse(BaseModel):
    id: int
    article_id: int
    recipient_phone: str
    recipient_name: Optional[str] = None
    sent_at: datetime
    status: str
    message: Optional[str] = None
    
    class Config:
        from_attributes = True

