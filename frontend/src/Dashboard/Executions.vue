<template>
  <div class="executions-page">
    <div class="page-content">
      <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <div class="title-badge">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polygon points="5 3 19 12 5 21 5 3"/>
            </svg>
            Test Runner
          </div>
          <h1 class="page-title">测试执行</h1>
          <p class="page-subtitle">执行和监控测试任务</p>
        </div>
        <button @click="showCreateModal = true" class="btn-create">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          创建执行
        </button>
      </div>
      <div class="header-decoration">
        <div class="deco-blob deco-blob-1"></div>
        <div class="deco-blob deco-blob-2"></div>
      </div>
    </div>

    <div class="filters-section">
      <div class="filters-container">
        <div class="filter-group">
          <div class="filter-label-row">
            <label class="filter-label">
              <span class="filter-icon">📁</span>
              项目
            </label>
            <div class="project-search-wrapper">
              <input 
                v-model="projectSearchKeyword" 
                type="text" 
                placeholder="搜索项目名称" 
                class="project-search-input"
              />
              <button @click="searchProjects" class="project-search-btn">查询</button>
            </div>
          </div>
          <select v-model="filters.project_id" @change="loadExecutions" class="filter-select">
            <option value="">全部项目</option>
            <option v-for="project in filteredProjects" :key="project.id" :value="project.id">
              {{ project.name }}
            </option>
          </select>
        </div>

        <div class="filter-stats">
          <div class="stat-badge">
            <span class="stat-dot"></span>
            <span class="stat-text">共 {{ executions.length }} 次执行</span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="executions.length === 0" class="empty-state">
      <div class="empty-icon">🎬</div>
      <h3>暂无执行记录</h3>
      <p>创建第一个测试执行来开始运行测试</p>
      <button @click="showCreateModal = true" class="btn-primary">创建执行</button>
    </div>

    <div v-else class="executions-grid">
      <div v-for="execution in executions" :key="execution.id" class="execution-card">
        <div class="card-glow"></div>
        <div class="card-header">
          <div class="execution-icon">
            <span class="icon-ring"></span>
            <span class="icon-emoji">{{ execution.type === 'auto' ? '🤖' : '👤' }}</span>
          </div>
          <div class="execution-status" :class="execution.status">
            <span class="status-dot"></span>
            <span class="status-text">{{ getStatusText(execution.status) }}</span>
          </div>
        </div>

        <div class="card-body">
          <h3 class="execution-title">{{ execution.name }}</h3>
          
          <div class="execution-meta">
            <div class="meta-item">
              <span class="meta-icon">🏷️</span>
              <span class="meta-label">类型</span>
              <span class="meta-value type-badge">{{ execution.type }}</span>
            </div>
          </div>

          <div class="execution-time">
            <svg class="time-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
              <line x1="16" y1="2" x2="16" y2="6"/>
              <line x1="8" y1="2" x2="8" y2="6"/>
              <line x1="3" y1="10" x2="21" y2="10"/>
            </svg>
            <span class="time-label">创建时间：</span>
            <span class="time-text">{{ formatDate(execution.created_at) }}</span>
          </div>

          <div v-if="hasUpdatedTime(execution)" class="execution-time">
            <svg class="time-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"/>
              <polyline points="12 6 12 12 16 14"/>
            </svg>
            <span class="time-label">更新时间：</span>
            <span class="time-text">{{ formatDate(execution.updated_at) }}</span>
          </div>

          <div v-if="execution.result" class="execution-result">
            <div class="result-label">
              <span class="label-icon">📊</span>
              执行结果
            </div>
            <pre class="result-content">{{ formatResult(execution.result) }}</pre>
          </div>
        </div>

        <div class="card-footer">
          <button 
            v-if="execution.status === '等待中'" 
            @click="runExecution(execution.id)" 
            class="btn-run"
          >
            <span class="run-icon">▶️</span>
            运行
          </button>
          <button @click="editExecution(execution)" class="btn-view">
            <span class="view-icon">✏️</span>
            修改
          </button>
          <button @click="showPassRate(execution)" class="btn-pass-rate">
            <span class="pass-rate-icon">📊</span>
            通过率
          </button>
          <button @click="deleteExecution(execution.id)" class="btn-delete">
            <span class="delete-icon">🗑</span>
            删除
          </button>
        </div>
      </div>
    </div>

    <Transition name="modal">
      <div v-if="showCreateModal" class="modal-overlay" @click="showCreateModal = false">
        <div class="modal-container" @click.stop>
          <div class="modal-header">
            <div class="modal-title">
              <span class="modal-icon">🎯</span>
              <h2>创建测试执行</h2>
            </div>
            <button @click="showCreateModal = false" class="btn-close">×</button>
          </div>
          
          <form @submit.prevent="createExecution" class="modal-body">
            <div class="form-group">
              <label class="form-label">
                <span class="label-icon">📁</span>
                选择项目
              </label>
              <select v-model="executionForm.project_id" required class="form-select">
                <option value="">选择项目</option>
                <option v-for="project in projects" :key="project.id" :value="project.id">
                  {{ project.name }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">
                <span class="label-icon">📝</span>
                执行名称
              </label>
              <input 
                v-model="executionForm.name" 
                type="text" 
                required 
                placeholder="输入执行名称"
                class="form-input"
              />
            </div>

            <div class="form-group">
              <label class="form-label">
                <span class="label-icon">⚙️</span>
                执行类型
              </label>
              <div class="type-selector">
                <button
                  type="button"
                  @click="executionForm.type = '手动执行'"
                  :class="['type-option', { active: executionForm.type === '手动执行' }]"
                >
                  <span class="type-icon">👤</span>
                  <span class="type-label">手动执行</span>
                </button>
                <button
                  type="button"
                  @click="executionForm.type = '自动化执行'"
                  :class="['type-option', { active: executionForm.type === '自动化执行' }]"
                >
                  <span class="type-icon">🤖</span>
                  <span class="type-label">自动执行</span>
                </button>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">
                <span class="label-icon">📊</span>
                执行状态
              </label>
              <select v-model="executionForm.status" class="form-select">
                <option value="等待中">等待中</option>
                <option value="执行中">执行中</option>
                <option value="已完成">已完成</option>
                <option value="失败">失败</option>
                <option value="已取消">已取消</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">
                <span class="label-icon">📝</span>
                执行结果 <span class="required-mark">*</span>
              </label>
              <textarea 
                v-model="executionForm.result" 
                placeholder="请输入执行结果"
                class="form-textarea"
                rows="3"
                required
              ></textarea>
            </div>
          </form>

          <div class="modal-footer">
            <button @click="showCreateModal = false" class="btn-cancel">取消</button>
            <button @click="createExecution" class="btn-submit">
              <span class="btn-spinner" v-if="loading"></span>
              <span v-else>创建执行</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <Transition name="modal">
      <div v-if="showEditModal" class="modal-overlay" @click="showEditModal = false">
        <div class="modal-container" @click.stop>
          <div class="modal-header">
            <div class="modal-title">
              <span class="modal-icon">✏️</span>
              <h2>修改测试执行</h2>
            </div>
            <button @click="showEditModal = false" class="btn-close">×</button>
          </div>
          
          <form @submit.prevent="updateExecution" class="modal-body">
            <div class="form-group">
              <label class="form-label">
                <span class="label-icon">📝</span>
                执行名称
              </label>
              <input 
                v-model="editForm.name" 
                type="text" 
                required 
                placeholder="输入执行名称"
                class="form-input"
              />
            </div>

            <div class="form-group">
              <label class="form-label">
                <span class="label-icon">⚙️</span>
                执行类型
              </label>
              <div class="type-selector">
                <button
                  type="button"
                  @click="editForm.type = '手动执行'"
                  :class="['type-option', { active: editForm.type === '手动执行' }]"
                >
                  <span class="type-icon">👤</span>
                  <span class="type-label">手动执行</span>
                </button>
                <button
                  type="button"
                  @click="editForm.type = '自动化执行'"
                  :class="['type-option', { active: editForm.type === '自动化执行' }]"
                >
                  <span class="type-icon">🤖</span>
                  <span class="type-label">自动执行</span>
                </button>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">
                <span class="label-icon">📊</span>
                执行状态
              </label>
              <select v-model="editForm.status" class="form-select">
                <option value="等待中">等待中</option>
                <option value="执行中">执行中</option>
                <option value="已完成">已完成</option>
                <option value="失败">失败</option>
                <option value="已取消">已取消</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">
                <span class="label-icon">📝</span>
                执行结果 <span class="required-mark">*</span>
              </label>
              <textarea 
                v-model="editForm.result" 
                placeholder="请输入执行结果"
                class="form-textarea"
                rows="3"
                required
              ></textarea>
            </div>
          </form>

          <div class="modal-footer">
            <button @click="showEditModal = false" class="btn-cancel">取消</button>
            <button @click="updateExecution" class="btn-submit">
              <span class="btn-spinner" v-if="loading"></span>
              <span v-else>保存修改</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <Transition name="modal">
      <div v-if="showPassRateModal" class="modal-overlay" @click="showPassRateModal = false">
        <div class="modal-container pass-rate-modal" @click.stop>
          <div class="modal-header">
            <div class="modal-title">
              <span class="modal-icon">📊</span>
              <h2>执行通过率统计</h2>
            </div>
            <button @click="showPassRateModal = false" class="btn-close">×</button>
          </div>
          
          <div class="modal-body">
            <div class="pass-rate-content">
              <div class="chart-container">
                <canvas ref="passRateChart"></canvas>
              </div>
              
              <div class="stats-summary">
                <div class="summary-item">
                  <div class="summary-label">总用例数</div>
                  <div class="summary-value">{{ selectedExecutionData?.total_cases || 0 }}</div>
                </div>
                <div class="summary-item passed">
                  <div class="summary-label">通过用例</div>
                  <div class="summary-value">{{ selectedExecutionData?.passed_cases || 0 }}</div>
                </div>
                <div class="summary-item failed">
                  <div class="summary-label">失败用例</div>
                  <div class="summary-value">{{ selectedExecutionData?.failed_cases || 0 }}</div>
                </div>
                <div class="summary-item rate">
                  <div class="summary-label">通过率</div>
                  <div class="summary-value">{{ selectedExecutionData?.pass_rate || 0 }}%</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <Transition name="toast">
      <div v-if="toast.show" class="toast-overlay" @click="hideToast">
        <div class="toast-container glass-panel" @click.stop>
          <div class="toast-icon" :class="toast.type">
            <svg v-if="toast.type === 'success'" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
            <svg v-else-if="toast.type === 'error'" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
            <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="12"/>
              <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
          </div>
          <div class="toast-content">
            <h3 class="toast-title">{{ toast.title }}</h3>
            <p class="toast-message">{{ toast.message }}</p>
          </div>
          <button @click="hideToast" class="toast-close">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
      </div>
    </Transition>

    <Transition name="confirm">
      <div v-if="confirmDialog.show" class="confirm-overlay" @click="cancelConfirm">
        <div class="confirm-container glass-panel" @click.stop>
          <div class="confirm-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
              <line x1="12" y1="9" x2="12" y2="13"/>
              <line x1="12" y1="17" x2="12.01" y2="17"/>
            </svg>
          </div>
          <div class="confirm-content">
            <h3 class="confirm-title">确认删除</h3>
            <p class="confirm-message">{{ confirmDialog.message }}</p>
          </div>
          <div class="confirm-actions">
            <button @click="cancelConfirm" class="confirm-btn cancel">取消</button>
            <button @click="confirmAction" class="confirm-btn delete">删除</button>
          </div>
        </div>
      </div>
    </Transition>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import { executionAPI, projectAPI } from '../api/index.js'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

const executions = ref([])
const projects = ref([])
const projectSearchKeyword = ref('')
const showCreateModal = ref(false)
const showEditModal = ref(false)
const showPassRateModal = ref(false)
const loading = ref(false)
const selectedExecution = ref(null)
const selectedExecutionData = ref(null)
const passRateChart = ref(null)
let chartInstance = null

const filters = ref({
  project_id: ''
})

const executionForm = ref({
  project_id: '',
  name: '',
  type: '手动执行',
  status: '等待中',
  result: ''
})

const editForm = ref({
  id: null,
  name: '',
  type: '',
  status: '',
  result: ''
})

const toast = ref({
  show: false,
  type: 'success',
  title: '',
  message: ''
})

const confirmDialog = ref({
  show: false,
  message: '',
  onConfirm: null
})

const statusMap = {
  '等待中': { text: '等待中', color: '#f59e0b' },
  '执行中': { text: '执行中', color: '#3b82f6' },
  '已完成': { text: '已完成', color: '#10b981' },
  '失败': { text: '失败', color: '#ef4444' },
  '已取消': { text: '已取消', color: '#9ca3af' }
}

const envMap = {
  test: '测试环境',
  staging: '预发布环境',
  production: '生产环境'
}

const filteredProjects = computed(() => {
  if (!projectSearchKeyword.value) {
    return projects.value
  }
  return projects.value.filter(project => 
    project.name.toLowerCase().includes(projectSearchKeyword.value.toLowerCase())
  )
})

const searchProjects = () => {
  console.log('搜索项目:', projectSearchKeyword.value)
}

onMounted(async () => {
  await loadProjects()
  await loadExecutions()
})

const loadProjects = async () => {
  try {
    const response = await projectAPI.getList(1, 100)
    projects.value = response.data.items
  } catch (error) {
    console.error('加载项目列表失败:', error)
  }
}

const loadExecutions = async () => {
  try {
    const response = await executionAPI.getList(
      1,
      100,
      filters.value.project_id || null
    )
    executions.value = response.data.items
  } catch (error) {
    console.error('加载执行列表失败:', error)
  }
}

const createExecution = async () => {
  if (!executionForm.value.name.trim()) {
    showToast('warning', '提示', '请输入执行名称')
    return
  }
  
  if (!executionForm.value.result.trim()) {
    showToast('warning', '提示', '请输入执行结果')
    return
  }
  
  loading.value = true
  try {
    await executionAPI.create(executionForm.value)
    showCreateModal.value = false
    executionForm.value = { project_id: '', name: '', type: '手动执行', status: '等待中', result: '' }
    await loadExecutions()
    showToast('success', '成功', '创建成功！')
  } catch (error) {
    console.error('创建执行失败:', error)
    showToast('error', '错误', '创建执行失败')
  } finally {
    loading.value = false
  }
}

const runExecution = async (id) => {
  try {
    await executionAPI.run(id)
    await loadExecutions()
    showToast('success', '成功', '运行成功！')
  } catch (error) {
    console.error('运行执行失败:', error)
    showToast('error', '错误', '运行执行失败')
  }
}

const deleteExecution = async (id) => {
  showConfirm('确定要删除这个执行吗？此操作无法撤销。', async () => {
    try {
      await executionAPI.delete(id)
      await loadExecutions()
      showToast('success', '成功', '删除成功！')
    } catch (error) {
      console.error('删除执行失败:', error)
      showToast('error', '错误', '删除执行失败')
    }
  })
}

const showToast = (type, title, message) => {
  toast.value = { show: true, type, title, message }
  setTimeout(() => {
    hideToast()
  }, 3000)
}

const hideToast = () => {
  toast.value.show = false
}

const showConfirm = (message, onConfirm) => {
  confirmDialog.value = { show: true, message, onConfirm }
}

const cancelConfirm = () => {
  confirmDialog.value.show = false
}

const confirmAction = () => {
  if (confirmDialog.value.onConfirm) {
    confirmDialog.value.onConfirm()
  }
  confirmDialog.value.show = false
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatResult = (result) => {
  try {
    return JSON.stringify(JSON.parse(result), null, 2)
  } catch {
    return result
  }
}

const hasUpdatedTime = (execution) => {
  if (!execution.updated_at) return false
  
  const createdTime = new Date(execution.created_at).getTime()
  const updatedTime = new Date(execution.updated_at).getTime()
  
  return updatedTime > createdTime
}

const getStatusText = (status) => {
  return statusMap[status]?.text || status
}

const getStatusClass = (status) => {
  const classMap = {
    '等待中': 'pending',
    '执行中': 'running',
    '已完成': 'completed',
    '失败': 'failed',
    '已取消': 'cancelled'
  }
  return classMap[status] || status
}

const editExecution = (execution) => {
  selectedExecution.value = execution
  editForm.value = {
    id: execution.id,
    name: execution.name,
    type: execution.type,
    status: execution.status,
    result: execution.result
  }
  showEditModal.value = true
}

const updateExecution = async () => {
  if (!editForm.value.name.trim()) {
    showToast('warning', '提示', '请输入执行名称')
    return
  }
  
  if (!editForm.value.result.trim()) {
    showToast('warning', '提示', '请输入执行结果')
    return
  }
  
  loading.value = true
  try {
    await executionAPI.update(editForm.value.id, {
      name: editForm.value.name,
      type: editForm.value.type,
      status: editForm.value.status,
      result: editForm.value.result
    })
    showEditModal.value = false
    await loadExecutions()
    showToast('success', '成功', '修改成功！')
  } catch (error) {
    console.error('修改执行失败:', error)
    showToast('error', '错误', '修改执行失败')
  } finally {
    loading.value = false
  }
}

const showPassRate = async (execution) => {
  selectedExecutionData.value = execution
  showPassRateModal.value = true
  
  await nextTick()
  
  if (chartInstance) {
    chartInstance.destroy()
  }
  
  const ctx = passRateChart.value.getContext('2d')
  const passedCases = execution.passed_cases || 0
  const failedCases = execution.failed_cases || 0
  const totalCases = execution.total_cases || 0
  const otherCases = totalCases - passedCases - failedCases
  
  const data = {
    labels: ['通过用例', '失败用例'],
    datasets: [{
      data: [passedCases, failedCases],
      backgroundColor: [
        'rgba(16, 185, 129, 0.8)',
        'rgba(239, 68, 68, 0.8)'
      ],
      borderColor: [
        'rgba(16, 185, 129, 1)',
        'rgba(239, 68, 68, 1)'
      ],
      borderWidth: 2
    }]
  }
  
  chartInstance = new Chart(ctx, {
    type: 'pie',
    data: data,
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            padding: 20,
            font: {
              size: 14,
              weight: 'bold'
            }
          }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const label = context.label || ''
              const value = context.parsed || 0
              const total = context.dataset.data.reduce((a, b) => a + b, 0)
              const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0
              return `${label}: ${value} (${percentage}%)`
            }
          }
        }
      }
    }
  })
}
</script>

