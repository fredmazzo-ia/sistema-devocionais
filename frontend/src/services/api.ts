import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface NewsArticle {
  id: number
  title: string
  content: string | null
  url: string
  source: string
  published_date: string | null
  scraped_date: string
  is_relevant: boolean
  relevance_score: number
  processed: boolean
  notified: boolean
  scope: string | null
  responsible_area: string | null
}

export interface Notification {
  id: number
  article: {
    id: number
    title: string
  }
  recipient_name: string
  recipient_phone: string
  status: string
  sent_at: string
}

export const newsApi = {
  getAll: async (skip = 0, limit = 50, relevantOnly = false) => {
    const response = await api.get('/news/', {
      params: { skip, limit, relevant_only: relevantOnly },
    })
    return response.data
  },

  getById: async (id: number) => {
    const response = await api.get(`/news/${id}`)
    return response.data
  },

  getRelevantCount: async () => {
    const response = await api.get('/news/relevant/count')
    return response.data
  },

  markAsProcessed: async (id: number) => {
    const response = await api.post(`/news/${id}/mark-processed`)
    return response.data
  },
}

export const monitoringApi = {
  start: async () => {
    const response = await api.post('/monitoring/start')
    return response.data
  },

  getStatus: async () => {
    const response = await api.get('/monitoring/status')
    return response.data
  },
}

export const notificationsApi = {
  getAll: async (skip = 0, limit = 50) => {
    const response = await api.get('/notifications/', {
      params: { skip, limit },
    })
    return response.data
  },

  getStats: async () => {
    const response = await api.get('/notifications/stats')
    return response.data
  },
}

export default api

