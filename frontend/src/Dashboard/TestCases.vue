<template>
  <div class="testcases-page">
    <div class="page-content">
      <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <span class="title-icon">📝</span>
            测试用例管理
          </h1>
          <p class="page-subtitle">编写和管理高质量的测试用例</p>
        </div>
        <button @click="showCreateModal = true" class="btn-create">
          <span class="btn-icon">+</span>
          创建用例
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
          <select v-model="filters.project_id" @change="loadTestCases" class="filter-select">
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
          <select v-model="filters.status" @change="loadTestCases" class="filter-select">
            <option value="">全部状态</option>
            <option value="草稿">草稿</option>
            <option value="有效">有效</option>
            <option value="已弃用">已弃用</option>
            <option value="阻塞">阻塞</option>
          </select>
        </div>

        <div class="filter-stats">
          <div class="stat-badge">
            <span class="stat-dot"></span>
            <span class="stat-text">共 {{ testcases.length }} 条用例</span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="testcases.length === 0" class="empty-state">
      <div class="empty-icon">📋</div>
      <h3>暂无测试用例</h3>
      <p>创建第一个测试用例来开始测试</p>
      <button @click="showCreateModal = true" class="btn-primary">创建用例</button>
    </div>

    <div v-else class="testcase-list">
      <div v-for="testcase in testcases" :key="testcase.id" class="testcase-card">
        <div class="card-header">
          <div class="testcase-title">{{ testcase.title }}</div>
          <div class="status-badges">
            <span class="badge module-badge">
              🔖 {{ testcase.module }}
            </span>
            <span class="badge status-badge" :class="testcase.status">
              {{ getStatusText(testcase.status) }}
            </span>
          </div>
        </div>

        <div class="card-content">
          <div class="content-section">
            <div class="section-label">
              <span class="label-icon">👣</span>
              执行步骤
            </div>
            <p class="section-text">{{ testcase.steps }}</p>
          </div>

          <div class="content-section">
            <div class="section-label">
              <span class="label-icon">🎯</span>
              期望结果
            </div>
            <p class="section-text expected">{{ testcase.expected }}</p>
          </div>
        </div>

        <div class="card-footer">
          <div class="testcase-id">#{{ testcase.id }}</div>
          <div class="action-buttons">
            <button @click="editTestCase(testcase)" class="btn-edit" title="编辑">
              <span>✏️</span>
            </button>
            <button @click="deleteTestCase(testcase.id)" class="btn-delete" title="删除">
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
              <span class="modal-icon">{{ editingTestCase ? '✏️' : '✨' }}</span>
              <h2>{{ editingTestCase ? '编辑用例' : '创建新用例' }}</h2>
            </div>
            <button @click="closeModal" class="btn-close">×</button>
          </div>
          
          <form @submit.prevent="saveTestCase" class="modal-body">
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">
                  <span class="label-icon">📁</span>
                  所属项目
                </label>
                <select v-model="testCaseForm.project_id" required class="form-select">
                  <option value="">选择项目</option>
                  <option v-for="project in projects" :key="project.id" :value="project.id">
                    {{ project.name }}
                  </option>
                </select>
              </div>

              <div class="form-group">
                <label class="form-label">
                  <span class="label-icon">🔖</span>
                  模块
                </label>
                <input 
                  v-model="testCaseForm.module" 
                  type="text" 
                  required 
                  placeholder="例如：用户管理"
                  class="form-input"
                />
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">
                <span class="label-icon">📝</span>
                用例标题
              </label>
              <input 
                v-model="testCaseForm.title" 
                type="text" 
                required 
                placeholder="简明扼要地描述测试用例"
                class="form-input"
              />
            </div>

            <div class="form-group">
              <label class="form-label">
                <span class="label-icon">👣</span>
                执行步骤
              </label>
              <textarea 
                v-model="testCaseForm.steps" 
                rows="4" 
                required 
                placeholder="详细描述执行步骤"
                class="form-textarea"
              ></textarea>
            </div>

            <div class="form-group">
              <label class="form-label">
                <span class="label-icon">🎯</span>
                期望结果
              </label>
              <textarea 
                v-model="testCaseForm.expected" 
                rows="3" 
                required 
                placeholder="描述期望的测试结果"
                class="form-textarea"
              ></textarea>
            </div>

            <div class="form-group">
              <label class="form-label">
                <span class="label-icon">✅</span>
                用例状态
              </label>
              <div class="status-selector">
                <button 
                  type="button"
                  v-for="status in statusOptions" 
                  :key="status.value"
                  @click="testCaseForm.status = status.value"
                  :class="['status-option', status.value, { active: testCaseForm.status === status.value }]"
                >
                  <span class="status-indicator"></span>
                  {{ status.label }}
                </button>
              </div>
            </div>
          </form>

          <div class="modal-footer">
            <button @click="closeModal" class="btn-cancel">取消</button>
            <button @click="saveTestCase" class="btn-submit">
              <span class="btn-spinner" v-if="loading"></span>
              <span v-else>{{ editingTestCase ? '保存修改' : '创建用例' }}</span>
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
            <span>⚠️</span>
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
import { testcaseAPI, projectAPI } from '../api/index.js'