<style scoped>
.executions-page {
  min-height: 100%;
  background: #f8fafc;
  padding: 24px;
}

.page-content {
  background: white;
  border-radius: 2rem;
  padding: 0;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.page-header {
  position: relative;
  padding: var(--space-xl);
  background: linear-gradient(145deg, var(--ink-primary) 0%, var(--ink-deep) 100%);
  overflow: hidden;
}

.header-decoration {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}

.deco-blob {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
}

.deco-blob-1 {
  width: 200px;
  height: 200px;
  top: -50%;
  right: -5%;
  background: 
    radial-gradient(circle at 50% 50%, rgba(34, 197, 94, 0.25) 0%, rgba(34, 197, 94, 0.15) 30%, rgba(34, 197, 94, 0.08) 50%, transparent 70%);
}

.deco-blob-2 {
  width: 150px;
  height: 150px;
  bottom: -40%;
  left: 10%;
  background: 
    radial-gradient(circle at 50% 50%, rgba(134, 239, 172, 0.2) 0%, rgba(134, 239, 172, 0.12) 30%, rgba(134, 239, 172, 0.06) 50%, transparent 70%);
}

.title-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 1.75rem;
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.25), rgba(134, 239, 172, 0.15));
  color: var(--forest-soft);
  border: 1px solid rgba(34, 197, 94, 0.3);
  margin-bottom: var(--space-sm);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  z-index: 1;
}

