import { useEffect, useState } from 'react'
import { statsApi, instancesApi } from '../../services/api'
import type { Stats } from '../../types'
import { 
  Send, 
  CheckCircle, 
  XCircle, 
  Users, 
  Server, 
  TrendingUp,
  Clock,
  Shield,
  Activity
} from 'lucide-react'
import './Dashboard.css'

export default function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null)
  const [instances, setInstances] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadData()
    const interval = setInterval(loadData, 30000) // Atualizar a cada 30s
    return () => clearInterval(interval)
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      const [statsData, instancesData] = await Promise.all([
        statsApi.get(),
        instancesApi.list()
      ])
      setStats(statsData)
      setInstances(instancesData.instances || [])
      setError(null)
    } catch (err: any) {
      console.error('Erro ao carregar dados:', err)
      setError(err.message || 'Erro ao carregar dados')
    } finally {
      setLoading(false)
    }
  }

  if (loading && !stats) {
    return (
      <div className="dashboard-loading">
        <div className="spinner"></div>
        <p>Carregando dados...</p>
      </div>
    )
  }

  // Garantir que stats sempre tenha valores padrão
  const safeStats: Stats = stats || {
    total_sent: 0,
    total_failed: 0,
    total_blocked: 0,
    total_retries: 0,
    instances: [],
    distribution_strategy: 'round_robin'
  }

  const successRate =
    safeStats.total_sent + safeStats.total_failed > 0
      ? ((safeStats.total_sent / (safeStats.total_sent + safeStats.total_failed)) * 100).toFixed(1)
      : '0'

  const activeInstances = instances.filter((i) => i.status === 'active').length
  const totalInstances = instances.length
  const totalContacts = safeStats.total_sent > 0 ? Math.ceil(safeStats.total_sent / (activeInstances || 1)) : 0

  return (
    <div className="dashboard-modern">
      {error && (
        <div className="alert alert-error">
          <XCircle size={18} />
          <p>{error}</p>
          <button onClick={loadData} className="btn-retry">Tentar novamente</button>
        </div>
      )}

      {/* Header com título */}
      <div className="dashboard-header">
        <div>
          <h1>Visão Geral</h1>
          <p className="dashboard-subtitle">Monitoramento do sistema de devocionais</p>
        </div>
        <button onClick={loadData} className="btn-refresh" disabled={loading}>
          <Activity size={18} className={loading ? 'spinning' : ''} />
          <span>Atualizar</span>
        </button>
      </div>

      {/* Cards principais de estatísticas */}
      <div className="stats-grid-modern">
        <div className="stat-card-modern stat-primary">
          <div className="stat-icon-modern">
            <Send size={28} />
          </div>
          <div className="stat-content-modern">
            <h3>Mensagens Enviadas</h3>
            <p className="stat-value-modern">{safeStats.total_sent || 0}</p>
            <p className="stat-label-modern">Total de envios realizados</p>
          </div>
        </div>

        <div className="stat-card-modern stat-success">
          <div className="stat-icon-modern">
            <CheckCircle size={28} />
          </div>
          <div className="stat-content-modern">
            <h3>Taxa de Sucesso</h3>
            <p className="stat-value-modern">{successRate}%</p>
            <p className="stat-label-modern">
              {safeStats.total_sent || 0} de{' '}
              {(safeStats.total_sent || 0) + (safeStats.total_failed || 0)} envios
            </p>
          </div>
        </div>

        <div className="stat-card-modern stat-warning">
          <div className="stat-icon-modern">
            <Server size={28} />
          </div>
          <div className="stat-content-modern">
            <h3>Instâncias Ativas</h3>
            <p className="stat-value-modern">
              {activeInstances}/{totalInstances}
            </p>
            <p className="stat-label-modern">Evolution API conectadas</p>
          </div>
        </div>

        <div className="stat-card-modern stat-danger">
          <div className="stat-icon-modern">
            <XCircle size={28} />
          </div>
          <div className="stat-content-modern">
            <h3>Falhas</h3>
            <p className="stat-value-modern">{safeStats.total_failed || 0}</p>
            <p className="stat-label-modern">Tentativas: {safeStats.total_retries || 0}</p>
          </div>
        </div>
      </div>

      {/* Seção de Blindagem */}
      {safeStats.shield && (
        <div className="shield-card-modern">
          <div className="shield-header">
            <Shield size={24} />
            <h2>Sistema de Blindagem</h2>
            <span className={`shield-status-badge ${safeStats.shield.status === 'active' ? 'active' : 'warning'}`}>
              {safeStats.shield.status === 'active' ? 'Ativo' : 'Atenção'}
            </span>
          </div>
          <div className="shield-grid-modern">
            <div className="shield-item-modern">
              <span className="shield-label-modern">Taxa de Sucesso:</span>
              <span className="shield-value-modern">
                {(safeStats.shield.success_rate * 100).toFixed(1)}%
              </span>
            </div>
            <div className="shield-item-modern">
              <span className="shield-label-modern">Limite Atual:</span>
              <span className="shield-value-modern">
                {safeStats.shield.current_hourly_limit}/hora • {safeStats.shield.current_daily_limit}/dia
              </span>
            </div>
            <div className="shield-item-modern">
              <span className="shield-label-modern">Mensagens desde pausa:</span>
              <span className="shield-value-modern">{safeStats.shield.messages_since_break}</span>
            </div>
          </div>
        </div>
      )}

      {/* Resumo de Instâncias */}
      <div className="instances-summary-modern">
        <div className="instances-summary-header">
          <Server size={24} />
          <h2>Status das Instâncias</h2>
        </div>
        <div className="instances-summary-grid">
          {instances.length === 0 ? (
            <div className="empty-state-modern">
              <Server size={48} />
              <p>Nenhuma instância configurada</p>
              <small>Configure instâncias no arquivo .env</small>
            </div>
          ) : (
            instances.map((instance) => (
              <div key={instance.name} className="instance-summary-card">
                <div className="instance-summary-header">
                  <h3>{instance.name}</h3>
                  <span className={`status-badge-modern ${instance.status}`}>
                    {instance.status === 'active' ? 'Ativa' : 
                     instance.status === 'inactive' ? 'Inativa' :
                     instance.status === 'error' ? 'Erro' : 'Desconhecida'}
                  </span>
                </div>
                <div className="instance-summary-stats">
                  <div className="instance-summary-stat">
                    <Clock size={16} />
                    <span>Hoje: {instance.messages_sent_today || 0}/{instance.max_messages_per_day || 200}</span>
                  </div>
                  <div className="instance-summary-stat">
                    <TrendingUp size={16} />
                    <span>Esta hora: {instance.messages_sent_this_hour || 0}/{instance.max_messages_per_hour || 20}</span>
                  </div>
                </div>
                {instance.phone_number && (
                  <div className="instance-phone">
                    <span>📱 {instance.phone_number}</span>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}