const testcases = ref([])
const projects = ref([])
const showCreateModal = ref(false)
const editingTestCase = ref(null)
const loading = ref(false)

const filters = ref({
  project_id: '',
  status: ''
})

const testCaseForm = ref({
  project_id: '',
  module: '',
  title: '',
  steps: '',
  expected: '',
  status: '有效'
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

const statusOptions = [
  { value: '草稿', label: '草稿' },
  { value: '有效', label: '有效' },
  { value: '已弃用', label: '已弃用' },
  { value: '阻塞', label: '阻塞' }
]

const statusMap = {
  '草稿': { text: '草稿', icon: '📝' },
  '有效': { text: '有效', icon: '✅' },
  '已弃用': { text: '已弃用', icon: '❌' },
  '阻塞': { text: '阻塞', icon: '🚫' }
}

onMounted(async () => {
  await loadProjects()
  await loadTestCases()
})

const loadProjects = async () => {
  try {
    const response = await projectAPI.getList()
    projects.value = response.data.items
  } catch (error) {
    console.error('加载项目列表失败:', error)
  }
}

const loadTestCases = async () => {
  try {
    const response = await testcaseAPI.getList(
      1,
      100,
      filters.value.project_id || null,
      null,
      filters.value.status || null
    )
    testcases.value = response.data.items
  } catch (error) {
    console.error('加载测试用例失败:', error)
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
  if (!testCaseForm.value.project_id) {
    showToast('warning', '提示', '请选择所属项目！')
    return false
  }
  if (!testCaseForm.value.module || !testCaseForm.value.module.trim()) {
    showToast('warning', '提示', '模块为必填项！')
    return false
  }
  if (!testCaseForm.value.title || !testCaseForm.value.title.trim()) {
    showToast('warning', '提示', '用例标题为必填项！')
    return false
  }
  if (!testCaseForm.value.steps || !testCaseForm.value.steps.trim()) {
    showToast('warning', '提示', '执行步骤为必填项！')
    return false
  }
  if (!testCaseForm.value.expected || !testCaseForm.value.expected.trim()) {
    showToast('warning', '提示', '期望结果为必填项！')
    return false
  }
  return true
}

const saveTestCase = async () => {
  if (!validateForm()) return
  
  loading.value = true
  try {
    const dataToSend = {
      ...testCaseForm.value,
      project_id: parseInt(testCaseForm.value.project_id)
    }
    if (editingTestCase.value) {
      await testcaseAPI.update(editingTestCase.value.id, dataToSend)
      showToast('success', '成功', '用例修改成功！')
    } else {
      await testcaseAPI.create(dataToSend)
      showToast('success', '成功', '用例创建成功！')
    }
    closeModal()
    await loadTestCases()
  } catch (error) {
    console.error('保存测试用例失败:', error)
    const errorMsg = error.response?.data?.detail || '保存测试用例失败'
    showToast('error', '错误', errorMsg)
  } finally {
    loading.value = false
  }
}

const editTestCase = (testcase) => {
  editingTestCase.value = testcase
  testCaseForm.value = { ...testcase }
  showCreateModal.value = true
}

const deleteTestCase = async (id) => {
  showConfirm('确定要删除这个测试用例吗？此操作不可恢复。', async () => {
    try {
      await testcaseAPI.delete(id)
      await loadTestCases()
      showToast('success', '成功', '删除成功！')
    } catch (error) {
      console.error('删除测试用例失败:', error)
      showToast('error', '错误', '删除测试用例失败')
    }
  })
}

const closeModal = () => {
  showCreateModal.value = false
  editingTestCase.value = null
  testCaseForm.value = {
    project_id: '',
    module: '',
    title: '',
    steps: '',
    expected: '',
    status: '有效'
  }
}

const getStatusText = (status) => {
  return statusMap[status]?.text || status
}
</script>

<style scoped>
.testcases-page {
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

.page-header::after {
  content: '';
  position: absolute;
  bottom: -30%;
  left: -5%;
  width: 200px;
  height: 200px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 50%;
  animation: float 8s ease-in-out infinite reverse;
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
  min-width: 200px;
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

.testcase-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 0 24px 24px;
}

.testcase-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid #e2e8f0;
}

.testcase-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(102, 126, 234, 0.1);
  border-color: #667eea;
}

.card-header {
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  background: linear-gradient(135deg, #f9fafb, #f3f4f6);
  border-bottom: 1px solid #e5e7eb;
}

.testcase-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1f2937;
  flex: 1;
}

.status-badges {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 4px;
}

.module-badge {
  background: #e0e7ff;
  color: #4338ca;
}

.status-badge {
  transition: all 0.3s;
}

.status-badge.草稿 {
  background: #fef3c7;
  color: #92400e;
}

.status-badge.有效 {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.已弃用 {
  background: #f3f4f6;
  color: #6b7280;
}

.status-badge.阻塞 {
  background: #fee2e2;
  color: #991b1b;
}

.card-content {
  padding: 20px;
}

.content-section {
  margin-bottom: 16px;
}

.content-section:last-child {
  margin-bottom: 0;
}

.section-label {
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

.section-text {
  margin: 0;
  color: #374151;
  line-height: 1.6;
  font-size: 0.95rem;
}

.section-text.expected {
  color: #059669;
  font-weight: 500;
}

.card-footer {
  padding: 16px 20px;
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.testcase-id {
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
  max-width: 700px;
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
  grid-template-columns: 1fr 1fr;
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

.status-selector {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.status-option {
  flex: 1;
  min-width: 80px;
  padding: 10px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  background: white;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  color: #6b7280;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.status-option .status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #e5e7eb;
  transition: all 0.3s;
}

.status-option.草稿 { border-color: #fcd34d; }
.status-option.草稿 .status-indicator { background: #fcd34d; }
.status-option.有效 { border-color: #34d399; }
.status-option.有效 .status-indicator { background: #34d399; }
.status-option.已弃用 { border-color: #9ca3af; }
.status-option.已弃用 .status-indicator { background: #9ca3af; }
.status-option.阻塞 { border-color: #f87171; }
.status-option.阻塞 .status-indicator { background: #f87171; }

.status-option.active {
  color: white;
  transform: scale(1.05);
}

.status-option.草稿.active { background: #fcd34d; border-color: #fcd34d; }
.status-option.有效.active { background: #34d399; border-color: #34d399; }
.status-option.已弃用.active { background: #9ca3af; border-color: #9ca3af; }
.status-option.阻塞.active { background: #f87171; border-color: #f87171; }

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
    margin-left: 0;
    width: 100%;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .modal-container {
    margin: 16px;
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
