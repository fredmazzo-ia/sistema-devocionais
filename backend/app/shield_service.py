"""
Serviço de Blindagem para WhatsApp
Ferramentas avançadas para prevenir bloqueios
"""
import logging
import random
import time
from typing import Optional, Dict, List, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class ShieldStatus(Enum):
    """Status da blindagem"""
    ACTIVE = "active"
    PAUSED = "paused"
    BLOCKED = "blocked"
    WARNING = "warning"


@dataclass
class EngagementData:
    """Dados de engajamento de um contato"""
    phone: str
    engagement_score: float = 0.5  # 0.0 a 1.0
    total_sent: int = 0
    total_responded: int = 0
    last_response_date: Optional[datetime] = None
    last_sent_date: Optional[datetime] = None
    consecutive_no_response: int = 0


@dataclass
class ShieldMetrics:
    """Métricas de blindagem"""
    total_messages_sent: int = 0
    consecutive_errors: int = 0
    last_error_time: Optional[datetime] = None
    success_rate: float = 1.0
    status: ShieldStatus = ShieldStatus.ACTIVE
    last_break_time: Optional[datetime] = None
    messages_since_break: int = 0


class ShieldService:
    """
    Serviço de blindagem avançada para WhatsApp
    Implementa múltiplas estratégias para prevenir bloqueios
    """
    
    def __init__(
        self,
        delay_variation: float = 0.3,
        break_interval: int = 50,
        break_duration_min: float = 15.0,
        break_duration_max: float = 30.0,
        min_engagement_score: float = 0.3,
        adaptive_limits_enabled: bool = True,
        block_detection_enabled: bool = True
    ):
        """
        Inicializa serviço de blindagem
        
        Args:
            delay_variation: Variação percentual do delay (0.3 = 30%)
            break_interval: Mensagens entre pausas
            break_duration_min: Duração mínima da pausa (segundos)
            break_duration_max: Duração máxima da pausa (segundos)
            min_engagement_score: Score mínimo de engajamento para enviar
            adaptive_limits_enabled: Ativar limites adaptativos
            block_detection_enabled: Ativar detecção de bloqueio
        """
        self.delay_variation = delay_variation
        self.break_interval = break_interval
        self.break_duration_min = break_duration_min
        self.break_duration_max = break_duration_max
        self.min_engagement_score = min_engagement_score
        self.adaptive_limits_enabled = adaptive_limits_enabled
        self.block_detection_enabled = block_detection_enabled
        
        # Dados de engajamento por contato
        self.engagement_data: Dict[str, EngagementData] = {}
        
        # Métricas globais
        self.metrics = ShieldMetrics()
        
        # Limites adaptativos
        self.base_hourly_limit = 20
        self.base_daily_limit = 200
        self.current_hourly_limit = 20
        self.current_daily_limit = 200
        
        logger.info("ShieldService inicializado")
    
    def get_randomized_delay(self, base_delay: float) -> float:
        """
        Retorna delay com variação aleatória
        
        Args:
            base_delay: Delay base em segundos
        
        Returns:
            Delay aleatório
        """
        min_delay = base_delay * (1 - self.delay_variation)
        max_delay = base_delay * (1 + self.delay_variation)
        randomized = random.uniform(min_delay, max_delay)
        
        logger.debug(f"Delay randomizado: {base_delay}s -> {randomized:.2f}s")
        return randomized
    
    def should_take_break(self) -> bool:
        """
        Verifica se deve fazer pausa estratégica
        
        Returns:
            True se deve fazer pausa
        """
        should_break = (
            self.metrics.messages_since_break >= self.break_interval
        )
        
        if should_break:
            logger.info(
                f"Pausa estratégica necessária: "
                f"{self.metrics.messages_since_break} mensagens desde última pausa"
            )
        
        return should_break
    
    def get_break_duration(self) -> float:
        """
        Retorna duração da pausa estratégica
        
        Returns:
            Duração em segundos
        """
        duration = random.uniform(
            self.break_duration_min,
            self.break_duration_max
        )
        
        logger.info(f"Pausa estratégica: {duration:.2f} segundos")
        return duration
    
    def take_break(self):
        """Executa pausa estratégica"""
        duration = self.get_break_duration()
        from app.timezone_utils import now_brazil
        self.metrics.last_break_time = now_brazil()
        self.metrics.messages_since_break = 0
        
        logger.info(f"Executando pausa estratégica de {duration:.2f} segundos...")
        time.sleep(duration)
        logger.info("Pausa estratégica concluída")
    
    def is_safe_send_time(self, hour: Optional[int] = None) -> bool:
        """
        Verifica se é horário seguro para envio
        
        Args:
            hour: Hora do dia (0-23). Se None, usa hora atual
        
        Returns:
            True se é horário seguro
        """
        if hour is None:
            from app.timezone_utils import now_brazil
            hour = now_brazil().hour
        
        # Horários seguros: 6h-22h
        safe_hours = list(range(6, 23))
        
        is_safe = hour in safe_hours
        
        if not is_safe:
            logger.warning(f"Horário não seguro para envio: {hour:02d}h")
        
        return is_safe
    
    def get_optimal_send_times(self, total_contacts: int) -> List[int]:
        """
        Calcula horários ótimos para distribuir envios
        
        Args:
            total_contacts: Total de contatos
        
        Returns:
            Lista de horários (em horas)
        """
        safe_hours = list(range(6, 23))
        
        # Se poucos contatos, enviar em horário único
        if total_contacts < 50:
            return [6]  # 06:00
        
        # Se muitos contatos, distribuir
        num_windows = min(4, total_contacts // 50)  # Máximo 4 janelas
        step = len(safe_hours) // num_windows
        
        optimal_times = [
            safe_hours[i * step] for i in range(num_windows)
        ]
        
        logger.info(f"Horários ótimos calculados: {optimal_times}")
        return optimal_times
    
    def update_engagement(self, phone: str, responded: bool = False):
        """
        Atualiza score de engajamento de um contato
        
        Args:
            phone: Número do telefone
            responded: Se o contato respondeu
        """
        if phone not in self.engagement_data:
            self.engagement_data[phone] = EngagementData(phone=phone)
        
        data = self.engagement_data[phone]
        data.total_sent += 1
        from app.timezone_utils import now_brazil
        data.last_sent_date = now_brazil()
        
        if responded:
            data.total_responded += 1
            from app.timezone_utils import now_brazil
            data.last_response_date = now_brazil()
            data.consecutive_no_response = 0
            # Aumentar score
            data.engagement_score = min(1.0, data.engagement_score + 0.1)
        else:
            data.consecutive_no_response += 1
            # Diminuir score gradualmente
            data.engagement_score = max(0.0, data.engagement_score - 0.05)
        
        # Calcular score baseado em taxa de resposta
        if data.total_sent > 0:
            response_rate = data.total_responded / data.total_sent
            # Combinar com score atual (média ponderada)
            data.engagement_score = (data.engagement_score * 0.6) + (response_rate * 0.4)
        
        logger.debug(
            f"Engajamento atualizado para {phone}: "
            f"score={data.engagement_score:.2f}, "
            f"responded={responded}"
        )
    
    def should_send_to_contact(self, phone: str) -> bool:
        """
        Decide se deve enviar para um contato baseado no engajamento
        
        Args:
            phone: Número do telefone
        
        Returns:
            True se deve enviar
        """
        if phone not in self.engagement_data:
            # Novo contato, permitir envio
            return True
        
        data = self.engagement_data[phone]
        should_send = data.engagement_score >= self.min_engagement_score
        
        if not should_send:
            logger.debug(
                f"Pulando envio para {phone}: "
                f"score muito baixo ({data.engagement_score:.2f})"
            )
        
        return should_send
    
    def analyze_response_for_block(self, response: Dict) -> bool:
        """
        Analisa resposta da API para detectar bloqueio
        
        Args:
            response: Resposta da API
        
        Returns:
            True se detectar bloqueio
        """
        if not self.block_detection_enabled:
            return False
        
        error_patterns = [
            "blocked",
            "rate limit",
            "too many requests",
            "forbidden",
            "unauthorized",
            "429",  # HTTP 429 Too Many Requests
            "403",  # HTTP 403 Forbidden
        ]
        
        error_text = str(response.get("error", "")).lower()
        status_code = response.get("status_code")
        
        # Verificar padrões de erro
        for pattern in error_patterns:
            if pattern in error_text:
                self.metrics.consecutive_errors += 1
                from app.timezone_utils import now_brazil
                self.metrics.last_error_time = now_brazil()
                
                logger.warning(
                    f"Padrão de bloqueio detectado: '{pattern}'. "
                    f"Erros consecutivos: {self.metrics.consecutive_errors}"
                )
                
                # Se 3 erros consecutivos, pode ser bloqueio
                if self.metrics.consecutive_errors >= 3:
                    self.metrics.status = ShieldStatus.BLOCKED
                    logger.error("BLOQUEIO DETECTADO! Pausando envios.")
                    return True
        
        # Verificar status code HTTP
        if status_code in [429, 403]:
            self.metrics.consecutive_errors += 1
            self.metrics.last_error_time = datetime.now()
            
            if self.metrics.consecutive_errors >= 3:
                self.metrics.status = ShieldStatus.BLOCKED
                return True
        
        # Reset se sucesso
        if response.get("status") == "success" or response.get("status_code") == 200:
            self.metrics.consecutive_errors = 0
            if self.metrics.status == ShieldStatus.BLOCKED:
                self.metrics.status = ShieldStatus.ACTIVE
                logger.info("Status de bloqueio removido após sucesso")
        
        return False
    
    def update_success_rate(self, success_count: int, total_count: int):
        """
        Atualiza taxa de sucesso global
        
        Args:
            success_count: Número de sucessos
            total_count: Total de tentativas
        """
        if total_count > 0:
            self.metrics.success_rate = success_count / total_count
            
            logger.debug(
                f"Taxa de sucesso atualizada: "
                f"{self.metrics.success_rate:.2%}"
            )
    
    def adjust_limits(self):
        """
        Ajusta limites adaptativamente baseado na taxa de sucesso
        """
        if not self.adaptive_limits_enabled:
            return
        
        success_rate = self.metrics.success_rate
        
        if success_rate < 0.8:  # Menos de 80% de sucesso
            # Reduzir limites em 20%
            self.current_hourly_limit = int(self.base_hourly_limit * 0.8)
            self.current_daily_limit = int(self.base_daily_limit * 0.8)
            
            self.metrics.status = ShieldStatus.WARNING
            
            logger.warning(
                f"Limites reduzidos devido à baixa taxa de sucesso "
                f"({success_rate:.2%}): "
                f"{self.current_hourly_limit}/hora, "
                f"{self.current_daily_limit}/dia"
            )
        
        elif success_rate > 0.95:  # Mais de 95% de sucesso
            # Aumentar limites em 10% (cuidado!)
            self.current_hourly_limit = min(
                int(self.base_hourly_limit * 1.1),
                self.base_hourly_limit + 5  # Máximo +5
            )
            self.current_daily_limit = min(
                int(self.base_daily_limit * 1.1),
                self.base_daily_limit + 20  # Máximo +20
            )
            
            logger.info(
                f"Limites aumentados devido à alta taxa de sucesso "
                f"({success_rate:.2%}): "
                f"{self.current_hourly_limit}/hora, "
                f"{self.current_daily_limit}/dia"
            )
        
        else:
            # Manter limites base
            self.current_hourly_limit = self.base_hourly_limit
            self.current_daily_limit = self.base_daily_limit
            self.metrics.status = ShieldStatus.ACTIVE
    
    def should_pause_sending(self) -> bool:
        """
        Verifica se deve pausar envios (bloqueio detectado)
        
        Returns:
            True se deve pausar
        """
        return self.metrics.status == ShieldStatus.BLOCKED
    
    def get_current_limits(self) -> Tuple[int, int]:
        """
        Retorna limites atuais (hora e dia)
        
        Returns:
            (limite_hora, limite_dia)
        """
        return (self.current_hourly_limit, self.current_daily_limit)
    
    def get_engagement_score(self, phone: str) -> float:
        """
        Retorna score de engajamento de um contato
        
        Args:
            phone: Número do telefone
        
        Returns:
            Score de engajamento (0.0 a 1.0)
        """
        if phone not in self.engagement_data:
            return 0.5  # Score padrão para novos contatos
        
        return self.engagement_data[phone].engagement_score
    
    def get_metrics(self) -> Dict:
        """
        Retorna métricas de blindagem
        
        Returns:
            Dicionário com métricas
        """
        return {
            "status": self.metrics.status.value,
            "total_messages_sent": self.metrics.total_messages_sent,
            "consecutive_errors": self.metrics.consecutive_errors,
            "success_rate": self.metrics.success_rate,
            "current_hourly_limit": self.current_hourly_limit,
            "current_daily_limit": self.current_daily_limit,
            "messages_since_break": self.metrics.messages_since_break,
            "last_break_time": (
                self.metrics.last_break_time.isoformat()
                if self.metrics.last_break_time
                else None
            ),
            "engagement_tracked": len(self.engagement_data)
        }

