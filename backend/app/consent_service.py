"""
Serviço para gerenciar consentimento dos contatos para receber devocionais
"""
import logging
import requests
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.database import ContactConsent, DevocionalContato
from app.timezone_utils import now_brazil_naive
from app.instance_manager import EvolutionInstance

logger = logging.getLogger(__name__)

CONSENT_MESSAGE = "Você gostaria de continuar recebendo o devocional diário?"
DENIAL_MESSAGE = "Entendido! Você não receberá mais devocionais.\n\nSe mudar de ideia e quiser voltar a receber, basta responder *sim* a qualquer momento. 😊"


def normalize_phone(phone: str) -> str:
    """
    Normaliza número de telefone removendo caracteres especiais e mantendo apenas dígitos
    Remove :88, :90, etc do final do número
    """
    if not phone:
        return ""
    # Remover tudo exceto dígitos
    phone_clean = ''.join(filter(str.isdigit, phone))
    # Se tiver mais de 11 dígitos, pode ter código do país (55) + DDD + número
    # Se tiver exatamente 11 dígitos e começar com 55, está OK
    # Se tiver 13 dígitos (55 + 11), está OK
    return phone_clean


class ConsentService:
    """Serviço para gerenciar consentimento dos contatos"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_or_create_consent(self, phone: str) -> ContactConsent:
        """Busca ou cria registro de consentimento"""
        consent = self.db.query(ContactConsent).filter(
            ContactConsent.phone == phone
        ).first()
        
        if not consent:
            consent = ContactConsent(
                phone=phone,
                consented=None,  # None = aguardando resposta
                consent_message_sent=False
            )
            self.db.add(consent)
            self.db.flush()
            logger.info(f"✅ Criado registro de consentimento para {phone}")
        
        return consent
    
    def can_send_devocional(self, phone: str) -> tuple[bool, str]:
        """
        Verifica se pode enviar devocional para o contato
        
        Returns:
            (pode_enviar, motivo)
        """
        consent = self.get_or_create_consent(phone)
        
        # Se já consentiu, pode enviar
        if consent.consented is True:
            return (True, "Consentimento confirmado")
        
        # Se negou, não pode enviar
        if consent.consented is False:
            return (False, "Contato não consentiu em receber devocionais")
        
        # Se está aguardando resposta, não pode enviar
        if consent.consent_message_sent and consent.consented is None:
            return (False, "Aguardando resposta de consentimento")
        
        # Se nunca enviou mensagem de consentimento, pode enviar (primeira vez)
        return (True, "Primeira mensagem - ainda não enviou consentimento")
    
    def should_send_consent_message(self, phone: str) -> bool:
        """
        Verifica se deve enviar mensagem de consentimento
        
        Deve enviar se:
        - É primeiro envio (total_sent == 0) OU acabou de enviar o primeiro (total_sent == 1)
        - Ainda não enviou mensagem de consentimento
        
        IMPORTANTE: Esta função deve ser chamada DEPOIS de incrementar total_sent
        para detectar que acabou de enviar o primeiro devocional
        """
        # Verificar total_sent do contato
        contact = self.db.query(DevocionalContato).filter(
            DevocionalContato.phone == phone
        ).first()
        
        if not contact:
            return False
        
        # Se é primeiro envio (total_sent == 0) OU acabou de enviar o primeiro (total_sent == 1)
        # total_sent == 0: ainda não enviou nenhum
        # total_sent == 1: acabou de enviar o primeiro (momento certo para enviar consentimento)
        is_first_send = (not contact.total_sent or contact.total_sent == 0 or contact.total_sent == 1)
        
        # Verificar se já enviou mensagem de consentimento
        consent = self.get_or_create_consent(phone)
        already_sent = consent.consent_message_sent
        
        logger.debug(f"📋 Verificando consentimento para {phone}: total_sent={contact.total_sent}, is_first_send={is_first_send}, already_sent={already_sent}")
        
        return is_first_send and not already_sent
    
    def send_consent_message(
        self,
        instance: EvolutionInstance,
        phone: str,
        name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Envia mensagem de consentimento para o contato
        
        Args:
            instance: Instância Evolution API
            phone: Telefone do contato
            name: Nome do contato (opcional)
            
        Returns:
            Dict com resultado do envio
        """
        try:
            # Personalizar mensagem
            personalized_message = CONSENT_MESSAGE
            if name:
                personalized_message = f"Olá {name}! 👋\n\n{CONSENT_MESSAGE}"
            
            # Formatar telefone
            phone_clean = ''.join(filter(str.isdigit, phone))
            if not phone_clean.startswith('55') and len(phone_clean) == 11:
                phone_clean = '55' + phone_clean
            
            # Enviar mensagem
            headers = {
                "Content-Type": "application/json",
                "apikey": instance.api_key
            }
            
            api_instance_name = getattr(instance, 'api_instance_name', None) or instance.name
            url = f"{instance.api_url}/message/sendText/{api_instance_name}"
            
            payload = {
                "number": phone_clean,
                "text": personalized_message
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code in [200, 201]:
                response_data = response.json()
                message_id = response_data.get('key', {}).get('id') if 'key' in response_data else None
                
                # Atualizar registro de consentimento
                consent = self.get_or_create_consent(phone)
                consent.consent_message_sent = True
                consent.consent_message_sent_at = now_brazil_naive()
                self.db.commit()
                
                logger.info(f"✅ Mensagem de consentimento enviada para {phone} (ID: {message_id})")
                
                return {
                    "success": True,
                    "message_id": message_id,
                    "phone": phone
                }
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                logger.error(f"❌ Erro ao enviar mensagem de consentimento: {error_msg}")
                return {
                    "success": False,
                    "error": error_msg,
                    "phone": phone
                }
                
        except Exception as e:
            logger.error(f"❌ Erro ao enviar mensagem de consentimento: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "phone": phone
            }
    
    def _is_negative_response(self, message_lower: str) -> bool:
        """
        Detecta se a mensagem é uma negação de consentimento de forma inteligente.
        
        Distingue entre:
        - "não quero mais receber" -> NEGAÇÃO
        - "não vou desistir de Jesus" -> POSITIVA (não é negação)
        - "não esperava que fosse tão bom" -> POSITIVA (não é negação)
        
        Args:
            message_lower: Mensagem em minúsculas
            
        Returns:
            True se for negação de consentimento, False caso contrário
        """
        import re
        
        # Palavras que indicam negação de consentimento quando aparecem após "não"
        negative_keywords = [
            'quero', 'quer', 'querer', 'querendo',
            'receber', 'recebendo', 'receber mais',
            'devocional', 'devocionais',
            'continuar', 'continuando',
            'parar', 'parando', 'parar de receber',
            'cancelar', 'cancelando', 'cancelamento',
            'obrigado', 'obrigada',
            'não quero', 'nao quero',
            'não receber', 'nao receber',
            'parar de', 'cancelar recebimento'
        ]
        
        # Frases positivas que contêm "não" mas não são negação
        positive_patterns = [
            r'não\s+vou\s+desistir',
            r'não\s+esperava',
            r'não\s+imaginava',
            r'não\s+acredito\s+que',
            r'não\s+poderia\s+ser\s+melhor',
            r'não\s+tenho\s+palavras',
            r'não\s+consigo\s+expressar',
            r'não\s+é\s+possível',
            r'não\s+é\s+verdade',
            r'não\s+acredito',
            r'não\s+parece\s+real',
            r'não\s+vou\s+parar',
            r'não\s+quero\s+parar',
            r'não\s+quero\s+cancelar',
            r'não\s+pretendo\s+parar',
            r'não\s+pretendo\s+cancelar',
            r'não\s+tenho\s+intenção\s+de\s+parar',
            r'não\s+tenho\s+intenção\s+de\s+cancelar',
            r'não\s+pretendo\s+deixar',
            r'não\s+vou\s+deixar',
            r'não\s+quero\s+deixar',
        ]
        
        # Verificar se contém padrões positivos (que contêm "não" mas são positivos)
        for pattern in positive_patterns:
            if re.search(pattern, message_lower):
                logger.debug(f"🔍 Mensagem contém padrão positivo: '{pattern}' - não é negação")
                return False
        
        # Verificar respostas negativas simples e diretas
        # Se a mensagem é apenas "não", "nao" ou "n" (palavra completa, sem outras palavras)
        message_words = message_lower.strip().split()
        if len(message_words) == 1 and message_words[0] in ['não', 'nao', 'n']:
            logger.debug(f"🔍 Mensagem é negação simples: '{message_lower}'")
            return True
        
        # Verificar se "não" ou "nao" aparece seguido de palavras-chave de negação
        # Buscar padrão: "não" + (até 3 palavras) + palavra-chave negativa
        negative_pattern = r'(não|nao)\s+(\w+\s+){0,3}?(' + '|'.join(negative_keywords) + ')'
        if re.search(negative_pattern, message_lower):
            logger.debug(f"🔍 Mensagem contém padrão de negação: '{message_lower}'")
            return True
        
        # Verificar palavras de cancelamento diretas
        direct_cancel = ['parar', 'cancelar', 'não obrigado', 'nao obrigado']
        if any(cancel in message_lower for cancel in direct_cancel):
            # Mas verificar se não está em contexto positivo
            if not any(pos in message_lower for pos in ['não vou parar', 'não quero cancelar', 'não quero parar']):
                logger.debug(f"🔍 Mensagem contém palavra de cancelamento: '{message_lower}'")
                return True
        
        return False
    
    def process_consent_response(self, phone: str, message_text: str, instance_name: Optional[str] = None) -> bool:
        """
        Processa resposta de consentimento do contato
        
        Args:
            phone: Telefone do contato
            message_text: Texto da mensagem recebida
            instance_name: Nome da instância que recebeu a mensagem (para usar na resposta)
            
        Returns:
            True se processou, False caso contrário
        """
        try:
            message_lower = message_text.lower().strip()
            
            # Verificar se é resposta de consentimento
            # Respostas positivas: sim, s, quero, quero sim, continuar, ok, tudo bem
            positive_responses = ['sim', 's', 'quero', 'quero sim', 'continuar', 'ok', 'tudo bem', 'claro', 'pode']
            
            # Detecção inteligente de negação
            is_negative = self._is_negative_response(message_lower)
            is_positive = any(resp in message_lower for resp in positive_responses)
            
            if not (is_positive or is_negative):
                # Não é resposta de consentimento
                return False
            
            # Normalizar telefone para busca
            phone_normalized = normalize_phone(phone)
            logger.info(f"🔍 Buscando contato com telefone normalizado: {phone} -> {phone_normalized}")
            
            # Obter contato - tentar busca exata primeiro
            contact = self.db.query(DevocionalContato).filter(
                DevocionalContato.phone == phone
            ).first()
            
            # Se não encontrou, tentar buscar normalizando telefones do banco também
            if not contact:
                # Buscar todos os contatos e comparar telefones normalizados
                all_contacts = self.db.query(DevocionalContato).all()
                for c in all_contacts:
                    if normalize_phone(c.phone) == phone_normalized:
                        contact = c
                        logger.info(f"✅ Contato encontrado por normalização: {c.phone} -> {phone_normalized}")
                        break
            
            if not contact:
                logger.warning(f"⚠️ Contato {phone} (normalizado: {phone_normalized}) não encontrado no banco. Criando registro de consentimento apenas.")
            else:
                logger.info(f"📋 Contato encontrado: ID={contact.id}, phone={contact.phone}, name={contact.name}, active={contact.active}")
            
            # Atualizar consentimento
            consent = self.get_or_create_consent(phone)
            logger.info(f"📋 Consentimento atual: consented={consent.consented}, response_received={consent.response_received}")
            previous_consent = consent.consented  # Guardar valor anterior para verificar mudança
            consent.consented = is_positive
            consent.response_received = True
            consent.response_received_at = now_brazil_naive()
            consent.response_text = message_text
            
            # Se negou, desativar contato e enviar mensagem
            if is_negative:
                if contact:
                    was_active = contact.active
                    contact.active = False
                    logger.info(f"⚠️ Contato {phone} desativado (negou consentimento). Status anterior: {was_active}")
                else:
                    logger.warning(f"⚠️ Contato {phone} não encontrado no banco ao processar negação")
                
                # Enviar mensagem informando que pode voltar a receber dizendo "sim"
                try:
                    logger.info(f"📤 Tentando enviar mensagem de negação para {phone} usando instância {instance_name or 'padrão'}...")
                    sent = self._send_denial_message(phone, contact.name if contact else None, instance_name)
                    if sent:
                        logger.info(f"✅ Mensagem de negação enviada com sucesso para {phone}")
                    else:
                        logger.warning(f"⚠️ Não foi possível enviar mensagem de negação para {phone}")
                except Exception as e:
                    logger.error(f"❌ Erro ao enviar mensagem de negação: {e}", exc_info=True)
                    # Não falhar o processamento se não conseguir enviar a mensagem
            
            # Se consentiu (voltou a dizer sim), reativar contato
            elif is_positive:
                if contact:
                    was_inactive = not contact.active
                    # Sempre reativar quando consentir (mesmo que já esteja ativo, garante que está ativo)
                    contact.active = True
                    if was_inactive:
                        logger.info(f"✅ Contato {phone} reativado (consentiu novamente). Status anterior: inativo")
                    else:
                        logger.info(f"✅ Contato {phone} mantido ativo (consentimento confirmado novamente). Status anterior: ativo")
                else:
                    logger.warning(f"⚠️ Contato {phone} não encontrado no banco ao processar consentimento positivo")
            
            # Fazer commit das mudanças
            try:
                self.db.commit()
                # Refresh para garantir que está atualizado
                if contact:
                    self.db.refresh(contact)
                self.db.refresh(consent)
                
                # Verificar valores após commit
                final_active = contact.active if contact else None
                final_consented = consent.consented
                
                logger.info(f"✅ Mudanças commitadas no banco para {phone}: active={final_active}, consented={final_consented}")
                logger.info(f"📊 Status final - Contato ID: {contact.id if contact else 'N/A'}, Active: {final_active}, Consentido: {final_consented}")
            except Exception as e:
                logger.error(f"❌ Erro ao fazer commit: {e}", exc_info=True)
                self.db.rollback()
                raise
            
            logger.info(f"✅ Consentimento processado para {phone}: {'SIM' if is_positive else 'NÃO'}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar resposta de consentimento: {e}", exc_info=True)
            self.db.rollback()
            return False
    
    def _send_denial_message(self, phone: str, name: Optional[str] = None, instance_name: Optional[str] = None) -> bool:
        """
        Envia mensagem quando consentimento é negado
        
        Args:
            phone: Telefone do contato
            name: Nome do contato (opcional)
            instance_name: Nome da instância que recebeu a mensagem (para usar a mesma)
            
        Returns:
            True se enviou com sucesso, False caso contrário
        """
        try:
            logger.info(f"📤 Iniciando envio de mensagem de negação para {phone} usando instância: {instance_name or 'padrão'}")
            
            # Obter instância ativa para enviar mensagem
            from app.instance_manager import InstanceManager, InstanceStatus
            
            # Passar db para InstanceManager buscar instâncias do banco
            logger.debug(f"🔍 Criando InstanceManager com db...")
            instance_manager = InstanceManager(db=self.db)
            logger.info(f"📊 InstanceManager criado. Total de instâncias: {len(instance_manager.instances) if instance_manager.instances else 0}")
            
            if not instance_manager.instances:
                logger.warning("⚠️ Nenhuma instância disponível para enviar mensagem de negação")
                return False
            
            instance = None
            
            # PRIORIDADE 1: Usar a mesma instância que recebeu a mensagem (se fornecida)
            if instance_name:
                logger.info(f"🔍 Buscando instância específica: {instance_name}")
                for inst in instance_manager.instances:
                    # Comparar por nome ou api_instance_name
                    inst_name = getattr(inst, 'api_instance_name', None) or inst.name
                    if inst_name == instance_name and inst.enabled:
                        instance = inst
                        logger.info(f"✅ Instância encontrada: {inst_name} (status: {inst.status})")
                        # Mesmo que não esteja ACTIVE, usar se não estiver BLOCKED
                        if inst.status == InstanceStatus.BLOCKED:
                            logger.warning(f"⚠️ Instância {inst_name} está bloqueada, tentando outra...")
                            instance = None
                        else:
                            break
            
            # PRIORIDADE 2: Se não encontrou a instância específica ou não foi fornecida, buscar primeira instância ativa
            if not instance:
                logger.info("🔍 Buscando primeira instância ativa...")
                for inst in instance_manager.instances:
                    if inst.enabled and inst.status == InstanceStatus.ACTIVE:
                        instance = inst
                        logger.info(f"✅ Instância ativa encontrada: {inst.name}")
                        break
            
            # PRIORIDADE 3: Se não encontrou ativa, tentar qualquer instância habilitada (exceto bloqueada)
            if not instance:
                logger.info("🔍 Buscando qualquer instância habilitada...")
                for inst in instance_manager.instances:
                    if inst.enabled and inst.status != InstanceStatus.BLOCKED:
                        instance = inst
                        logger.info(f"✅ Instância habilitada encontrada: {inst.name} (status: {inst.status})")
                        break
            
            if not instance:
                logger.warning("⚠️ Nenhuma instância disponível para enviar mensagem de negação")
                return False
            
            # Personalizar mensagem
            personalized_message = DENIAL_MESSAGE
            if name:
                personalized_message = f"Olá {name}! 👋\n\n{DENIAL_MESSAGE}"
            
            # Formatar telefone
            phone_clean = ''.join(filter(str.isdigit, phone))
            if not phone_clean.startswith('55') and len(phone_clean) == 11:
                phone_clean = '55' + phone_clean
            
            # Enviar mensagem
            headers = {
                "Content-Type": "application/json",
                "apikey": instance.api_key
            }
            
            api_instance_name = getattr(instance, 'api_instance_name', None) or instance.name
            url = f"{instance.api_url}/message/sendText/{api_instance_name}"
            
            payload = {
                "number": phone_clean,
                "text": personalized_message
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code in [200, 201]:
                logger.info(f"✅ Mensagem de negação enviada para {phone}")
                return True
            else:
                logger.error(f"❌ Erro ao enviar mensagem de negação: HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erro ao enviar mensagem de negação: {e}", exc_info=True)
            return False