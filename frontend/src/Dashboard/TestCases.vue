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
            <option value="new">新建</option>
            <option value="executed">已执行</option>
            <option value="failed">失败</option>
            <option value="passed">通过</option>
            <option value="blocked">阻塞</option>
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
  status: 'new'
})

const statusOptions = [
  { value: 'new', label: '新建' },
  { value: 'executed', label: '已执行' },
  { value: 'failed', label: '失败' },
  { value: 'passed', label: '通过' },
  { value: 'blocked', label: '阻塞' }
]

const statusMap = {
  new: { text: '新建', icon: '🆕' },
  executed: { text: '已执行', icon: '▶️' },
  failed: { text: '失败', icon: '❌' },
  passed: { text: '通过', icon: '✅' },
  blocked: { text: '阻塞', icon: '🚫' }
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

const saveTestCase = async () => {
  loading.value = true
  try {
    if (editingTestCase.value) {
      await testcaseAPI.update(editingTestCase.value.id, testCaseForm.value)
    } else {
      await testcaseAPI.create(testCaseForm.value)
    }
    closeModal()
    await loadTestCases()
  } catch (error) {
    console.error('保存测试用例失败:', error)
    alert('保存测试用例失败')
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
  if (!confirm('确定要删除这个测试用例吗？')) return
  
  try {
    await testcaseAPI.delete(id)
    await loadTestCases()
  } catch (error) {
    console.error('删除测试用例失败:', error)
    alert('删除测试用例失败')
  }
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
    status: 'new'
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

.status-badge.new {
  background: #fef3c7;
  color: #92400e;
}

.status-badge.executed {
  background: #dbeafe;
  color: #1e40af;
}

.status-badge.failed {
  background: #fee2e2;
  color: #991b1b;
}

.status-badge.passed {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.blocked {
  background: #f3e8ff;
  color: #6b21a8;
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

.status-option.new { border-color: #fcd34d; }
.status-option.new .status-indicator { background: #fcd34d; }
.status-option.executed { border-color: #60a5fa; }
.status-option.executed .status-indicator { background: #60a5fa; }
.status-option.failed { border-color: #f87171; }
.status-option.failed .status-indicator { background: #f87171; }
.status-option.passed { border-color: #34d399; }
.status-option.passed .status-indicator { background: #34d399; }
.status-option.blocked { border-color: #a78bfa; }
.status-option.blocked .status-indicator { background: #a78bfa; }

.status-option.active {
  color: white;
  transform: scale(1.05);
}

.status-option.new.active { background: #fcd34d; border-color: #fcd34d; }
.status-option.executed.active { background: #60a5fa; border-color: #60a5fa; }
.status-option.failed.active { background: #f87171; border-color: #f87171; }
.status-option.passed.active { background: #34d399; border-color: #34d399; }
.status-option.blocked.active { background: #a78bfa; border-color: #a78bfa; }

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
</style>
