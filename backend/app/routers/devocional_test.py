"""
Endpoints para teste de geração de devocionais (sem contexto)
"""
from fastapi import APIRouter, HTTPException
from typing import Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/devocional", tags=["devocional-test"])


@router.get("/test/contexto-vazio")
async def get_contexto_vazio():
    """
    Retorna contexto vazio para testes iniciais
    
    Use quando ainda não há devocionais no banco
    """
    return {
        "contexto_historico": "Esta é uma das primeiras mensagens da série. O tema central é 'Expressar Jesus Cristo' em nossa vida diária.",
        "versiculos_usados": [],
        "temas_abordados": [],
        "direcionamento_sugerido": "Inicie a jornada apresentando como podemos expressar Jesus em nosso dia a dia, focando em aspectos práticos e transformadores.",
        "conceito_central": "Expressar Jesus através da nossa caminhada diária",
        "mensagem": "Use o prompt PROMPT_GERADOR_SEM_CONTEXTO.md para gerar o devocional"
    }


@router.get("/test/personalizacao")
async def test_personalizacao(
    nome: str = "Tadeu",
    mensagem: Optional[str] = None
):
    """
    Testa a personalização de mensagem (saudação + nome)
    
    Útil para ver como o sistema adiciona saudação automaticamente
    """
    from app.devocional_service import DevocionalService
    
    service = DevocionalService()
    
    # Mensagem exemplo (sem saudação)
    if not mensagem:
        mensagem = """📅 Quarta-feira, 10 de dezembro de 2025

🌟 *Caminhando Guiados pelo Eterno*

📖 *Versículo Principal:*
"Porque este Deus é o nosso Deus para sempre; ele será o nosso guia até à morte." (Salmos 48:14 ACF)

📖 *Versículo de Apoio:*
"Faze-me entender o caminho dos teus preceitos; assim falarei das tuas maravilhas." (Salmos 119:27 ACF)

💬 Amado(a) irmão(ã), que alegria é saber que temos um Deus eterno que não apenas nos criou, mas também se propõe a ser nosso guia em cada passo da vida!

🌱 *Aplicação:*
Hoje, permita que o Senhor seja seu guia em todas as decisões.

🙏 *Oração:*
Pai amado, agradeço porque és o meu Deus para sempre e meu guia fiel.

Deus te abençoe abundantemente! Até amanhã!

Alex e Daniela Mantovani"""
    
    # Personalizar
    mensagem_personalizada = service._personalize_message(mensagem, nome)
    
    return {
        "original": mensagem,
        "personalizada": mensagem_personalizada,
        "nome_usado": nome,
        "saudacao": service._get_greeting_by_time(),
        "diferenca": {
            "tamanho_original": len(mensagem),
            "tamanho_personalizada": len(mensagem_personalizada),
            "adicionado": len(mensagem_personalizada) - len(mensagem)
        }
    }
