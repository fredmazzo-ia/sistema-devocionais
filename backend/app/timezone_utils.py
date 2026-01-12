"""
Utilitários para timezone - sempre usa horário de Brasília (America/Sao_Paulo)
"""
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional

# Timezone padrão do sistema
BRAZIL_TZ = ZoneInfo("America/Sao_Paulo")
UTC_TZ = ZoneInfo("UTC")


def now_brazil() -> datetime:
    """
    Retorna datetime atual no horário de Brasília (America/Sao_Paulo)
    Use esta função em vez de datetime.now() ou datetime.utcnow()
    """
    return datetime.now(BRAZIL_TZ)


def now_brazil_naive() -> datetime:
    """
    Retorna datetime atual no horário de Brasília SEM timezone (naive)
    Para salvar no PostgreSQL que armazena em UTC
    PostgreSQL vai converter automaticamente se o datetime for naive
    """
    return datetime.now(BRAZIL_TZ).replace(tzinfo=None)


def to_brazil_timezone(dt: datetime) -> datetime:
    """
    Converte um datetime para timezone de Brasília
    Se não tiver timezone, assume que é UTC
    """
    if dt.tzinfo is None:
        # Se não tem timezone, assume UTC
        dt = dt.replace(tzinfo=UTC_TZ)
    
    return dt.astimezone(BRAZIL_TZ)


def from_utc_to_brazil(utc_dt: datetime) -> datetime:
    """
    Converte um datetime UTC para horário de Brasília
    """
    if utc_dt.tzinfo is None:
        # Se não tem timezone, assume que já é UTC
        utc_dt = utc_dt.replace(tzinfo=UTC_TZ)
    return utc_dt.astimezone(BRAZIL_TZ)


def today_brazil() -> datetime:
    """
    Retorna data de hoje no horário de Brasília (meia-noite)
    """
    now = now_brazil()
    return now.replace(hour=0, minute=0, second=0, microsecond=0)


def today_brazil_naive() -> datetime:
    """
    Retorna data de hoje no horário de Brasília (meia-noite) SEM timezone
    Para salvar no PostgreSQL
    """
    now = now_brazil()
    return now.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
