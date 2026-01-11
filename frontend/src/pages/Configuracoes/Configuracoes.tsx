import { useEffect, useState } from 'react'
import { statsApi } from '../../services/api'
import type { Stats } from '../../types'
import { Settings, Save, RefreshCw, Clock, Shield, Server } from 'lucide-react'
import './Configuracoes.css'

export default function Configuracoes() {
  const [stats, setStats] = useState<Stats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    try {
      setLoading(true)
      const data = await statsApi.get()
      setStats(data)
      setError(null)
    } catch (err: any) {
      setError(err.message || 'Erro ao carregar configurações')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="configuracoes-loading">
        <div className="spinner"></div>
        <p>Carregando configurações...</p>
      </div>
    )
  }

  return (
    <div className="configuracoes-page">
      <div className="configuracoes-header">
        <Settings size={24} />
        <h2>Configurações</h2>
      </div>

      {error && (
        <div className="error-message">
          <p>{error}</p>
          <button onClick={loadStats}>Tentar novamente</button>
        </div>
      )}

      {stats && (
        <div className="configuracoes-content">
          {/* Instâncias */}
          <section className="config-section">
            <div className="section-header">
              <Server size={20} />
              <h3>Instâncias WhatsApp</h3>
            </div>
            <div className="section-content">
              <div className="info-grid">
                <div className="info-item">
                  <span className="info-label">Total de Instâncias:</span>
                  <span className="info-value">{stats.total_instances || 0}</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Instâncias Ativas:</span>
                  <span className="info-value success">{stats.active_instances || 0}</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Instâncias Inativas:</span>
                  <span className="info-value warning">{stats.inactive_instances || 0}</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Instâncias com Erro:</span>
                  <span className="info-value error">{stats.error_instances || 0}</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Estratégia de Distribuição:</span>
                  <span className="info-value">{stats.distribution_strategy || 'round_robin'}</span>
                </div>
              </div>

              {stats.instances && stats.instances.length > 0 && (
                <div className="instances-list">
                  <h4>Lista de Instâncias</h4>
                  {stats.instances.map((instance) => (
                    <div key={instance.name} className="instance-card">
                      <div className="instance-header">
                        <span className="instance-name">{instance.name}</span>
                        <span className={`status-badge ${instance.status}`}>
                          {instance.status}
                        </span>
                      </div>
                      <div className="instance-details">
                        <div className="detail-item">
                          <span>Mensagens hoje:</span>
                          <span>{instance.messages_sent_today || 0} / {instance.max_messages_per_day || 0}</span>
                        </div>
                        <div className="detail-item">
                          <span>Mensagens esta hora:</span>
                          <span>{instance.messages_sent_this_hour || 0} / {instance.max_messages_per_hour || 0}</span>
                        </div>
                        {instance.phone_number && (
                          <div className="detail-item">
                            <span>Telefone:</span>
                            <span>{instance.phone_number}</span>
                          </div>
                        )}
                        {instance.last_error && (
                          <div className="detail-item error">
                            <span>Último erro:</span>
                            <span>{instance.last_error}</span>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </section>

          {/* Blindagem */}
          <section className="config-section">
            <div className="section-header">
              <Shield size={20} />
              <h3>Blindagem Anti-Bloqueio</h3>
            </div>
            <div className="section-content">
              {stats.shield ? (
                <div className="info-grid">
                  <div className="info-item">
                    <span className="info-label">Blindagem Ativa:</span>
                    <span className="info-value success">Sim</span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Mensagens desde última pausa:</span>
                    <span className="info-value">{stats.shield.messages_since_break || 0}</span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Pausas estratégicas ativas:</span>
                    <span className="info-value">{stats.shield.breaks_taken || 0}</span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Bloqueios detectados:</span>
                    <span className="info-value error">{stats.shield.blocks_detected || 0}</span>
                  </div>
                </div>
              ) : (
                <p className="no-data">Blindagem não configurada</p>
              )}
            </div>
          </section>

          {/* Estatísticas Gerais */}
          <section className="config-section">
            <div className="section-header">
              <RefreshCw size={20} />
              <h3>Estatísticas Gerais</h3>
            </div>
            <div className="section-content">
              <div className="info-grid">
                <div className="info-item">
                  <span className="info-label">Total Enviado:</span>
                  <span className="info-value">{stats.total_sent || 0}</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Total Falhou:</span>
                  <span className="info-value error">{stats.total_failed || 0}</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Total Bloqueado:</span>
                  <span className="info-value error">{stats.total_blocked || 0}</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Total de Retries:</span>
                  <span className="info-value warning">{stats.total_retries || 0}</span>
                </div>
              </div>
            </div>
          </section>

          {/* Horário de Envio */}
          <section className="config-section">
            <div className="section-header">
              <Clock size={20} />
              <h3>Agendamento</h3>
            </div>
            <div className="section-content">
              <p className="info-text">
                O horário de envio automático é configurado via variável de ambiente <code>DEVOCIONAL_SEND_TIME</code>.
                <br />
                Para alterar, edite a configuração no EasyPanel.
              </p>
            </div>
          </section>

          <div className="actions-bar">
            <button className="btn-refresh" onClick={loadStats}>
              <RefreshCw size={18} />
              <span>Atualizar</span>
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

