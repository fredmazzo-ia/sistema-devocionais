"""
Módulo de web scraping para portais de notícias
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from datetime import datetime
import time
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class NewsScraper:
    """Classe para realizar scraping de portais de notícias"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_portal(self, portal_config: Dict) -> List[Dict]:
        """
        Realiza scraping de um portal de notícias
        
        Args:
            portal_config: Configuração do portal com URL e seletores
            
        Returns:
            Lista de artigos encontrados
        """
        articles = []
        
        try:
            logger.info(f"Raspando portal: {portal_config['name']}")
            response = self.session.get(portal_config['url'], timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Encontrar todos os artigos
            article_elements = soup.select(portal_config['selectors']['article'])
            
            for element in article_elements[:settings.MAX_ARTICLES_PER_CHECK]:
                try:
                    article = self._extract_article_data(element, portal_config)
                    if article:
                        articles.append(article)
                except Exception as e:
                    logger.error(f"Erro ao extrair artigo: {e}")
                    continue
            
            logger.info(f"Encontrados {len(articles)} artigos em {portal_config['name']}")
            
        except requests.RequestException as e:
            logger.error(f"Erro ao acessar portal {portal_config['name']}: {e}")
        except Exception as e:
            logger.error(f"Erro inesperado ao raspar {portal_config['name']}: {e}")
        
        return articles
    
    def _extract_article_data(self, element, portal_config: Dict) -> Optional[Dict]:
        """Extrai dados de um elemento de artigo"""
        try:
            # Extrair título
            title_elem = element.select_one(portal_config['selectors']['title'])
            title = title_elem.get_text(strip=True) if title_elem else None
            
            if not title:
                return None
            
            # Extrair link
            link_elem = element.select_one(portal_config['selectors']['link'])
            if link_elem:
                link = link_elem.get('href', '')
                # Converter para URL absoluta se necessário
                if link and not link.startswith('http'):
                    base_url = portal_config['url']
                    if not base_url.endswith('/'):
                        base_url += '/'
                    link = base_url + link.lstrip('/')
            else:
                link = None
            
            # Extrair data
            date_elem = element.select_one(portal_config['selectors'].get('date', ''))
            published_date = None
            if date_elem:
                date_text = date_elem.get_text(strip=True)
                # Tentar parsear a data (implementar parser específico se necessário)
                published_date = datetime.now()  # Placeholder
            
            # Extrair conteúdo/resumo
            content_elem = element.select_one(portal_config['selectors'].get('content', ''))
            content = content_elem.get_text(strip=True) if content_elem else None
            
            return {
                'title': title,
                'url': link or portal_config['url'],
                'content': content,
                'source': portal_config['name'],
                'published_date': published_date,
                'scraped_date': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Erro ao extrair dados do artigo: {e}")
            return None
    
    def scrape_all_portals(self) -> List[Dict]:
        """Raspa todos os portais configurados"""
        all_articles = []
        
        for portal in settings.NEWS_PORTALS:
            articles = self.scrape_portal(portal)
            all_articles.extend(articles)
            time.sleep(2)  # Delay entre requisições para não sobrecarregar
        
        return all_articles

