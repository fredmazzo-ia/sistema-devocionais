import { useEffect, useState } from 'react'
import { dashboardApi, instancesApi } from '../../services/api'
import type { DashboardStats } from '../../types'
import { 
  Send, 
  CheckCircle, 
  XCircle, 
  Users, 
  Server, 
  TrendingUp,
  Clock,
  Shield,
  Activity,
  Eye,
  MessageSquare,
  FileText,
  Webhook,
  UserCheck,
  UserX,
  AlertCircle,
  BarChart3
} from 'lucide-react'
import './Dashboard.css'

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null)
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
        dashboardApi.getStats(),
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

  if (!stats) {
    return (
      <div className="dashboard-error">
        <AlertCircle size={48} />
        <p>Erro ao carregar estatísticas</p>
        <button onClick={loadData} className="btn-retry">Tentar novamente</button>
      </div>
    )
  }

  return (
    <div className="dashboard-modern">
      {error && (
        <div className="alert alert-error">
          <XCircle size={18} />
          <p>{error}</p>
          <button onClick={loadData} className="btn-retry">Tentar novamente</button>
        </div>
      )}

      {/* Header */}
      <div className="dashboard-header">
        <div>
          <h1>Visão Geral</h1>
          <p className="dashboard-subtitle">Monitoramento completo do sistema de devocionais</p>
        </div>
        <button onClick={loadData} className="btn-refresh" disabled={loading}>
          <Activity size={18} className={loading ? 'spinning' : ''} />
          <span>Atualizar</span>
        </button>
      </div>

      {/* Cards principais de mensagens */}
      <div className="dashboard-section">
        <h2 className="section-title">
          <Send size={24} />
          Mensagens
        </h2>
        <div className="stats-grid-modern">
          <div className="stat-card-modern stat-primary">
            <div className="stat-icon-modern">
              <Send size={28} />
            </div>
            <div className="stat-content-modern">
              <h3>Total Enviadas</h3>
              <p className="stat-value-modern">{stats.messages.total.toLocaleString()}</p>
              <p className="stat-label-modern">
                {stats.messages.today} hoje • {stats.messages.week} esta semana
              </p>
            </div>
          </div>

          <div className="stat-card-modern stat-success">
            <div className="stat-icon-modern">
              <CheckCircle size={28} />
            </div>
            <div className="stat-content-modern">
              <h3>Entregues</h3>
              <p className="stat-value-modern">{stats.messages.delivered.toLocaleString()}</p>
              <p className="stat-label-modern">
                Taxa: {stats.messages.delivery_rate}% • {stats.messages.read} lidas
              </p>
            </div>
          </div>

          <div className="stat-card-modern stat-info">
            <div className="stat-icon-modern">
              <Eye size={28} />
            </div>
            <div className="stat-content-modern">
              <h3>Lidas</h3>
              <p className="stat-value-modern">{stats.messages.read.toLocaleString()}</p>
              <p className="stat-label-modern">
                Taxa de leitura: {stats.messages.read_rate}%
              </p>
            </div>
          </div>

          <div className="stat-card-modern stat-danger">
            <div className="stat-icon-modern">
              <XCircle size={28} />
            </div>
            <div className="stat-content-modern">
              <h3>Falhas</h3>
              <p className="stat-value-modern">{stats.messages.failed.toLocaleString()}</p>
              <p className="stat-label-modern">
                {stats.messages.blocked} bloqueadas • {stats.messages.retries} retries
              </p>
            </div>
          </div>

          <div className="stat-card-modern stat-warning">
            <div className="stat-icon-modern">
              <TrendingUp size={28} />
            </div>
            <div className="stat-content-modern">
              <h3>Taxa de Sucesso</h3>
              <p className="stat-value-modern">{stats.messages.success_rate}%</p>
              <p className="stat-label-modern">
                {stats.messages.sent} enviadas com sucesso
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Cards de contatos */}
      <div className="dashboard-section">
        <h2 className="section-title">
          <Users size={24} />
          Contatos
        </h2>
        <div className="stats-grid-modern">
          <div className="stat-card-modern stat-primary">
            <div className="stat-icon-modern">
              <Users size={28} />
            </div>
            <div className="stat-content-modern">
              <h3>Total de Contatos</h3>
              <p className="stat-value-modern">{stats.contacts.total.toLocaleString()}</p>
              <p className="stat-label-modern">
                {stats.contacts.active} ativos • {stats.contacts.inactive} inativos
              </p>
            </div>
          </div>

          <div className="stat-card-modern stat-success">
            <div className="stat-icon-modern">
              <UserCheck size={28} />
            </div>
            <div className="stat-content-modern">
              <h3>Contatos Ativos</h3>
              <p className="stat-value-modern">{stats.contacts.active.toLocaleString()}</p>
              <p className="stat-label-modern">
                {stats.contacts.with_messages} receberam mensagens
              </p>
            </div>
          </div>

          <div className="stat-card-modern stat-info">
            <div className="stat-icon-modern">
              <TrendingUp size={28} />
            </div>
            <div className="stat-content-modern">
              <h3>Novos Contatos</h3>
              <p className="stat-value-modern">{stats.contacts.month.toLocaleString()}</p>
              <p className="stat-label-modern">
                {stats.contacts.today} hoje • {stats.contacts.week} esta semana
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Cards de consentimentos */}
      {stats.consents.total > 0 && (
        <div className="dashboard-section">
          <h2 className="section-title">
            <UserCheck size={24} />
            Consentimentos
          </h2>
          <div className="stats-grid-modern">
            <div className="stat-card-modern stat-success">
              <div className="stat-icon-modern">
                <UserCheck size={28} />
              </div>
              <div className="stat-content-modern">
                <h3>Aceitos</h3>
                <p className="stat-value-modern">{stats.consents.accepted.toLocaleString()}</p>
                <p className="stat-label-modern">
                  Taxa: {stats.consents.acceptance_rate}%
                </p>
              </div>
            </div>

            <div className="stat-card-modern stat-warning">
              <div className="stat-icon-modern">
                <Clock size={28} />
              </div>
              <div className="stat-content-modern">
                <h3>Aguardando</h3>
                <p className="stat-value-modern">{stats.consents.pending.toLocaleString()}</p>
                <p className="stat-label-modern">
                  {stats.consents.awaiting_response} aguardando resposta
                </p>
              </div>
            </div>

            <div className="stat-card-modern stat-danger">
              <div className="stat-icon-modern">
                <UserX size={28} />
              </div>
              <div className="stat-content-modern">
                <h3>Negados</h3>
                <p className="stat-value-modern">{stats.consents.denied.toLocaleString()}</p>
                <p className="stat-label-modern">Contatos que recusaram</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Cards de devocionais */}
      <div className="dashboard-section">
        <h2 className="section-title">
          <FileText size={24} />
          Devocionais
        </h2>
        <div className="stats-grid-modern">
          <div className="stat-card-modern stat-primary">
            <div className="stat-icon-modern">
              <FileText size={28} />
            </div>
            <div className="stat-content-modern">
              <h3>Total de Devocionais</h3>
              <p className="stat-value-modern">{stats.devocionais.total.toLocaleString()}</p>
              <p className="stat-label-modern">
                {stats.devocionais.sent} enviados • {stats.devocionais.pending} pendentes
              </p>
            </div>
          </div>

          <div className="stat-card-modern stat-info">
            <div className="stat-icon-modern">
              <TrendingUp size={28} />
            </div>
            <div className="stat-content-modern">
              <h3>Criados Este Mês</h3>
              <p className="stat-value-modern">{stats.devocionais.month.toLocaleString()}</p>
              <p className="stat-label-modern">
                {stats.devocionais.today} hoje • {stats.devocionais.week} esta semana
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Cards de webhooks */}
      {stats.webhooks.total > 0 && (
        <div className="dashboard-section">
          <h2 className="section-title">
            <Webhook size={24} />
            Webhooks
          </h2>
          <div className="stats-grid-modern">
            <div className="stat-card-modern stat-primary">
              <div className="stat-icon-modern">
                <Webhook size={28} />
              </div>
              <div className="stat-content-modern">
                <h3>Total Recebidos</h3>
                <p className="stat-value-modern">{stats.webhooks.total.toLocaleString()}</p>
                <p className="stat-label-modern">
                  {stats.webhooks.processed} processados • {stats.webhooks.pending} pendentes
                </p>
              </div>
            </div>

            <div className="stat-card-modern stat-success">
              <div className="stat-icon-modern">
                <CheckCircle size={28} />
              </div>
              <div className="stat-content-modern">
                <h3>Taxa de Processamento</h3>
                <p className="stat-value-modern">{stats.webhooks.processing_rate}%</p>
                <p className="stat-label-modern">
                  {stats.webhooks.today} recebidos hoje
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Cards de engajamento */}
      {stats.engagement.total_records > 0 && (
        <div className="dashboard-section">
          <h2 className="section-title">
            <BarChart3 size={24} />
            Engajamento
          </h2>
          <div className="stats-grid-modern">
            <div className="stat-card-modern stat-primary">
              <div className="stat-icon-modern">
                <TrendingUp size={28} />
              </div>
              <div className="stat-content-modern">
                <h3>Score Médio</h3>
                <p className="stat-value-modern">{stats.engagement.avg_score.toFixed(1)}</p>
                <p className="stat-label-modern">
                  {stats.engagement.high_engagement_count} alto • {stats.engagement.low_engagement_count} baixo
                </p>
              </div>
            </div>

            <div className="stat-card-modern stat-info">
              <div className="stat-icon-modern">
                <MessageSquare size={28} />
              </div>
              <div className="stat-content-modern">
                <h3>Respostas</h3>
                <p className="stat-value-modern">{stats.engagement.total_responses.toLocaleString()}</p>
                <p className="stat-label-modern">
                  {stats.engagement.total_read} lidas • {stats.engagement.total_delivered} entregues
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Instâncias */}
      <div className="dashboard-section">
        <h2 className="section-title">
          <Server size={24} />
          Instâncias Evolution API
        </h2>
        <div className="instances-summary-modern">
          <div className="instances-summary-grid">
            {instances.length === 0 ? (
              <div className="empty-state-modern">
                <Server size={48} />
                <p>Nenhuma instância configurada</p>
                <small>Configure instâncias no arquivo .env</small>
              </div>
            ) : (
              <>
                <div className="stat-card-modern stat-primary">
                  <div className="stat-icon-modern">
                    <Server size={28} />
                  </div>
                  <div className="stat-content-modern">
                    <h3>Total de Instâncias</h3>
                    <p className="stat-value-modern">{stats.instances.total}</p>
                    <p className="stat-label-modern">
                      {stats.instances.active} ativas • {stats.instances.inactive} inativas
                    </p>
                  </div>
                </div>

                <div className="stat-card-modern stat-info">
                  <div className="stat-icon-modern">
                    <Send size={28} />
                  </div>
                  <div className="stat-content-modern">
                    <h3>Mensagens Hoje</h3>
                    <p className="stat-value-modern">{stats.instances.messages_today.toLocaleString()}</p>
                    <p className="stat-label-modern">
                      {stats.instances.messages_this_hour} nesta hora
                    </p>
                  </div>
                </div>

                {instances.map((instance) => (
                  <div key={instance.name} className="instance-summary-card">
                    <div className="instance-summary-header">
                      <h3>{instance.display_name || instance.name}</h3>
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
                ))}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
