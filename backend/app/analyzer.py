"""
Módulo de análise e classificação de notícias
"""
from typing import Dict, List, Optional
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class NewsAnalyzer:
    """Classe para analisar e classificar notícias"""
    
    def __init__(self):
        self.keywords = [kw.lower() for kw in settings.KEYWORDS]
    
    def is_relevant(self, article: Dict) -> bool:
        """
        Verifica se uma notícia é relevante baseado nas palavras-chave
        
        Args:
            article: Dicionário com dados do artigo
            
        Returns:
            True se a notícia for relevante
        """
        text_to_analyze = f"{article.get('title', '')} {article.get('content', '')}".lower()
        
        # Contar ocorrências de palavras-chave
        matches = sum(1 for keyword in self.keywords if keyword in text_to_analyze)
        
        return matches > 0
    
    def calculate_relevance_score(self, article: Dict) -> int:
        """
        Calcula um score de relevância para a notícia
        
        Args:
            article: Dicionário com dados do artigo
            
        Returns:
            Score de relevância (0-100)
        """
        text_to_analyze = f"{article.get('title', '')} {article.get('content', '')}".lower()
        
        score = 0
        for keyword in self.keywords:
            count = text_to_analyze.count(keyword)
            # Palavras mais específicas têm peso maior
            if len(keyword.split()) > 1:  # Frase completa
                score += count * 20
            else:  # Palavra única
                score += count * 10
        
        return min(score, 100)
    
    def identify_scope(self, article: Dict) -> Optional[str]:
        """
        Identifica o escopo de atuação da notícia
        
        Args:
            article: Dicionário com dados do artigo
            
        Returns:
            Escopo identificado (ex: "CRAS", "CREAS", "Cadastro Único", etc.)
        """
        text_to_analyze = f"{article.get('title', '')} {article.get('content', '')}".lower()
        
        # Mapeamento de palavras-chave para escopos
        scope_keywords = {
            "CRAS": ["cras", "centro de referência"],
            "CREAS": ["creas", "centro especializado"],
            "Cadastro Único": ["cadastro único", "cadunico"],
            "Bolsa Família": ["bolsa família", "bolsa familia"],
            "Benefícios": ["benefício", "beneficio", "auxílio", "auxilio"],
            "Proteção Social": ["proteção social", "protecao social", "vulnerabilidade"]
        }
        
        for scope, keywords in scope_keywords.items():
            if any(kw in text_to_analyze for kw in keywords):
                return scope
        
        return "Geral"
    
    def identify_responsible_area(self, article: Dict) -> Optional[str]:
        """
        Identifica a área responsável baseado no escopo
        
        Args:
            article: Dicionário com dados do artigo
            
        Returns:
            Área responsável
        """
        scope = self.identify_scope(article)
        
        # Mapear escopo para área responsável
        scope_to_area = {
            "CRAS": "CRAS",
            "CREAS": "CREAS",
            "Cadastro Único": "Cadastro Único",
            "Bolsa Família": "Benefícios",
            "Benefícios": "Benefícios",
            "Proteção Social": "Proteção Social",
            "Geral": "Coordenação Geral"
        }
        
        return scope_to_area.get(scope, "Coordenação Geral")
    
    def analyze_article(self, article: Dict) -> Dict:
        """
        Realiza análise completa de um artigo
        
        Args:
            article: Dicionário com dados do artigo
            
        Returns:
            Artigo com informações de análise adicionadas
        """
        is_relevant = self.is_relevant(article)
        relevance_score = self.calculate_relevance_score(article) if is_relevant else 0
        scope = self.identify_scope(article) if is_relevant else None
        responsible_area = self.identify_responsible_area(article) if is_relevant else None
        
        article['is_relevant'] = is_relevant
        article['relevance_score'] = relevance_score
        article['scope'] = scope
        article['responsible_area'] = responsible_area
        
        return article

