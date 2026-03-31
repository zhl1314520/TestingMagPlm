import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token') || sessionStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      sessionStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const authAPI = {
  login: (email, password) => api.post('/auth/login', { email, password }),
  getCurrentUser: () => api.get('/auth/me')
}

export const userAPI = {
  getList: (page = 1, pageSize = 10) => api.get('/users', { params: { page, page_size: pageSize } }),
  create: (data) => api.post('/users', data),
  delete: (id) => api.delete(`/users/${id}`),
  getDetail: (id) => api.get(`/users/${id}`),
  update: (id, data) => api.put(`/users/${id}`, data)
}

export const projectAPI = {
  getList: (page = 1, pageSize = 10) => api.get('/projects', { params: { page, page_size: pageSize } }),
  create: (data) => api.post('/projects', data),
  delete: (id) => api.delete(`/projects/${id}`),
  addMember: (id, data) => api.post(`/projects/${id}/members`, data),
  getMembers: (id) => api.get(`/projects/${id}/members`),
  removeMember: (memberId) => api.delete(`/projects/members/${memberId}`)
}

export const testcaseAPI = {
  getList: (page = 1, pageSize = 10, projectId = null, module = null, status = null) => 
    api.get('/testcases', { params: { page, page_size: pageSize, project_id: projectId, module, status } }),
  create: (data) => api.post('/testcases', data),
  get: (id) => api.get(`/testcases/${id}`),
  update: (id, data) => api.put(`/testcases/${id}`, data),
  delete: (id) => api.delete(`/testcases/${id}`)
}

export const executionAPI = {
  getList: (page = 1, pageSize = 10, projectId = null) => 
    api.get('/executions', { params: { page, page_size: pageSize, project_id: projectId } }),
  create: (data) => api.post('/executions', data),
  run: (id) => api.post(`/executions/${id}/run`),
  delete: (id) => api.delete(`/executions/${id}`)
}

export const bugAPI = {
  getList: (page = 1, pageSize = 10, projectId = null, status = null, priority = null) => 
    api.get('/bugs', { params: { page, page_size: pageSize, project_id: projectId, status, priority } }),
  create: (data) => api.post('/bugs', data),
  get: (id) => api.get(`/bugs/${id}`),
  update: (id, data) => api.put(`/bugs/${id}`, data),
  updateStatus: (id, status) => api.put(`/bugs/${id}/status`, null, { params: { status } }),
  delete: (id) => api.delete(`/bugs/${id}`)
}

export const reportAPI = {
  getList: (page = 1, pageSize = 10, projectId = null) => 
    api.get('/reports', { params: { page, page_size: pageSize, project_id: projectId } })
}

export const metricsAPI = {
  getOverview: () => api.get('/metrics/overview'),
  getTrend: () => api.get('/metrics/trend')
}

export default api
