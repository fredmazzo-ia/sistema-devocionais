import { useState, useEffect } from 'react'
import { notificationsApi, Notification } from '../services/api'
import './Notifications.css'

function Notifications() {
  const [notifications, setNotifications] = useState<Notification[]>([])
  const [stats, setStats] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      const [notifs, notificationStats] = await Promise.all([
        notificationsApi.getAll(),
        notificationsApi.getStats(),
      ])
      setNotifications(notifs)
      setStats(notificationStats)
      setError(null)
    } catch (err: any) {
      setError(err.message || 'Erro ao carregar notificações')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="loading">Carregando notificações...</div>
  }

  return (
    <div className="notifications">
      <h1>Notificações</h1>

      {error && <div className="error">{error}</div>}

      {stats && (
        <div className="stats-summary">
          <div className="stat-item">
            <span className="stat-label">Total:</span>
            <span className="stat-value">{stats.total}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Enviadas:</span>
            <span className="stat-value success">{stats.sent}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Falhadas:</span>
            <span className="stat-value error">{stats.failed}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Taxa de Sucesso:</span>
            <span className="stat-value">{stats.success_rate.toFixed(1)}%</span>
          </div>
        </div>
      )}

      <div className="notifications-list">
        {notifications.map((notif) => (
          <div
            key={notif.id}
            className={`notification-card ${notif.status === 'sent' ? 'success' : 'failed'}`}
          >
            <div className="notification-header">
              <h3>{notif.article.title}</h3>
              <span className={`status-badge ${notif.status}`}>
                {notif.status === 'sent' ? '✓ Enviada' : '✗ Falhou'}
              </span>
            </div>

            <div className="notification-details">
              <div className="detail-item">
                <strong>Destinatário:</strong> {notif.recipient_name}
              </div>
              <div className="detail-item">
                <strong>Telefone:</strong> {notif.recipient_phone}
              </div>
              <div className="detail-item">
                <strong>Enviada em:</strong>{' '}
                {new Date(notif.sent_at).toLocaleString('pt-BR')}
              </div>
            </div>
          </div>
        ))}
      </div>

      {notifications.length === 0 && (
        <div className="empty-state">
          <p>Nenhuma notificação encontrada.</p>
        </div>
      )}
    </div>
  )
}

export default Notifications