.title-section {
  color: white;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  margin: 0 0 8px 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.title-icon {
  font-size: 2.5rem;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.page-subtitle {
  font-size: 1rem;
  opacity: 0.9;
  margin: 0;
}

.btn-create {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
  padding: 12px 24px;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  backdrop-filter: blur(10px);
  transition: all 0.3s;
}

.btn-create:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.btn-icon {
  font-size: 1.2rem;
  font-weight: bold;
}

.filters-section {
  background: white;
  padding: 24px;
  border-radius: 16px;
  margin-bottom: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.filters-container {
  display: flex;
  gap: 24px;
  align-items: flex-end;
}

.filter-group {
  flex: 1;
  max-width: 300px;
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  color: #374151;
  font-size: 0.9rem;
}

.filter-label-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
  gap: 12px;
}

.filter-icon {
  font-size: 1.1rem;
}

.filter-select {
  width: 100%;
  padding: 10px 14px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 0.95rem;
  background: white;
  cursor: pointer;
  transition: all 0.3s;
}

.filter-select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
}

.project-search-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
}

.project-search-input {
  flex: 1;
  padding: 6px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 0.85rem;
  transition: all 0.3s;
}

.project-search-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.project-search-btn {
  padding: 6px 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  white-space: nowrap;
}

.project-search-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.filter-stats {
  margin-left: auto;
}

