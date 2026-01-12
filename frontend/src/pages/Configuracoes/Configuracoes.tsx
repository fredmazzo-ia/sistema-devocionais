import { useEffect, useState } from 'react'
import { configApi } from '../../services/api'
import { Settings, Save, RefreshCw, Clock, Shield, AlertCircle } from 'lucide-react'
import './Configuracoes.css'

interface ConfigData {
  shield: {
    enabled: boolean
    delay_variation: number
    break_interval: number
    break_duration_min: number
    break_duration_max: number
    min_engagement_score: number
    adaptive_limits_enabled: boolean
    block_detection_enabled: boolean
  }
  rate_limit: {
    delay_between_messages: number
    max_messages_per_hour: number
    max_messages_per_day: number
    max_retries: number
    retry_delay: number
  }
  schedule: {
    send_time: string
  }
}

export default function Configuracoes() {
  const [config, setConfig] = useState<ConfigData | null>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)

  useEffect(() => {
    loadConfig()
  }, [])

  const loadConfig = async () => {
    try {
      setLoading(true)
      const data = await configApi.get()
      setConfig(data)
      setError(null)
    } catch (err: any) {
      setError(err.message || 'Erro ao carregar configurações')
    } finally {
      setLoading(false)
    }
  }

  const handleSaveShield = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!config) return

    setSaving(true)
    setError(null)
    setSuccess(null)

    try {
      await configApi.updateShield(config.shield)
      setSuccess('Configurações de blindagem atualizadas! Reinicie a aplicação para aplicar.')
    } catch (err: any) {
      setError(err.message || 'Erro ao salvar configurações de blindagem')
    } finally {
      setSaving(false)
    }
  }

  const handleSaveRateLimit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!config) return

    setSaving(true)
    setError(null)
    setSuccess(null)

    try {
      await configApi.updateRateLimit(config.rate_limit)
      setSuccess('Configurações de rate limiting atualizadas! Reinicie a aplicação para aplicar.')
    } catch (err: any) {
      setError(err.message || 'Erro ao salvar configurações de rate limiting')
    } finally {
      setSaving(false)
    }
  }

  const handleSaveSchedule = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!config) return

    setSaving(true)
    setError(null)
    setSuccess(null)

    try {
      await configApi.updateSchedule({ send_time: config.schedule.send_time })
      setSuccess('Horário de envio atualizado! Reinicie a aplicação para aplicar.')
    } catch (err: any) {
      setError(err.message || 'Erro ao salvar horário de envio')
    } finally {
      setSaving(false)
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

  if (!config) {
    return (
      <div className="error-message">
        <p>Erro ao carregar configurações</p>
        <button onClick={loadConfig}>Tentar novamente</button>
      </div>
    )
  }

  return (
    <div className="configuracoes-page">
      <div className="configuracoes-header">
        <Settings size={24} />
        <h2>Configurações</h2>
        <button className="btn-refresh" onClick={loadConfig}>
          <RefreshCw size={18} />
          <span>Atualizar</span>
        </button>
      </div>

      {error && (
        <div className="alert alert-error">
          <AlertCircle size={18} />
          <p>{error}</p>
        </div>
      )}

      {success && (
        <div className="alert alert-success">
          <p>{success}</p>
        </div>
      )}

      <div className="configuracoes-content">
        {/* Blindagem */}
        <section className="config-section">
          <form onSubmit={handleSaveShield}>
            <div className="section-header">
              <Shield size={20} />
              <h3>Blindagem Anti-Bloqueio</h3>
            </div>
            <div className="section-content">
              <div className="form-grid">
                <div className="form-group">
                  <label>
                    <input
                      type="checkbox"
                      checked={config.shield.enabled}
                      onChange={(e) =>
                        setConfig({
                          ...config,
                          shield: { ...config.shield, enabled: e.target.checked },
                        })
                      }
                    />
                    <span>Blindagem Ativada</span>
                  </label>
                </div>

                <div className="form-group">
                  <label>Variação de Delay (%)</label>
                  <input
                    type="number"
                    min="0"
                    max="1"
                    step="0.1"
                    value={config.shield.delay_variation}
                    onChange={(e) =>
                      setConfig({
                        ...config,
                        shield: {
                          ...config.shield,
                          delay_variation: parseFloat(e.target.value),
                        },
                      })
                    }
                  />
                </div>

                <div className="form-group">
                  <label>Intervalo entre Pausas (mensagens)</label>
                  <input
                    type="number"
                    min="1"
                    value={config.shield.break_interval}
                    onChange={(e) =>
                      setConfig({
                        ...config,
                        shield: {
                          ...config.shield,
                          break_interval: parseInt(e.target.value),
                        },
                      })
                    }
                  />
                </div>

                <div className="form-group">
                  <label>Duração Mínima da Pausa (segundos)</label>
                  <input
                    type="number"
                    min="0"
                    step="0.1"
                    value={config.shield.break_duration_min}
                    onChange={(e) =>
                      setConfig({
                        ...config,
                        shield: {
                          ...config.shield,
                          break_duration_min: parseFloat(e.target.value),
                        },
                      })
                    }
                  />
                </div>

                <div className="form-group">
                  <label>Duração Máxima da Pausa (segundos)</label>
                  <input
                    type="number"
                    min="0"
                    step="0.1"
                    value={config.shield.break_duration_max}
                    onChange={(e) =>
                      setConfig({
                        ...config,
                        shield: {
                          ...config.shield,
                          break_duration_max: parseFloat(e.target.value),
                        },
                      })
                    }
                  />
                </div>

                <div className="form-group">
                  <label>Score Mínimo de Engajamento</label>
                  <input
                    type="number"
                    min="0"
                    max="1"
                    step="0.1"
                    value={config.shield.min_engagement_score}
                    onChange={(e) =>
                      setConfig({
                        ...config,
                        shield: {
                          ...config.shield,
                          min_engagement_score: parseFloat(e.target.value),
                        },
                      })
                    }
                  />
                </div>

                <div className="form-group">
                  <label>
                    <input
                      type="checkbox"
                      checked={config.shield.adaptive_limits_enabled}
                      onChange={(e) =>
                        setConfig({
                          ...config,
                          shield: {
                            ...config.shield,
                            adaptive_limits_enabled: e.target.checked,
                          },
                        })
                      }
                    />
                    <span>Limites Adaptativos</span>
                  </label>
                </div>

                <div className="form-group">
                  <label>
                    <input
                      type="checkbox"
                      checked={config.shield.block_detection_enabled}
                      onChange={(e) =>
                        setConfig({
                          ...config,
                          shield: {
                            ...config.shield,
                            block_detection_enabled: e.target.checked,
                          },
                        })
                      }
                    />
                    <span>Detecção de Bloqueios</span>
                  </label>
                </div>
              </div>

              <button type="submit" className="btn-save" disabled={saving}>
                <Save size={18} />
                <span>{saving ? 'Salvando...' : 'Salvar Blindagem'}</span>
              </button>
            </div>
          </form>
        </section>

        {/* Rate Limiting */}
        <section className="config-section">
          <form onSubmit={handleSaveRateLimit}>
            <div className="section-header">
              <Shield size={20} />
              <h3>Rate Limiting</h3>
            </div>
            <div className="section-content">
              <div className="form-grid">
                <div className="form-group">
                  <label>Delay entre Mensagens (segundos)</label>
                  <input
                    type="number"
                    min="0"
                    step="0.1"
                    value={config.rate_limit.delay_between_messages}
                    onChange={(e) =>
                      setConfig({
                        ...config,
                        rate_limit: {
                          ...config.rate_limit,
                          delay_between_messages: parseFloat(e.target.value),
                        },
                      })
                    }
                  />
                </div>

                <div className="form-group">
                  <label>Máximo de Mensagens por Hora</label>
                  <input
                    type="number"
                    min="1"
                    value={config.rate_limit.max_messages_per_hour}
                    onChange={(e) =>
                      setConfig({
                        ...config,
                        rate_limit: {
                          ...config.rate_limit,
                          max_messages_per_hour: parseInt(e.target.value),
                        },
                      })
                    }
                  />
                </div>

                <div className="form-group">
                  <label>Máximo de Mensagens por Dia</label>
                  <input
                    type="number"
                    min="1"
                    value={config.rate_limit.max_messages_per_day}
                    onChange={(e) =>
                      setConfig({
                        ...config,
                        rate_limit: {
                          ...config.rate_limit,
                          max_messages_per_day: parseInt(e.target.value),
                        },
                      })
                    }
                  />
                </div>

                <div className="form-group">
                  <label>Máximo de Tentativas (Retry)</label>
                    <input
                      type="number"
                      min="0"
                      value={config.rate_limit.max_retries}
                      onChange={(e) =>
                        setConfig({
                          ...config,
                          rate_limit: {
                            ...config.rate_limit,
                            max_retries: parseInt(e.target.value),
                          },
                        })
                      }
                    />
                </div>

                <div className="form-group">
                  <label>Delay entre Tentativas (segundos)</label>
                  <input
                    type="number"
                    min="0"
                    step="0.1"
                    value={config.rate_limit.retry_delay}
                    onChange={(e) =>
                      setConfig({
                        ...config,
                        rate_limit: {
                          ...config.rate_limit,
                          retry_delay: parseFloat(e.target.value),
                        },
                      })
                    }
                  />
                </div>
              </div>

              <button type="submit" className="btn-save" disabled={saving}>
                <Save size={18} />
                <span>{saving ? 'Salvando...' : 'Salvar Rate Limiting'}</span>
              </button>
            </div>
          </form>
        </section>

        {/* Agendamento */}
        <section className="config-section">
          <form onSubmit={handleSaveSchedule}>
            <div className="section-header">
              <Clock size={20} />
              <h3>Agendamento</h3>
            </div>
            <div className="section-content">
              <div className="form-group">
                <label>Horário de Envio Automático (HH:MM)</label>
                <input
                  type="time"
                  value={config.schedule.send_time}
                  onChange={(e) =>
                    setConfig({
                      ...config,
                      schedule: { ...config.schedule, send_time: e.target.value },
                    })
                  }
                />
                <small>Horário em que o devocional será enviado automaticamente todos os dias</small>
              </div>

              <button type="submit" className="btn-save" disabled={saving}>
                <Save size={18} />
                <span>{saving ? 'Salvando...' : 'Salvar Horário'}</span>
              </button>
            </div>
          </form>
        </section>
      </div>
    </div>
  )
}
