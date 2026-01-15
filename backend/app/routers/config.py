"""
Endpoints para gerenciar configurações do sistema
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, Field
from app.database import get_db, User, SystemConfig
from app.config import settings
from app.auth import get_current_user
from app.timezone_utils import now_brazil
import logging
import os

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/config", tags=["config"])


# Schemas
class ShieldConfigUpdate(BaseModel):
    enabled: Optional[bool] = None
    delay_variation: Optional[float] = Field(None, ge=0.0, le=1.0)
    break_interval: Optional[int] = Field(None, ge=1)
    break_duration_min: Optional[float] = Field(None, ge=0.0)
    break_duration_max: Optional[float] = Field(None, ge=0.0)
    min_engagement_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    adaptive_limits_enabled: Optional[bool] = None
    block_detection_enabled: Optional[bool] = None


class RateLimitConfigUpdate(BaseModel):
    delay_between_messages: Optional[float] = Field(None, ge=0.0)
    max_messages_per_hour: Optional[int] = Field(None, ge=1)
    max_messages_per_day: Optional[int] = Field(None, ge=1)
    max_retries: Optional[int] = Field(None, ge=0)
    retry_delay: Optional[float] = Field(None, ge=0.0)


class ScheduleConfigUpdate(BaseModel):
    send_time: Optional[str] = Field(None, pattern=r'^\d{2}:\d{2}$')


class ConfigResponse(BaseModel):
    shield: dict
    rate_limit: dict
    schedule: dict
    message: str


def _get_send_time_from_db(db: Session) -> str:
    """Helper para obter horário de envio do banco"""
    try:
        config = db.query(SystemConfig).filter(SystemConfig.key == "devocional_send_time").first()
        if config and config.value:
            return config.value
    except Exception as e:
        logger.warning(f"Erro ao buscar horário do banco: {e}. Usando padrão do .env")
    return settings.DEVOCIONAL_SEND_TIME


def _get_config_from_db(db: Session, key: str, default_value, value_type=str):
    """Helper para obter configuração do banco com fallback para .env"""
    try:
        db_config = db.query(SystemConfig).filter(SystemConfig.key == key).first()
        if db_config and db_config.value:
            if value_type == bool:
                return db_config.value.lower() == "true"
            elif value_type == int:
                return int(db_config.value)
            elif value_type == float:
                return float(db_config.value)
            else:
                return db_config.value
    except Exception as e:
        logger.debug(f"Erro ao buscar {key} do banco: {e}. Usando padrão do .env")
    return default_value


@router.get("/")
async def get_config(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retorna todas as configurações do sistema (lê do banco quando disponível)"""
    send_time = _get_send_time_from_db(db)
    now_sp = now_brazil()
    
    return {
        "shield": {
            "enabled": _get_config_from_db(db, "SHIELD_ENABLED", settings.SHIELD_ENABLED, bool),
            "delay_variation": _get_config_from_db(db, "DELAY_VARIATION", settings.DELAY_VARIATION, float),
            "break_interval": _get_config_from_db(db, "BREAK_INTERVAL", settings.BREAK_INTERVAL, int),
            "break_duration_min": _get_config_from_db(db, "BREAK_DURATION_MIN", settings.BREAK_DURATION_MIN, float),
            "break_duration_max": _get_config_from_db(db, "BREAK_DURATION_MAX", settings.BREAK_DURATION_MAX, float),
            "min_engagement_score": _get_config_from_db(db, "MIN_ENGAGEMENT_SCORE", settings.MIN_ENGAGEMENT_SCORE, float),
            "adaptive_limits_enabled": _get_config_from_db(db, "ADAPTIVE_LIMITS_ENABLED", settings.ADAPTIVE_LIMITS_ENABLED, bool),
            "block_detection_enabled": _get_config_from_db(db, "BLOCK_DETECTION_ENABLED", settings.BLOCK_DETECTION_ENABLED, bool),
        },
        "rate_limit": {
            "delay_between_messages": _get_config_from_db(db, "DELAY_BETWEEN_MESSAGES", settings.DELAY_BETWEEN_MESSAGES, float),
            "max_messages_per_hour": _get_config_from_db(db, "MAX_MESSAGES_PER_HOUR", settings.MAX_MESSAGES_PER_HOUR, int),
            "max_messages_per_day": _get_config_from_db(db, "MAX_MESSAGES_PER_DAY", settings.MAX_MESSAGES_PER_DAY, int),
            "max_retries": _get_config_from_db(db, "MAX_RETRIES", settings.MAX_RETRIES, int),
            "retry_delay": _get_config_from_db(db, "RETRY_DELAY", settings.RETRY_DELAY, float),
        },
        "schedule": {
            "send_time": send_time,
            "timezone": "America/Sao_Paulo",
            "timezone_note": "O horário informado é sempre interpretado como horário de São Paulo/Brasília",
            "current_time_sp": now_sp.strftime("%H:%M:%S"),
            "current_datetime_sp": now_sp.strftime("%Y-%m-%d %H:%M:%S %Z"),
        }
    }


