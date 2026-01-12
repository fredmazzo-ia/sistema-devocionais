"""
Utilitários para timezone - sempre usa horário de Brasília (America/Sao_Paulo)
"""
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional

# Timezone padrão do sistema
BRAZIL_TZ = ZoneInfo("America/Sao_Paulo")


def now_brazil() -> datetime:
    """
    Retorna datetime atual no horário de Brasília (America/Sao_Paulo)
    Use esta função em vez de datetime.now() ou datetime.utcnow()
    """
    return datetime.now(BRAZIL_TZ)


def to_brazil_timezone(dt: datetime) -> datetime:
    """
    Converte um datetime para timezone de Brasília
    Se não tiver timezone, assume que é UTC
    """
    if dt.tzinfo is None:
        # Se não tem timezone, assume UTC
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))
    
    return dt.astimezone(BRAZIL_TZ)


def today_brazil() -> datetime:
    """
    Retorna data de hoje no horário de Brasília (meia-noite)
    """
    now = now_brazil()
    return now.replace(hour=0, minute=0, second=0, microsecond=0)