.stat-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: linear-gradient(135deg, #f3f4f6, #e5e7eb);
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
  color: #374151;
}

.stat-dot {
  width: 8px;
  height: 8px;
  background: #667eea;
  border-radius: 50%;
  animation: pulse-dot 2s ease-in-out infinite;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.executions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 24px;
  padding: 0 24px 24px;
}

.execution-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid #e2e8f0;
  position: relative;
}

.execution-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(102, 126, 234, 0.15);
  border-color: #667eea;
}

.card-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #667eea, #764ba2);
  opacity: 0;
  transition: opacity 0.3s;
}

.execution-card:hover .card-glow {
  opacity: 1;
}

.card-header {
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #f9fafb, #f3f4f6);
  border-bottom: 1px solid #e5e7eb;
}

.execution-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.icon-ring {
  position: absolute;
  inset: -3px;
  border: 3px solid rgba(102, 126, 234, 0.3);
  border-radius: 14px;
  animation: rotate 3s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.icon-emoji {
  font-size: 1.6rem;
  position: relative;
  z-index: 1;
}

.execution-status {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.execution-status.pending {
  background: #fef3c7;
  color: #92400e;
}

.execution-status.running {
  background: #dbeafe;
  color: #1e40af;
}

.execution-status.completed {
  background: #d1fae5;
  color: #065f46;
}

.execution-status.failed {
  background: #fee2e2;
  color: #991b1b;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
  animation: pulse-dot-2 2s ease-in-out infinite;
}

@keyframes pulse-dot-2 {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(1.2); }
}

.card-body {
  padding: 20px;
}

.execution-title {
  font-size: 1.15rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 16px 0;
}

.execution-meta {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 16px;
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.meta-icon {
  font-size: 0.9rem;
}

.meta-label {
  font-size: 0.75rem;
  color: #9ca3af;
}

.meta-value {
  font-size: 0.9rem;
  font-weight: 500;
  color: #374151;
}

.type-badge {
  display: inline-block;
  padding: 4px 8px;
  background: #e0e7ff;
  color: #4338ca;
  border-radius: 6px;
  text-align: center;
}

.execution-time {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: #f9fafb;
  border-radius: 10px;
  font-size: 0.85rem;
  color: #6b7280;
  margin-bottom: 16px;
}

.time-icon {
  color: #667eea;
  flex-shrink: 0;
}

.time-label {
  font-weight: 500;
  color: #374151;
}

.execution-result {
  margin-top: 16px;
}

.result-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 500;
  color: #6b7280;
  font-size: 0.85rem;
  margin-bottom: 8px;
}

.label-icon {
  font-size: 1rem;
}

.result-content {
  margin: 0;
  padding: 12px;
  background: #f3f4f6;
  border-radius: 8px;
  font-size: 0.8rem;
  color: #374151;
  font-family: 'Courier New', monospace;
  max-height: 150px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.card-footer {
  padding: 16px 20px;
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 8px;
}

.btn-run,
.btn-view,
.btn-pass-rate,
.btn-delete {
  flex: 1;
  padding: 10px 16px;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: all 0.3s;
}

.btn-run {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
}

.btn-run:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.3);
}

