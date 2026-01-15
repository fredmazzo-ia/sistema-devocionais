"""
Configuração de logging
Sempre usa horário de São Paulo (America/Sao_Paulo) nos logs
"""
import logging
import sys
from datetime import datetime
from zoneinfo import ZoneInfo
from logging import Formatter

# Timezone de São Paulo para logs
BRAZIL_TZ = ZoneInfo("America/Sao_Paulo")


class BrazilTimeFormatter(Formatter):
    """
    Formatter customizado que sempre mostra horário de São Paulo nos logs
    Independente do timezone do sistema operacional
    """
    def formatTime(self, record, datefmt=None):
        """Sobrescreve formatTime para usar horário de São Paulo"""
        dt = datetime.now(BRAZIL_TZ)
        if datefmt:
            return dt.strftime(datefmt)
        else:
            # Formato padrão: YYYY-MM-DD HH:MM:SS,mmm com timezone
            return dt.strftime('%Y-%m-%d %H:%M:%S,%f')[:-3] + f' {dt.strftime("%Z")}'


def setup_logging():
    """Configura o sistema de logging com horário de São Paulo"""
    # Criar handlers
    stream_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler('monitoramento.log', encoding='utf-8')
    
    # Aplicar formatter customizado que usa horário de São Paulo
    formatter = BrazilTimeFormatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt=None
    )
    
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        handlers=[stream_handler, file_handler]
    )
    
    # Log inicial para confirmar timezone
    logger = logging.getLogger(__name__)
    now_sp = datetime.now(BRAZIL_TZ)
    logger.info(f"📅 Sistema de logging configurado. Horário atual em São Paulo: {now_sp.strftime('%Y-%m-%d %H:%M:%S %Z')}")