@router.put("/shield")
async def update_shield_config(
    config: ShieldConfigUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Atualiza configurações de blindagem
    Salva no banco de dados para persistência
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Apenas administradores podem alterar configurações")
    
    updated_keys = []
    
    # Salvar no banco de dados (SystemConfig)
    config_map = {
        "enabled": "SHIELD_ENABLED",
        "delay_variation": "DELAY_VARIATION",
        "break_interval": "BREAK_INTERVAL",
        "break_duration_min": "BREAK_DURATION_MIN",
        "break_duration_max": "BREAK_DURATION_MAX",
        "min_engagement_score": "MIN_ENGAGEMENT_SCORE",
        "adaptive_limits_enabled": "ADAPTIVE_LIMITS_ENABLED",
        "block_detection_enabled": "BLOCK_DETECTION_ENABLED"
    }
    
    for field_name, config_key in config_map.items():
        value = getattr(config, field_name, None)
        if value is not None:
            # Buscar ou criar configuração no banco
            db_config = db.query(SystemConfig).filter(SystemConfig.key == config_key).first()
            if db_config:
                # Converter boolean para string
                str_value = str(value).lower() if isinstance(value, bool) else str(value)
                db_config.value = str_value
                db_config.updated_at = now_brazil()
            else:
                str_value = str(value).lower() if isinstance(value, bool) else str(value)
                db_config = SystemConfig(
                    key=config_key,
                    value=str_value,
                    description=f"Configuração de {field_name.replace('_', ' ').title()}"
                )
                db.add(db_config)
            
            # Também atualizar em memória para aplicar imediatamente
            os.environ[config_key] = str_value
            updated_keys.append(field_name)
    
    try:
        db.commit()
        logger.info(f"✅ Configurações de blindagem salvas no banco por {current_user.email}: {updated_keys}")
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Erro ao salvar configurações no banco: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro ao salvar configurações: {str(e)}")
    
    return {
        "message": "Configurações atualizadas e salvas no banco de dados.",
        "updated": {k: getattr(config, k) for k in updated_keys if getattr(config, k) is not None}
    }


@router.put("/rate-limit")
async def update_rate_limit_config(
    config: RateLimitConfigUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Atualiza configurações de rate limiting
    Salva no banco de dados para persistência
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Apenas administradores podem alterar configurações")
    
    updated_keys = []
    
    # Salvar no banco de dados (SystemConfig)
    config_map = {
        "delay_between_messages": "DELAY_BETWEEN_MESSAGES",
        "max_messages_per_hour": "MAX_MESSAGES_PER_HOUR",
        "max_messages_per_day": "MAX_MESSAGES_PER_DAY",
        "max_retries": "MAX_RETRIES",
        "retry_delay": "RETRY_DELAY"
    }
    
    for field_name, config_key in config_map.items():
        value = getattr(config, field_name, None)
        if value is not None:
            # Buscar ou criar configuração no banco
            db_config = db.query(SystemConfig).filter(SystemConfig.key == config_key).first()
            if db_config:
                db_config.value = str(value)
                db_config.updated_at = now_brazil()
            else:
                db_config = SystemConfig(
                    key=config_key,
                    value=str(value),
                    description=f"Configuração de {field_name.replace('_', ' ').title()}"
                )
                db.add(db_config)
            
            # Também atualizar em memória para aplicar imediatamente
            os.environ[config_key] = str(value)
            updated_keys.append(field_name)
    
    try:
        db.commit()
        logger.info(f"✅ Configurações de rate limiting salvas no banco por {current_user.email}: {updated_keys}")
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Erro ao salvar configurações no banco: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro ao salvar configurações: {str(e)}")
    
    return {
        "message": "Configurações atualizadas e salvas no banco de dados.",
        "updated": {k: getattr(config, k) for k in updated_keys if getattr(config, k) is not None}
    }


@router.put("/schedule")
async def update_schedule_config(
    config: ScheduleConfigUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Atualiza horário de envio automático (dinâmico - não precisa reiniciar)
    IMPORTANTE: O horário deve ser sempre em horário de São Paulo (America/Sao_Paulo)
    """
    from app.timezone_utils import now_brazil
    
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Apenas administradores podem alterar configurações")
    
    if config.send_time:
        # Validar formato HH:MM
        try:
            hour, minute = map(int, config.send_time.split(':'))
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError("Hora ou minuto inválido")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Formato de horário inválido: {e}")
        
        # Log do horário atual em São Paulo para referência
        now_sp = now_brazil()
        logger.info(f"⏰ Recebendo atualização de horário: {config.send_time} (horário de São Paulo)")
        logger.info(f"⏰ Horário atual em São Paulo: {now_sp.strftime('%H:%M:%S %Z')}")
        
        # Salvar no banco de dados
        try:
            db_config = db.query(SystemConfig).filter(SystemConfig.key == "devocional_send_time").first()
            old_value = db_config.value if db_config else None
            if db_config:
                logger.info(f"Atualizando horário existente: {old_value} -> {config.send_time} (horário de São Paulo)")
                db_config.value = config.send_time
            else:
                logger.info(f"Criando nova configuração de horário: {config.send_time} (horário de São Paulo)")
                db_config = SystemConfig(
                    key="devocional_send_time",
                    value=config.send_time,
                    description="Horário de envio automático de devocionais (formato HH:MM, horário de Brasília/São Paulo - America/Sao_Paulo)"
                )
                db.add(db_config)
            
            db.commit()
            db.refresh(db_config)  # Garantir que está atualizado
            
            # Verificar se foi salvo corretamente
            verify_config = db.query(SystemConfig).filter(SystemConfig.key == "devocional_send_time").first()
            if verify_config and verify_config.value == config.send_time:
                logger.info(f"✅ Horário de envio salvo com sucesso no banco: {verify_config.value} (horário de São Paulo)")
                logger.info(f"⏰ O scheduler irá enviar às {verify_config.value} no horário de São Paulo (America/Sao_Paulo)")
            else:
                logger.error(f"❌ Erro: Horário não foi salvo corretamente. Esperado: {config.send_time}, Encontrado: {verify_config.value if verify_config else 'None'}")
                raise HTTPException(status_code=500, detail="Erro ao salvar horário no banco de dados")
            
        except Exception as e:
            logger.error(f"Erro ao salvar horário no banco: {e}", exc_info=True)
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro ao salvar horário: {str(e)}")
        
        # Também atualizar variável de ambiente (para compatibilidade)
        os.environ["DEVOCIONAL_SEND_TIME"] = config.send_time
        
        logger.info(f"Horário de envio atualizado para {config.send_time} (horário de São Paulo) por {current_user.email} (dinâmico - aplicado imediatamente)")
    
    return {
        "message": "Horário de envio atualizado. Mudança será aplicada automaticamente em até 5 minutos.",
        "send_time": config.send_time,
        "timezone": "America/Sao_Paulo",
        "note": "O horário informado é sempre interpretado como horário de São Paulo (Brasil)"
    }