.btn-view {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
}

.btn-view:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.3);
}

.view-icon {
  font-size: 1rem;
}

.run-icon {
  font-size: 1rem;
}

.btn-delete {
  background: #fee2e2;
  color: #dc2626;
}

.btn-delete:hover {
  background: #dc2626;
  color: white;
}

.btn-pass-rate {
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
  color: white;
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.2);
}

.btn-pass-rate:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.3);
}

.pass-rate-icon {
  font-size: 1rem;
}

.delete-icon {
  font-size: 1rem;
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: #6b7280;
}

.empty-icon {
  font-size: 5rem;
  margin-bottom: 24px;
  opacity: 0.5;
}

.empty-state h3 {
  font-size: 1.5rem;
  color: #374151;
  margin: 0 0 8px 0;
}

.empty-state p {
  margin: 0 0 24px 0;
  color: #9ca3af;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 32px;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  z-index: 1000;
  padding: 90px 20px 20px;
  overflow-y: auto;
}

.modal-container {
  background: white;
  border-radius: 20px;
  width: 100%;
  max-width: 500px;
  max-height: calc(100vh - 140px);
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.2);
  animation: slideDown 0.3s ease-out;
  overflow-y: auto;
  margin-top: 20px;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  padding: 24px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.modal-icon {
  font-size: 1.5rem;
}

