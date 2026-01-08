import { useState, useEffect } from 'react'
import { newsApi, monitoringApi, notificationsApi } from '../services/api'
import './Dashboard.css'

interface Stats {
  relevantCount: number
  monitoringStatus: { running: boolean; message: string }
  notificationStats: {
    total: number
    sent: number
    failed: number
    success_rate: number
  }
}

function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadStats()
    const interval = setInterval(loadStats, 30000) // Atualizar a cada 30s
    return () => clearInterval(interval)
  }, [])

  const loadStats = async () => {
    try {
      setLoading(true)
      const [relevantCount, monitoringStatus, notificationStats] = await Promise.all([
        newsApi.getRelevantCount(),
        monitoringApi.getStatus(),
        notificationsApi.getStats(),
      ])

      setStats({
        relevantCount: relevantCount.count,
        monitoringStatus,
        notificationStats,
      })
      setError(null)
    } catch (err: any) {
      setError(err.message || 'Erro ao carregar estatísticas')
    } finally {
      setLoading(false)
    }
  }

  const handleStartMonitoring = async () => {
    try {
      await monitoringApi.start()
      await loadStats()
    } catch (err: any) {
      setError(err.message || 'Erro ao iniciar monitoramento')
    }
  }

  if (loading && !stats) {
    return <div className="loading">Carregando...</div>
  }

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>

      {error && <div className="error">{error}</div>}

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">📰</div>
          <div className="stat-content">
            <h3>Notícias Relevantes</h3>
            <p className="stat-value">{stats?.relevantCount || 0}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🔄</div>
          <div className="stat-content">
            <h3>Status do Monitoramento</h3>
            <p className={`stat-value ${stats?.monitoringStatus.running ? 'active' : 'inactive'}`}>
              {stats?.monitoringStatus.running ? 'Ativo' : 'Inativo'}
            </p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📱</div>
          <div className="stat-content">
            <h3>Notificações Enviadas</h3>
            <p className="stat-value">{stats?.notificationStats.sent || 0}</p>
            <p className="stat-subtitle">
              {stats?.notificationStats.success_rate.toFixed(1) || 0}% de sucesso
            </p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">⚠️</div>
          <div className="stat-content">
            <h3>Notificações Falhadas</h3>
            <p className="stat-value">{stats?.notificationStats.failed || 0}</p>
          </div>
        </div>
      </div>

      <div className="card">
        <h2>Ações</h2>
        <button className="btn btn-primary" onClick={handleStartMonitoring}>
          Executar Monitoramento Agora
        </button>
        <button className="btn btn-secondary" onClick={loadStats} style={{ marginLeft: '1rem' }}>
          Atualizar Estatísticas
        </button>
      </div>
    </div>
  )
}

export default Dashboard

