<template>
  <div class="bugs-page">
    <div class="page-content">
      <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <div class="title-badge">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="12"/>
              <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
            Bug Tracker
          </div>
          <h1 class="page-title">缺陷管理</h1>
          <p class="page-subtitle">跟踪和管理软件缺陷</p>
        </div>
        <button @click="showCreateModal = true" class="btn-create">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          创建缺陷
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
              <Icon class="filter-icon" icon="carbon:folder" />
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
          <select v-model="filters.project_id" @change="loadBugs" class="filter-select">
            <option value="">全部项目</option>
            <option v-for="project in filteredProjects" :key="project.id" :value="project.id">
              {{ project.name }}
            </option>
          </select>
        </div>

        <div class="filter-group">
          <label class="filter-label">
            <Icon class="filter-icon" icon="carbon:checkmark" />
            状态
          </label>
          <select v-model="filters.status" @change="loadBugs" class="filter-select">
            <option value="">全部状态</option>
            <option value="new">新建</option>
            <option value="in_progress">处理中</option>
            <option value="resolved">已解决</option>
            <option value="closed">已关闭</option>
            <option value="deferred">延期</option>
          </select>
        </div>

        <div class="filter-group">
          <label class="filter-label">
            <Icon class="filter-icon" icon="carbon:fire" />
            优先级
          </label>
          <select v-model="filters.priority" @change="loadBugs" class="filter-select">
            <option value="">全部优先级</option>
            <option value="critical">严重</option>
            <option value="high">高</option>
            <option value="medium">中</option>
            <option value="low">低</option>
          </select>
        </div>

        <div class="filter-stats">
          <div class="stat-badge">
            <span class="stat-dot"></span>
            <span class="stat-text">共 {{ bugs.length }} 个缺陷</span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="bugs.length === 0" class="empty-state">
      <div class="empty-icon">
        <Icon icon="carbon:search" width="80" height="80" />
      </div>
      <h3>暂无缺陷</h3>
      <p>太棒了！目前没有发现任何缺陷</p>
      <button @click="showCreateModal = true" class="btn-primary">报告缺陷</button>
    </div>

    <div v-else class="bugs-grid">
      <div v-for="bug in bugs" :key="bug.id" class="bug-card">
        <div class="card-glow"></div>
        <div class="card-header">
          <div class="priority-indicator" :class="bug.priority"></div>
          <div class="status-badge" :class="bug.status">
            <span class="status-dot"></span>
            {{ getStatusText(bug.status) }}
          </div>
        </div>

        <div class="card-body">
          <h3 class="bug-title">{{ bug.title }}</h3>
          <p class="bug-description">{{ bug.description }}</p>

          <div class="bug-meta">
            <div class="meta-item">
              <Icon class="meta-icon" icon="carbon:folder" />
              <span class="meta-label">项目</span>
              <span class="meta-value project-name">项目：{{ bug.project_name || '未知项目' }}</span>
            </div>
            <div class="meta-item">
              <Icon class="meta-icon" icon="carbon:fire" />
              <span class="meta-label">优先级</span>
              <span class="priority-badge" :class="bug.priority">{{ getPriorityText(bug.priority) }}</span>
            </div>
            <div v-if="bug.testcase_id" class="meta-item">
              <Icon class="meta-icon" icon="carbon:list-checked" />
              <span class="meta-label">测试用例</span>
              <span class="meta-value">#{{ bug.testcase_id }}</span>
            </div>
            <div v-if="bug.reporter_name" class="meta-item">
              <Icon class="meta-icon" icon="carbon:user" />
              <span class="meta-label">报告者</span>
              <span class="meta-value">{{ bug.reporter_name }}</span>
            </div>
            <div v-if="bug.assignee_name" class="meta-item">
              <Icon class="meta-icon" icon="carbon:tools" />
              <span class="meta-label">指派给</span>
              <span class="meta-value">{{ bug.assignee_name }}</span>
            </div>
          </div>

          <div class="bug-time">
            <svg class="time-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
              <line x1="16" y1="2" x2="16" y2="6"/>
              <line x1="8" y1="2" x2="8" y2="6"/>
              <line x1="3" y1="10" x2="21" y2="10"/>
            </svg>
            <span class="time-label">创建时间：</span>
            <span class="time-text">{{ formatDate(bug.created_at) }}</span>
          </div>

          <div v-if="bug.updated_at && hasUpdatedTime(bug)" class="bug-time">
            <svg class="time-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"/>
              <polyline points="12 6 12 12 16 14"/>
            </svg>
            <span class="time-label">更新时间：</span>
            <span class="time-text">{{ formatDate(bug.updated_at) }}</span>
          </div>
        </div>

        <div class="card-footer">
          <div class="bug-id">#{{ bug.id }}</div>
          <div class="action-buttons" @click.stop>
            <button @click="editBug(bug)" class="btn-edit" title="编辑">
              <Icon icon="carbon:edit" width="16" height="16" />
            </button>
            <button @click="deleteBug(bug.id)" class="btn-delete" title="删除">
              <Icon icon="carbon:trash-can" width="16" height="16" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <Transition name="modal">
      <div v-if="showCreateModal" class="modal-overlay" @click="closeModal">
        <div class="modal-container" @click.stop>
          <div class="modal-header">
            <div class="modal-title">
              <Icon class="modal-icon" :icon="editingBug ? 'carbon:edit' : 'carbon:bug'" />
              <h2>{{ editingBug ? '编辑缺陷' : '报告新缺陷' }}</h2>
            </div>
            <button @click="closeModal" class="btn-close">×</button>
          </div>

          <form @submit.prevent="saveBug" class="modal-body">
            <div class="form-group">
              <label class="form-label">
                <Icon class="label-icon" icon="carbon:folder" />
                所属项目
              </label>
              <select v-model="bugForm.project_id" required class="form-select">
                <option value="">选择项目</option>
                <option v-for="project in projects" :key="project.id" :value="project.id">
                  {{ project.name }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">
                <Icon class="label-icon" icon="carbon:text-creation" />
                缺陷标题
              </label>
              <input
                v-model="bugForm.title"
                type="text"
                required
                placeholder="简明扼要地描述缺陷"
                class="form-input"
              />
            </div>

            <div class="form-group">
              <label class="form-label">
                <Icon class="label-icon" icon="carbon:document" />
                详细描述
              </label>
              <textarea
                v-model="bugForm.description"
                rows="4"
                required
                placeholder="详细描述缺陷现象、复现步骤等"
                class="form-textarea"
              ></textarea>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label class="form-label">
                  <Icon class="label-icon" icon="carbon:checkmark" />
                  状态
                </label>
                <select v-model="bugForm.status" class="form-select">
                  <option value="new">新建</option>
                  <option value="in_progress">处理中</option>
                  <option value="resolved">已解决</option>
                  <option value="closed">已关闭</option>
                  <option value="deferred">延期</option>
                </select>
              </div>

              <div class="form-group">
                <label class="form-label">
                  <Icon class="label-icon" icon="carbon:fire" />
                  优先级
                </label>
                <div class="priority-selector">
                  <button
                    type="button"
                    v-for="priority in priorityOptions"
                    :key="priority.value"
                    @click="bugForm.priority = priority.value"
                    :class="['priority-option', priority.value, { active: bugForm.priority === priority.value }]"
                  >
                    {{ priority.label }}
                  </button>
                </div>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label class="form-label">
                  <Icon class="label-icon" icon="carbon:tools" />
                  指派给
                </label>
                <select v-model="bugForm.assignee_id" class="form-select">
                  <option :value="null">未指派</option>
                  <option v-for="user in users" :key="user.id" :value="user.id">
                    {{ user.username }} ({{ user.role }})
                  </option>
                </select>
              </div>

              <div class="form-group">
                <label class="form-label">
                  <Icon class="label-icon" icon="carbon:list-checked" />
                  关联测试用例
                </label>
                <select v-model="bugForm.testcase_id" class="form-select">
                  <option :value="null">无关联</option>
                  <option v-for="testcase in testcases" :key="testcase.id" :value="testcase.id">
                    #{{ testcase.id }} - {{ testcase.title }}
                  </option>
                </select>
              </div>
            </div>
          </form>

          <div class="modal-footer">
            <button @click="closeModal" class="btn-cancel">取消</button>
            <button @click="saveBug" class="btn-submit">
              <span class="btn-spinner" v-if="loading"></span>
              <span v-else>{{ editingBug ? '保存修改' : '提交缺陷' }}</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <Transition name="toast">
      <div v-if="toast.show" class="toast-overlay" @click="hideToast">
        <div class="toast-container" @click.stop>
          <div class="toast-icon" :class="toast.type">
            <span v-if="toast.type === 'success'">✓</span>
            <span v-else-if="toast.type === 'error'">✕</span>
            <span v-else>!</span>
          </div>
          <div class="toast-content">
            <h3 class="toast-title">{{ toast.title }}</h3>
            <p class="toast-message">{{ toast.message }}</p>
          </div>
          <button @click="hideToast" class="toast-close">×</button>
        </div>
      </div>
    </Transition>

    <Transition name="confirm">
      <div v-if="confirmDialog.show" class="confirm-overlay" @click="cancelConfirm">
        <div class="confirm-container" @click.stop>
          <div class="confirm-icon">
            <Icon icon="carbon:warning" width="32" height="32" />
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
import { ref, onMounted, computed } from 'vue'
import { Icon } from '@iconify/vue'
import { bugAPI, projectAPI, userAPI, testcaseAPI } from '../api/index.js'

const bugs = ref([])
const projects = ref([])
const users = ref([])
const testcases = ref([])
const projectSearchKeyword = ref('')
const showCreateModal = ref(false)
const editingBug = ref(null)
const loading = ref(false)

const filters = ref({
  project_id: '',
  status: '',
  priority: ''
})

const bugForm = ref({
  project_id: '',
  title: '',
  description: '',
  status: 'new',
  priority: 'medium',
  assignee_id: null,
  testcase_id: null
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

const priorityOptions = [
  { value: 'critical', label: '严重' },
  { value: 'high', label: '高' },
  { value: 'medium', label: '中' },
  { value: 'low', label: '低' }
]

const statusMap = {
  new: '新建',
  in_progress: '处理中',
  resolved: '已解决',
  closed: '已关闭',
  deferred: '延期'
}

const priorityMap = {
  critical: '严重',
  high: '高',
  medium: '中',
  low: '低'
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
  await loadUsers()
  await loadTestCases()
  await loadBugs()
})

const loadProjects = async () => {
  try {
    const response = await projectAPI.getList(1, 100)
    projects.value = response.data.items
  } catch (error) {
    console.error('加载项目列表失败:', error)
  }
}

const loadUsers = async () => {
  try {
    const response = await userAPI.getList(1, 100)
    users.value = response.data.items
  } catch (error) {
    console.error('加载用户列表失败:', error)
  }
}

const loadTestCases = async () => {
  try {
    const response = await testcaseAPI.getList(1, 100)
    testcases.value = response.data.items
  } catch (error) {
    console.error('加载测试用例列表失败:', error)
  }
}

const loadBugs = async () => {
  try {
    const response = await bugAPI.getList(
      1,
      100,
      filters.value.project_id || null,
      filters.value.status || null,
      filters.value.priority || null
    )
    bugs.value = response.data.items
  } catch (error) {
    console.error('加载缺陷列表失败:', error)
  }
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

const validateForm = () => {
  if (!bugForm.value.project_id) {
    showToast('warning', '提示', '请选择所属项目！')
    return false
  }
  if (!bugForm.value.title || !bugForm.value.title.trim()) {
    showToast('warning', '提示', '缺陷标题为必填项！')
    return false
  }
  if (!bugForm.value.description || !bugForm.value.description.trim()) {
    showToast('warning', '提示', '详细描述为必填项！')
    return false
  }
  return true
}

const saveBug = async () => {
  if (!validateForm()) return
  
  loading.value = true
  try {
    const dataToSend = {
      ...bugForm.value,
      project_id: parseInt(bugForm.value.project_id)
    }
    if (editingBug.value) {
      await bugAPI.update(editingBug.value.id, dataToSend)
      showToast('success', '成功', '缺陷修改成功！')
    } else {
      await bugAPI.create(dataToSend)
      showToast('success', '成功', '缺陷创建成功！')
    }
    closeModal()
    await loadBugs()
  } catch (error) {
    console.error('保存缺陷失败:', error)
    const errorMsg = error.response?.data?.detail || '保存缺陷失败'
    showToast('error', '错误', errorMsg)
  } finally {
    loading.value = false
  }
}

const editBug = (bug) => {
  editingBug.value = bug
  bugForm.value = { ...bug }
  showCreateModal.value = true
}

const deleteBug = async (id) => {
  showConfirm('确定要删除这个缺陷吗？此操作不可恢复。', async () => {
    try {
      await bugAPI.delete(id)
      await loadBugs()
      showToast('success', '成功', '删除成功！')
    } catch (error) {
      console.error('删除缺陷失败:', error)
      showToast('error', '错误', '删除缺陷失败')
    }
  })
}

const closeModal = () => {
  showCreateModal.value = false
  editingBug.value = null
  bugForm.value = {
    project_id: '',
    title: '',
    description: '',
    status: 'new',
    priority: 'medium',
    assignee_id: null,
    testcase_id: null
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const hasUpdatedTime = (bug) => {
  if (!bug.updated_at) return false
  
  const createdTime = new Date(bug.created_at).getTime()
  const updatedTime = new Date(bug.updated_at).getTime()
  
  return updatedTime > createdTime
}

const getStatusText = (status) => {
  return statusMap[status] || status
}

const getPriorityText = (priority) => {
  return priorityMap[priority] || priority
}
</script>

<style scoped>
.bugs-page {
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
    radial-gradient(circle at 50% 50%, rgba(244, 63, 94, 0.25) 0%, rgba(244, 63, 94, 0.15) 30%, rgba(244, 63, 94, 0.08) 50%, transparent 70%);
}

.deco-blob-2 {
  width: 150px;
  height: 150px;
  bottom: -40%;
  left: 10%;
  background: 
    radial-gradient(circle at 50% 50%, rgba(253, 164, 175, 0.2) 0%, rgba(253, 164, 175, 0.12) 30%, rgba(253, 164, 175, 0.06) 50%, transparent 70%);
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
  background: linear-gradient(135deg, rgba(244, 63, 94, 0.25), rgba(253, 164, 175, 0.15));
  color: var(--coral-soft);
  border: 1px solid rgba(244, 63, 94, 0.3);
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
  flex-wrap: wrap;
}

.filter-group {
  flex: 1;
  min-width: 180px;
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
  width: 1.1rem;
  height: 1.1rem;
  color: #374151;
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

.bugs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
  padding: 0 24px 24px;
}

.bug-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid #e2e8f0;
  position: relative;
}

.bug-card:hover {
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

.bug-card:hover .card-glow {
  opacity: 1;
}

.card-header {
  padding: 16px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #f9fafb, #f3f4f6);
  border-bottom: 1px solid #e5e7eb;
}

.priority-indicator {
  width: 4px;
  height: 32px;
  border-radius: 2px;
}

.priority-indicator.critical {
  background: linear-gradient(180deg, #dc2626, #991b1b);
}

.priority-indicator.high {
  background: linear-gradient(180deg, #f97316, #c2410c);
}

.priority-indicator.medium {
  background: linear-gradient(180deg, #f59e0b, #92400e);
}

.priority-indicator.low {
  background: linear-gradient(180deg, #10b981, #059669);
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.status-badge.new {
  background: #fef3c7;
  color: #92400e;
}

.status-badge.in_progress {
  background: #dbeafe;
  color: #1e40af;
}

.status-badge.resolved {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.closed {
  background: #e5e7eb;
  color: #374151;
}

.status-badge.deferred {
  background: #f3e8ff;
  color: #6b21a8;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}

.card-body {
  padding: 20px;
}

.bug-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 8px 0;
}

.bug-description {
  color: #6b7280;
  font-size: 0.9rem;
  line-height: 1.6;
  margin: 0 0 16px 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.bug-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.meta-icon {
  width: 0.9rem;
  height: 0.9rem;
  color: #6b7280;
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

.priority-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
}

.priority-badge.critical {
  background: #fee2e2;
  color: #991b1b;
}

.priority-badge.high {
  background: #fed7aa;
  color: #9a3412;
}

.priority-badge.medium {
  background: #fef3c7;
  color: #92400e;
}

.priority-badge.low {
  background: #d1fae5;
  color: #065f46;
}

.bug-time {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: #f9fafb;
  border-radius: 10px;
  font-size: 0.85rem;
  color: #6b7280;
  margin-bottom: 12px;
}

.time-icon {
  color: #667eea;
  flex-shrink: 0;
}

.time-label {
  font-weight: 500;
  color: #374151;
}

.card-footer {
  padding: 16px 20px;
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.bug-id {
  font-size: 0.85rem;
  color: #9ca3af;
  font-weight: 500;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.btn-edit,
.btn-delete {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  transition: all 0.3s;
}

.btn-edit {
  background: #e0e7ff;
  color: #4338ca;
}

.btn-edit:hover {
  background: #4338ca;
  color: white;
  transform: scale(1.1);
}

.btn-delete {
  background: #fee2e2;
  color: #dc2626;
}

.btn-delete:hover {
  background: #dc2626;
  color: white;
  transform: scale(1.1);
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
  max-width: 600px;
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
  position: sticky;
  top: 0;
  background: white;
  z-index: 1;
}

.modal-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.modal-icon {
  width: 1.5rem;
  height: 1.5rem;
  color: #1f2937;
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

.form-row {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 16px;
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

.label-icon {
  width: 1.1rem;
  height: 1.1rem;
  color: #374151;
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

.form-textarea {
  resize: vertical;
}

.priority-selector {
  display: flex;
  gap: 6px;
}

.priority-option {
  flex: 1;
  padding: 8px 4px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  font-size: 0.8rem;
  font-weight: 600;
  color: #6b7280;
  transition: all 0.3s;
}

.priority-option.critical { border-color: #f87171; }
.priority-option.high { border-color: #fb923c; }
.priority-option.medium { border-color: #fbbf24; }
.priority-option.low { border-color: #34d399; }

.priority-option.active {
  color: white;
  transform: scale(1.05);
}

.priority-option.critical.active { background: #f87171; border-color: #f87171; }
.priority-option.high.active { background: #fb923c; border-color: #fb923c; }
.priority-option.medium.active { background: #fbbf24; border-color: #fbbf24; }
.priority-option.low.active { background: #34d399; border-color: #34d399; }

.modal-footer {
  padding: 24px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  position: sticky;
  bottom: 0;
  background: white;
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
    width: 100%;
  }

  .filter-stats {
    width: 100%;
  }

  .bugs-grid {
    grid-template-columns: 1fr;
    padding: 0 16px 16px;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .priority-selector {
    flex-wrap: wrap;
  }

  .priority-option {
    min-width: 60px;
  }
}

.toast-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.toast-container {
  background: #ffffff;
  border-radius: 16px;
  padding: 24px 32px;
  min-width: 320px;
  max-width: 90vw;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  gap: 20px;
  animation: toastBounce 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

@keyframes toastBounce {
  0% {
    opacity: 0;
    transform: scale(0.3);
  }
  50% {
    transform: scale(1.05);
  }
  70% {
    transform: scale(0.95);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

.toast-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  font-weight: 600;
  color: white;
  flex-shrink: 0;
}

.toast-icon.success {
  background: #10b981;
}

.toast-icon.error {
  background: #ef4444;
}

.toast-icon.warning {
  background: #f59e0b;
}

.toast-content {
  flex: 1;
}

.toast-title {
  margin: 0 0 4px 0;
  font-size: 1rem;
  font-weight: 600;
  color: #111827;
}

.toast-message {
  margin: 0;
  font-size: 0.875rem;
  color: #6b7280;
}

.toast-close {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  border: none;
  background: transparent;
  color: #9ca3af;
  font-size: 1.25rem;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.toast-close:hover {
  background: #f3f4f6;
  color: #374151;
}

.toast-enter-active {
  animation: fadeIn 0.3s ease;
}

.toast-leave-active {
  animation: fadeOut 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fadeOut {
  from { opacity: 1; }
  to { opacity: 0; }
}

.confirm-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.confirm-container {
  background: #ffffff;
  border-radius: 20px;
  padding: 32px;
  min-width: 360px;
  max-width: 90vw;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  animation: confirmBounce 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  text-align: center;
}

@keyframes confirmBounce {
  0% {
    opacity: 0;
    transform: scale(0.3);
  }
  50% {
    transform: scale(1.05);
  }
  70% {
    transform: scale(0.95);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

.confirm-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 20px;
  background: #fef3c7;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
}

.confirm-title {
  margin: 0 0 8px 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
}

.confirm-message {
  margin: 0 0 24px 0;
  font-size: 0.9375rem;
  color: #6b7280;
  line-height: 1.5;
}

.confirm-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.confirm-btn {
  padding: 10px 24px;
  border-radius: 10px;
  font-size: 0.9375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.confirm-btn.cancel {
  background: #f3f4f6;
  color: #374151;
}

.confirm-btn.cancel:hover {
  background: #e5e7eb;
}

.confirm-btn.delete {
  background: #ef4444;
  color: white;
}

.confirm-btn.delete:hover {
  background: #dc2626;
}

.confirm-enter-active {
  animation: fadeIn 0.3s ease;
}

.confirm-leave-active {
  animation: fadeOut 0.2s ease;
}
</style>
