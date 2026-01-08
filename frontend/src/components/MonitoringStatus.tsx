import { useState, useEffect } from 'react'
import { monitoringApi } from '../services/api'
import './MonitoringStatus.css'

function MonitoringStatus() {
  const [status, setStatus] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [executing, setExecuting] = useState(false)

  useEffect(() => {
    loadStatus()
    const interval = setInterval(loadStatus, 5000) // Atualizar a cada 5s
    return () => clearInterval(interval)
  }, [])

  const loadStatus = async () => {
    try {
      const data = await monitoringApi.getStatus()
      setStatus(data)
      setError(null)
    } catch (err: any) {
      setError(err.message || 'Erro ao carregar status')
    } finally {
      setLoading(false)
    }
  }

  const handleStartMonitoring = async () => {
    try {
      setExecuting(true)
      await monitoringApi.start()
      await loadStatus()
    } catch (err: any) {
      setError(err.message || 'Erro ao iniciar monitoramento')
    } finally {
      setExecuting(false)
    }
  }

  if (loading && !status) {
    return <div className="loading">Carregando status...</div>
  }

  return (
    <div className="monitoring-status">
      <h1>Status do Monitoramento</h1>

      {error && <div className="error">{error}</div>}

      <div className="card">
        <div className="status-display">
          <div className={`status-indicator ${status?.running ? 'active' : 'inactive'}`}>
            <div className="status-dot"></div>
            <span>{status?.running ? 'Ativo' : 'Inativo'}</span>
          </div>
          <p className="status-message">{status?.message || 'Carregando...'}</p>
        </div>

        <div className="monitoring-actions">
          <button
            className="btn btn-primary"
            onClick={handleStartMonitoring}
            disabled={executing}
          >
            {executing ? 'Executando...' : 'Executar Monitoramento Agora'}
          </button>
          <button className="btn btn-secondary" onClick={loadStatus}>
            Atualizar Status
          </button>
        </div>
      </div>

      <div className="card">
        <h2>Informações</h2>
        <div className="info-list">
          <div className="info-item">
            <strong>Intervalo de Monitoramento:</strong> A cada 30 minutos
          </div>
          <div className="info-item">
            <strong>Portais Monitorados:</strong> Configurados em backend/app/config.py
          </div>
          <div className="info-item">
            <strong>Palavras-chave:</strong> Assistência Social, CRAS, CREAS, etc.
          </div>
        </div>
      </div>
    </div>
  )
}

export default MonitoringStatus

