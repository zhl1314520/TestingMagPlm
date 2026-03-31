<template>
  <div class="bugs-page">
    <div class="page-content">
      <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <span class="title-icon">🐛</span>
            缺陷管理
          </h1>
          <p class="page-subtitle">跟踪和管理软件缺陷</p>
        </div>
        <button @click="showCreateModal = true" class="btn-create">
          <span class="btn-icon">+</span>
          创建缺陷
        </button>
      </div>
    </div>

    <div class="filters-section">
      <div class="filters-container">
        <div class="filter-group">
          <label class="filter-label">
            <span class="filter-icon">📁</span>
            项目
          </label>
          <select v-model="filters.project_id" @change="loadBugs" class="filter-select">
            <option value="">全部项目</option>
            <option v-for="project in projects" :key="project.id" :value="project.id">
              {{ project.name }}
            </option>
          </select>
        </div>

        <div class="filter-group">
          <label class="filter-label">
            <span class="filter-icon">✅</span>
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
            <span class="filter-icon">🔥</span>
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
      <div class="empty-icon">🔍</div>
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
              <span class="meta-icon">📁</span>
              <span class="meta-label">项目</span>
              <span class="meta-value">#{{ bug.project_id }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-icon">🔥</span>
              <span class="meta-label">优先级</span>
              <span class="priority-badge" :class="bug.priority">{{ getPriorityText(bug.priority) }}</span>
            </div>
          </div>

          <div class="bug-time">
            <span class="time-icon">📅</span>
            <span class="time-text">创建于 {{ formatDate(bug.created_at) }}</span>
          </div>
        </div>

        <div class="card-footer">
          <div class="bug-id">#{{ bug.id }}</div>
          <div class="action-buttons" @click.stop>
            <button @click="editBug(bug)" class="btn-edit" title="编辑">
              <span>✏️</span>
            </button>
            <button @click="deleteBug(bug.id)" class="btn-delete" title="删除">
              <span>🗑</span>
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
              <span class="modal-icon">{{ editingBug ? '✏️' : '🐛' }}</span>
              <h2>{{ editingBug ? '编辑缺陷' : '报告新缺陷' }}</h2>
            </div>
            <button @click="closeModal" class="btn-close">×</button>
          </div>

          <form @submit.prevent="saveBug" class="modal-body">
            <div class="form-group">
              <label class="form-label">
                <span class="label-icon">📁</span>
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
                <span class="label-icon">📝</span>
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
                <span class="label-icon">📄</span>
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
                  <span class="label-icon">✅</span>
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
                  <span class="label-icon">🔥</span>
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
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { bugAPI, projectAPI } from '../api/index.js'

const bugs = ref([])
const projects = ref([])
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
  assignee_id: null
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

onMounted(async () => {
  await loadProjects()
  await loadBugs()
})

const loadProjects = async () => {
  try {
    const response = await projectAPI.getList()
    projects.value = response.data.items
  } catch (error) {
    console.error('加载项目列表失败:', error)
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

const saveBug = async () => {
  loading.value = true
  try {
    if (editingBug.value) {
      await bugAPI.update(editingBug.value.id, bugForm.value)
    } else {
      await bugAPI.create(bugForm.value)
    }
    closeModal()
    await loadBugs()
  } catch (error) {
    console.error('保存缺陷失败:', error)
    alert('保存缺陷失败')
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
  if (!confirm('确定要删除这个缺陷吗？')) return

  try {
    await bugAPI.delete(id)
    await loadBugs()
  } catch (error) {
    console.error('删除缺陷失败:', error)
    alert('删除缺陷失败')
  }
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
    assignee_id: null
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  margin: -24px -24px 32px -24px;
  padding: 32px;
  position: relative;
  overflow: hidden;
  border-radius: 2rem 2rem 0 0;
}

.page-header::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -10%;
  width: 300px;
  height: 300px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(5deg); }
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
  margin-bottom: 8px;
  font-weight: 500;
  color: #374151;
  font-size: 0.9rem;
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
}

.time-icon {
  font-size: 1rem;
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
</style>
