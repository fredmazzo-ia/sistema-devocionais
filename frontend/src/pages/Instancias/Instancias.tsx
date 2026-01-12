import { useEffect, useState } from 'react'
import { instancesApi } from '../../services/api'
import { 
  Server, 
  RefreshCw, 
  QrCode, 
  CheckCircle, 
  XCircle, 
  AlertCircle, 
  Loader,
  Wifi,
  WifiOff,
  Phone,
  Clock,
  TrendingUp
} from 'lucide-react'
import './Instancias.css'

interface Instancia {
  name: string
  api_url: string
  display_name: string
  status: 'active' | 'inactive' | 'error' | 'blocked' | 'unknown'
  phone_number: string | null
  messages_sent_today: number
  messages_sent_this_hour: number
  max_messages_per_hour: number
  max_messages_per_day: number
  priority: number
  enabled: boolean
  last_check: string | null
  last_error: string | null
  error_count: number
}

export default function Instancias() {
  const [instances, setInstances] = useState<Instancia[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [qrCode, setQrCode] = useState<{ instance: string; qr: string } | null>(null)
  const [refreshing, setRefreshing] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  const [checkingConnection, setCheckingConnection] = useState<string | null>(null)

  useEffect(() => {
    loadInstances()
    const interval = setInterval(loadInstances, 30000) // Atualizar a cada 30s
    return () => clearInterval(interval)
  }, [])

  const loadInstances = async () => {
    try {
      setLoading(true)
      const data = await instancesApi.list()
      setInstances(data.instances || [])
      setError(null)
    } catch (err: any) {
      setError(err.message || 'Erro ao carregar instâncias')
    } finally {
      setLoading(false)
    }
  }

  const handleGenerateQR = async (instanceName: string) => {
    try {
      setError(null)
      setSuccess(null)
      const data = await instancesApi.generateQR(instanceName)
      setQrCode({
        instance: instanceName,
        qr: data.qr_code || data.base64 || '',
      })
      setSuccess('QR Code gerado com sucesso! Escaneie com o WhatsApp.')
    } catch (err: any) {
      setError(err.message || 'Erro ao gerar QR code')
      setQrCode(null)
    }
  }

  const handleConnect = async (instanceName: string) => {
    try {
      setCheckingConnection(instanceName)
      setError(null)
      setSuccess(null)
      const data = await instancesApi.connect(instanceName)
      if (data.connected) {
        setSuccess(`✅ Instância ${instanceName} está conectada!`)
      } else {
        setError(`⚠️ Instância ${instanceName} não está conectada. Estado: ${data.state || 'desconhecido'}`)
      }
      await loadInstances()
    } catch (err: any) {
      setError(err.message || 'Erro ao verificar conexão')
    } finally {
      setCheckingConnection(null)
    }
  }

  const handleRefresh = async (instanceName: string) => {
    try {
      setRefreshing(instanceName)
      setError(null)
      setSuccess(null)
      await instancesApi.refresh(instanceName)
      setSuccess(`Status da instância ${instanceName} atualizado!`)
      await loadInstances()
    } catch (err: any) {
      setError(err.message || 'Erro ao atualizar status')
    } finally {
      setRefreshing(null)
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
        return <CheckCircle size={20} className="status-icon active" />
      case 'error':
        return <XCircle size={20} className="status-icon error" />
      case 'blocked':
        return <AlertCircle size={20} className="status-icon blocked" />
      default:
        return <AlertCircle size={20} className="status-icon inactive" />
    }
  }

  const getStatusLabel = (status: string) => {
    const labels: Record<string, string> = {
      active: 'Conectada',
      inactive: 'Desconectada',
      error: 'Erro',
      blocked: 'Bloqueada',
      unknown: 'Desconhecida',
    }
    return labels[status] || status
  }

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      active: '#10b981',
      inactive: '#f59e0b',
      error: '#ef4444',
      blocked: '#dc2626',
      unknown: '#6b7280',
    }
    return colors[status] || '#6b7280'
  }

  if (loading) {
    return (
      <div className="instancias-loading">
        <div className="spinner"></div>
        <p>Carregando instâncias...</p>
      </div>
    )
  }

  return (
    <div className="instancias-page-modern">
      <div className="instancias-header-modern">
        <div>
          <h1>Gerenciar Instâncias WhatsApp</h1>
          <p className="instancias-subtitle">Configure e monitore suas instâncias Evolution API</p>
        </div>
        <button className="btn-refresh-modern" onClick={loadInstances} disabled={loading}>
          <RefreshCw size={18} className={loading ? 'spinning' : ''} />
          <span>Atualizar</span>
        </button>
      </div>

      {error && (
        <div className="alert-modern alert-error-modern">
          <AlertCircle size={18} />
          <p>{error}</p>
        </div>
      )}

      {success && (
        <div className="alert-modern alert-success-modern">
          <CheckCircle size={18} />
          <p>{success}</p>
        </div>
      )}

      {qrCode && (
        <div className="qr-modal-modern" onClick={() => setQrCode(null)}>
          <div className="qr-modal-content-modern" onClick={(e) => e.stopPropagation()}>
            <div className="qr-modal-header">
              <h3>QR Code - {qrCode.instance}</h3>
              <button className="btn-close-modern" onClick={() => setQrCode(null)}>
                <XCircle size={20} />
              </button>
            </div>
            <p className="qr-instructions">
              Escaneie este QR code com o WhatsApp para conectar a instância
            </p>
            {qrCode.qr && (
              <div className="qr-image-container">
                <img
                  src={qrCode.qr.startsWith('data:') ? qrCode.qr : `data:image/png;base64,${qrCode.qr}`}
                  alt="QR Code"
                  className="qr-image-modern"
                />
              </div>
            )}
            <button className="btn-primary-modern" onClick={() => setQrCode(null)}>
              Fechar
            </button>
          </div>
        </div>
      )}

      <div className="instances-grid-modern">
        {instances.length === 0 ? (
          <div className="empty-state-modern">
            <Server size={64} />
            <p>Nenhuma instância configurada</p>
            <small>Configure instâncias no arquivo .env do EasyPanel</small>
          </div>
        ) : (
          instances.map((instance) => (
            <div key={instance.name} className="instance-card-modern">
              <div className="instance-card-header-modern">
                <div className="instance-title-section">
                  <div className="instance-name-row">
                    <h3>{instance.name}</h3>
                    <span className={`status-badge-modern ${instance.status}`}>
                      {getStatusIcon(instance.status)}
                      {getStatusLabel(instance.status)}
                    </span>
                  </div>
                  <p className="instance-display-name">{instance.display_name}</p>
                </div>
                <div 
                  className="status-indicator-modern"
                  style={{ backgroundColor: getStatusColor(instance.status) }}
                >
                  {instance.status === 'active' ? <Wifi size={16} /> : <WifiOff size={16} />}
                </div>
              </div>

              <div className="instance-details-modern">
                <div className="detail-item-modern">
                  <span className="detail-label">URL da API:</span>
                  <span className="detail-value">{instance.api_url}</span>
                </div>
                
                {instance.phone_number ? (
                  <div className="detail-item-modern">
                    <Phone size={16} />
                    <span className="detail-value">{instance.phone_number}</span>
                  </div>
                ) : (
                  <div className="detail-item-modern detail-warning">
                    <AlertCircle size={16} />
                    <span>Número não identificado</span>
                  </div>
                )}

                <div className="instance-stats-modern">
                  <div className="instance-stat-modern">
                    <Clock size={16} />
                    <div>
                      <span className="stat-label-small">Hoje</span>
                      <span className="stat-value-small">
                        {instance.messages_sent_today} / {instance.max_messages_per_day}
                      </span>
                    </div>
                  </div>
                  <div className="instance-stat-modern">
                    <TrendingUp size={16} />
                    <div>
                      <span className="stat-label-small">Esta hora</span>
                      <span className="stat-value-small">
                        {instance.messages_sent_this_hour} / {instance.max_messages_per_hour}
                      </span>
                    </div>
                  </div>
                </div>

                {instance.last_error && (
                  <div className="detail-item-modern detail-error">
                    <AlertCircle size={16} />
                    <span className="error-text">{instance.last_error.substring(0, 100)}...</span>
                  </div>
                )}
              </div>

              <div className="instance-actions-modern">
                <button
                  className="btn-action-modern btn-primary"
                  onClick={() => handleRefresh(instance.name)}
                  disabled={refreshing === instance.name}
                >
                  {refreshing === instance.name ? (
                    <Loader size={16} className="spinning" />
                  ) : (
                    <RefreshCw size={16} />
                  )}
                  <span>Atualizar</span>
                </button>
                <button
                  className="btn-action-modern btn-secondary"
                  onClick={() => handleGenerateQR(instance.name)}
                >
                  <QrCode size={16} />
                  <span>QR Code</span>
                </button>
                <button
                  className="btn-action-modern btn-success"
                  onClick={() => handleConnect(instance.name)}
                  disabled={checkingConnection === instance.name}
                >
                  {checkingConnection === instance.name ? (
                    <Loader size={16} className="spinning" />
                  ) : (
                    <CheckCircle size={16} />
                  )}
                  <span>Verificar</span>
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
