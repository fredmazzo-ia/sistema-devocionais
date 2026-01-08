import { useState, useEffect } from 'react'
import { newsApi, NewsArticle } from '../services/api'
import './NewsList.css'

function NewsList() {
  const [news, setNews] = useState<NewsArticle[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [relevantOnly, setRelevantOnly] = useState(false)

  useEffect(() => {
    loadNews()
  }, [relevantOnly])

  const loadNews = async () => {
    try {
      setLoading(true)
      const data = await newsApi.getAll(0, 50, relevantOnly)
      setNews(data)
      setError(null)
    } catch (err: any) {
      setError(err.message || 'Erro ao carregar notícias')
    } finally {
      setLoading(false)
    }
  }

  const handleMarkProcessed = async (id: number) => {
    try {
      await newsApi.markAsProcessed(id)
      loadNews()
    } catch (err: any) {
      setError(err.message || 'Erro ao marcar como processada')
    }
  }

  if (loading) {
    return <div className="loading">Carregando notícias...</div>
  }

  return (
    <div className="news-list">
      <div className="news-header">
        <h1>Notícias</h1>
        <label className="filter-toggle">
          <input
            type="checkbox"
            checked={relevantOnly}
            onChange={(e) => setRelevantOnly(e.target.checked)}
          />
          Apenas relevantes
        </label>
      </div>

      {error && <div className="error">{error}</div>}

      <div className="news-grid">
        {news.map((article) => (
          <div
            key={article.id}
            className={`news-card ${article.is_relevant ? 'relevant' : ''}`}
          >
            <div className="news-card-header">
              <h3>{article.title}</h3>
              {article.is_relevant && (
                <span className="badge relevant-badge">Relevante</span>
              )}
            </div>

            <div className="news-card-meta">
              <span className="source">{article.source}</span>
              <span className="date">
                {new Date(article.scraped_date).toLocaleDateString('pt-BR')}
              </span>
            </div>

            {article.scope && (
              <div className="news-card-info">
                <strong>Escopo:</strong> {article.scope}
              </div>
            )}

            {article.responsible_area && (
              <div className="news-card-info">
                <strong>Área Responsável:</strong> {article.responsible_area}
              </div>
            )}

            {article.content && (
              <p className="news-content">{article.content.substring(0, 200)}...</p>
            )}

            <div className="news-card-actions">
              <a
                href={article.url}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-primary"
              >
                Ver Notícia
              </a>
              {!article.processed && (
                <button
                  className="btn btn-secondary"
                  onClick={() => handleMarkProcessed(article.id)}
                >
                  Marcar como Processada
                </button>
              )}
            </div>
          </div>
        ))}
      </div>

      {news.length === 0 && (
        <div className="empty-state">
          <p>Nenhuma notícia encontrada.</p>
        </div>
      )}
    </div>
  )
}

export default NewsList