.modal-title h2 {
  margin: 0;
  font-size: 1.25rem;
  color: #1f2937;
}

.btn-close {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: none;
  background: #f3f4f6;
  color: #6b7280;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-close:hover {
  background: #e5e7eb;
  color: #374151;
}

.modal-body {
  padding: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-weight: 500;
  color: #374151;
  font-size: 0.95rem;
}

.required-mark {
  color: #ef4444;
  font-weight: 700;
  margin-left: 2px;
}

.label-icon {
  font-size: 1.1rem;
}

.form-input,
.form-textarea,
.form-select {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 1rem;
  font-family: inherit;
  transition: all 0.3s;
  background: white;
}

.form-input:focus,
.form-textarea:focus,
.form-select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
}

.type-selector {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.type-option {
  padding: 16px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  background: white;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.type-option .type-icon {
  font-size: 2rem;
}

.type-option .type-label {
  font-size: 0.9rem;
  font-weight: 500;
  color: #6b7280;
}

.type-option.active {
  border-color: #667eea;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05));
}

.type-option.active .type-label {
  color: #667eea;
}

.modal-footer {
  padding: 24px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.btn-cancel,
.btn-submit {
  padding: 12px 24px;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
}

.btn-cancel {
  background: #f3f4f6;
  color: #6b7280;
}

.btn-cancel:hover {
  background: #e5e7eb;
  color: #374151;
}

.btn-submit {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.btn-submit:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.btn-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .page-header {
    padding: 24px;
    margin: -16px -16px 24px -16px;
  }

  .header-content {
    flex-direction: column;
    gap: 16px;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .filters-container {
    flex-direction: column;
    gap: 16px;
  }

  .filter-group {
    max-width: 100%;
  }

  .filter-stats {
    width: 100%;
  }

  .executions-grid {
    grid-template-columns: 1fr;
    padding: 0 16px 16px;
  }

  .type-selector {
    grid-template-columns: 1fr;
  }
}

.detail-modal {
  max-width: 600px;
}

.detail-section {
  margin-bottom: 24px;
}

.detail-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 16px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-item.full-width {
  grid-column: 1 / -1;
}

.detail-label {
  font-size: 0.85rem;
  color: #9ca3af;
  font-weight: 500;
}

.detail-value {
  font-size: 1rem;
  color: #1f2937;
  font-weight: 600;
}

.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.85rem;
}

.status-badge.pending {
  background: #fef3c7;
  color: #92400e;
}

.status-badge.running {
  background: #dbeafe;
  color: #1e40af;
}

.status-badge.completed {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.failed {
  background: #fee2e2;
  color: #991b1b;
}

.result-section {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
}

.result-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 16px 0;
}

.result-icon {
  font-size: 1.2rem;
}

.result-stats {
  background: #f9fafb;
  border-radius: 12px;
  padding: 20px;
}

.result-stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}

.stat-card {
  background: white;
  border-radius: 10px;
  padding: 16px;
  text-align: center;
  border: 2px solid #e5e7eb;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-card.passed {
  border-color: #10b981;
  background: #d1fae5;
}

.stat-card.failed {
  border-color: #ef4444;
  background: #fee2e2;
}

.stat-card.skipped {
  border-color: #f59e0b;
  background: #fef3c7;
}

.stat-number {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 4px;
}

.stat-card.passed .stat-number {
  color: #065f46;
}

.stat-card.failed .stat-number {
  color: #991b1b;
}

.stat-card.skipped .stat-number {
  color: #92400e;
}

.stat-label {
  font-size: 0.85rem;
  color: #6b7280;
  font-weight: 500;
}

.pass-rate-section {
  display: flex;
  align-items: center;
  gap: 16px;
}

.pass-rate-label {
  font-size: 0.9rem;
  color: #6b7280;
  font-weight: 500;
  min-width: 60px;
}

.pass-rate-bar {
  flex: 1;
  height: 12px;
  background: #e5e7eb;
  border-radius: 6px;
  overflow: hidden;
}

.pass-rate-fill {
  height: 100%;
  background: linear-gradient(90deg, #10b981, #059669);
  border-radius: 6px;
  transition: width 0.5s ease;
}

.pass-rate-text {
  font-size: 1rem;
  font-weight: 600;
  color: #10b981;
  min-width: 50px;
  text-align: right;
}

.no-result {
  text-align: center;
  padding: 40px 20px;
  color: #9ca3af;
}

.no-result-icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 12px;
  opacity: 0.5;
}

.no-result p {
  margin: 0;
  font-size: 0.95rem;
}

@media (max-width: 768px) {
  .detail-row {
    grid-template-columns: 1fr;
  }

  .result-stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .pass-rate-section {
    flex-direction: column;
    align-items: stretch;
  }

  .pass-rate-label {
    text-align: center;
  }

  .pass-rate-text {
    text-align: center;
  }
}

.toast-overlay {
  position: fixed;
  inset: 0;
  background: rgba(10, 15, 26, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.toast-container {
  background: white;
  border-radius: 16px;
  padding: 20px 24px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  gap: 16px;
  max-width: 400px;
  animation: scale-bounce 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  border: 1px solid rgba(232, 93, 4, 0.08);
}

@keyframes scale-bounce {
  0% {
    opacity: 0;
    transform: scale(0.8);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

.toast-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.toast-icon.success {
  background: linear-gradient(135deg, #10b981, #059669);
  box-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
}

.toast-icon.error {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  box-shadow: 0 0 20px rgba(239, 68, 68, 0.3);
}

.toast-icon.warning {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  box-shadow: 0 0 20px rgba(245, 158, 11, 0.3);
}

.toast-content {
  flex: 1;
}

.toast-title {
  margin: 0 0 4px 0;
  font-size: 1rem;
  font-weight: 700;
  color: #1f2937;
}

.toast-message {
  margin: 0;
  font-size: 0.875rem;
  color: #6b7280;
}

.toast-close {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: none;
  background: transparent;
  color: #6b7280;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
}

.toast-close:hover {
  background: rgba(232, 93, 4, 0.06);
  color: #e85d04;
}

.confirm-overlay {
  position: fixed;
  inset: 0;
  background: rgba(10, 15, 26, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.confirm-container {
  background: white;
  border-radius: 20px;
  padding: 32px;
  min-width: 360px;
  max-width: 90vw;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  text-align: center;
  animation: scale-bounce 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  border: 1px solid rgba(232, 93, 4, 0.08);
}

.confirm-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 20px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.1), rgba(217, 119, 6, 0.08));
  display: flex;
  align-items: center;
  justify-content: center;
  color: #f59e0b;
}

.confirm-title {
  margin: 0 0 8px 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: #1f2937;
}

.confirm-message {
  margin: 0 0 32px 0;
  font-size: 0.9375rem;
  color: #6b7280;
  line-height: 1.6;
}

.confirm-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.confirm-btn {
  padding: 10px 24px;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
}

.confirm-btn.cancel {
  background: rgba(232, 93, 4, 0.04);
  color: #6b7280;
}

.confirm-btn.cancel:hover {
  background: rgba(232, 93, 4, 0.08);
  color: #1f2937;
}

.confirm-btn.delete {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2);
}

.confirm-btn.delete:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(239, 68, 68, 0.3);
}

.toast-enter-active,
.toast-leave-active {
  transition: opacity 0.3s;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
}

.confirm-enter-active,
.confirm-leave-active {
  transition: opacity 0.3s;
}

.confirm-enter-from,
.confirm-leave-to {
  opacity: 0;
}

.pass-rate-modal {
  max-width: 600px;
}

.pass-rate-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.chart-container {
  position: relative;
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
}

.stats-summary {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-top: 20px;
}

.summary-item {
  background: #f9fafb;
  border-radius: 12px;
  padding: 16px;
  text-align: center;
  border: 2px solid #e5e7eb;
  transition: all 0.3s;
}

.summary-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.summary-item.passed {
  border-color: #10b981;
  background: #d1fae5;
}

.summary-item.failed {
  border-color: #ef4444;
  background: #fee2e2;
}

.summary-item.rate {
  border-color: #8b5cf6;
  background: #ede9fe;
}

.summary-label {
  font-size: 0.85rem;
  color: #6b7280;
  font-weight: 500;
  margin-bottom: 8px;
}

.summary-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
}

.summary-item.passed .summary-value {
  color: #065f46;
}

.summary-item.failed .summary-value {
  color: #991b1b;
}

.summary-item.rate .summary-value {
  color: #6d28d9;
}

@media (max-width: 768px) {
  .stats-summary {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
