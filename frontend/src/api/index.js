import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'  // 后端 API 运行端口

// axios：用来发送 HTTP 请求（get, post, delete, put...）,和服务器数据交互.自动解析 JSON
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Axios 请求拦截器配置，实现了一个全局的自动登录态注入功能
api.interceptors.request.use(   // 发送请求之前执行这个函数
  // 下面函数是 function(config) { ... } 的缩写
  
  // config：函数参数，包含url(请求地址)，method（请求方法），headers（请求头）, data(发送的数据)
  (config) => {

    // 获取 token，从localStorage（浏览器本地存储） 或者 sessionStorage（会话存储）中获取token
    const token = localStorage.getItem('token') || sessionStorage.getItem('token')

    // 把token注入 Authorization 
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // 放行请求，相当于告诉 Axios："好了，我改完了，你可以带着这个新的配置继续发送请求了。"
    return config
  },

  // 参数2：错误回调函数
  (error) => {
    return Promise.reject(error)
  }
)

// Axios 响应拦截器，统一处理后端返回的响应和错误
api.interceptors.response.use(

  // 参数1：成功回调函数，接受后端 response 
  (response) => response,

  // 
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
  getCurrentUser: () => api.get('/auth/me'),
  // 忘记密码的3个相关接口
  sendResetCode: (email) => api.post('/password-reset/send-code', {}, { params: { email } }),
  verifyResetCode: (email, code) => api.post('/password-reset/verify-code', {}, { params: { email, code } }),
  resetPassword: (email, code, newPassword) => api.post('/password-reset/reset-password', {}, { params: { email, code, new_password: newPassword } })
}

export const userAPI = {
  getList: (page = 1, pageSize = 10) => api.get('/users', { params: { page, page_size: pageSize } }),
  create: (data) => api.post('/users', data),
  delete: (id) => api.delete(`/users/${id}`),
  getDetail: (id) => api.get(`/users/${id}`),
  update: (id, data) => api.put(`/users/${id}`, data),
  // 个人信息-修改密码接口
  changePassword: (id, data) => api.put(`/users/${id}/password`, data)
}

export const projectAPI = {
  getList: (page = 1, pageSize = 10) => api.get('/projects', { params: { page, page_size: pageSize } }),
  create: (data) => api.post('/projects', data),
  update: (id, data) => api.put(`/projects/${id}`, data),
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
  get: (id) => api.get(`/executions/${id}`),
  create: (data) => api.post('/executions', data),
  update: (id, data) => api.put(`/executions/${id}`, data),
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
  getOverview: (params = {}) => api.get('/metrics/overview', { params }),
  getTrend: () => api.get('/metrics/trend'),
  getProjectProgress: () => api.get('/metrics/project-progress'),
  getRecentActivities: (limit = 10) => api.get('/metrics/recent-activities', { params: { limit } })
}

export default api
