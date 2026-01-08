"""
Agendador de tarefas para monitoramento automático
"""
import schedule
import time
import threading
import logging
from app.scraper import NewsScraper
from app.analyzer import NewsAnalyzer
from app.database import SessionLocal, NewsArticle, Notification
from app.whatsapp_service import WhatsAppService
from app.config import settings
from datetime import datetime

logger = logging.getLogger(__name__)

scraper = NewsScraper()
analyzer = NewsAnalyzer()
whatsapp = WhatsAppService()

scheduler_thread = None
scheduler_running = False


def monitor_news():
    """Função principal de monitoramento"""
    logger.info("Iniciando monitoramento de notícias...")
    
    try:
        # Raspar todos os portais
        articles = scraper.scrape_all_portals()
        
        db = SessionLocal()
        new_relevant_count = 0
        
        try:
            for article_data in articles:
                # Verificar se já existe
                existing = db.query(NewsArticle).filter(
                    NewsArticle.url == article_data['url']
                ).first()
                
                if existing:
                    continue  # Já processado
                
                # Analisar artigo
                analyzed = analyzer.analyze_article(article_data)
                
                # Salvar no banco
                news_article = NewsArticle(
                    title=analyzed['title'],
                    content=analyzed.get('content'),
                    url=analyzed['url'],
                    source=analyzed['source'],
                    published_date=analyzed.get('published_date'),
                    scraped_date=analyzed.get('scraped_date', datetime.now()),
                    is_relevant=analyzed.get('is_relevant', False),
                    relevance_score=analyzed.get('relevance_score', 0),
                    scope=analyzed.get('scope'),
                    responsible_area=analyzed.get('responsible_area')
                )
                
                db.add(news_article)
                db.commit()
                db.refresh(news_article)
                
                # Se for relevante, enviar notificações
                if analyzed.get('is_relevant'):
                    new_relevant_count += 1
                    logger.info(f"Nova notícia relevante encontrada: {analyzed['title']}")
                    
                    # Enviar notificações
                    notification_results = whatsapp.notify_responsibles(analyzed)
                    
                    # Registrar notificações
                    for result in notification_results:
                        notification = Notification(
                            article_id=news_article.id,
                            recipient_phone=result['phone'],
                            recipient_name=result['responsible'],
                            status='sent' if result['success'] else 'failed',
                            message=f"Notificação sobre: {analyzed['title']}"
                        )
                        db.add(notification)
                    
                    news_article.notified = True
                    news_article.processed = True
                    db.commit()
        
        finally:
            db.close()
        
        logger.info(f"Monitoramento concluído. {new_relevant_count} novas notícias relevantes encontradas.")
        
    except Exception as e:
        logger.error(f"Erro no monitoramento: {e}")


def run_scheduler():
    """Executa o agendador em thread separada"""
    global scheduler_running
    scheduler_running = True
    
    # Agendar monitoramento
    schedule.every(settings.MONITORING_INTERVAL_MINUTES).minutes.do(monitor_news)
    
    # Executar imediatamente na primeira vez
    monitor_news()
    
    while scheduler_running:
        schedule.run_pending()
        time.sleep(60)  # Verificar a cada minuto


def start_scheduler():
    """Inicia o agendador"""
    global scheduler_thread
    
    if scheduler_thread and scheduler_thread.is_alive():
        logger.warning("Agendador já está em execução")
        return
    
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    logger.info("Agendador de monitoramento iniciado")


def stop_scheduler():
    """Para o agendador"""
    global scheduler_running
    scheduler_running = False
    schedule.clear()
    logger.info("Agendador de monitoramento parado")

