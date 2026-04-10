<template>
  <div class="testcases-page">
    <div class="page-content">
      <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <div class="title-badge">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
              <line x1="16" y1="13" x2="8" y2="13"/>
              <line x1="16" y1="17" x2="8" y2="17"/>
            </svg>
            Test Cases
          </div>
          <h1 class="page-title">测试用例管理</h1>
          <p class="page-subtitle">编写和管理高质量的测试用例</p>
        </div>
        <button @click="showCreateModal = true" class="btn-create">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          创建用例
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
              <svg class="filter-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
              </svg>
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
          <select v-model="filters.project_id" @change="loadTestCases" class="filter-select">
            <option value="">全部项目</option>
            <option v-for="project in filteredProjects" :key="project.id" :value="project.id">
              {{ project.name }}
            </option>
          </select>
        </div>
        
        <div class="filter-group">
          <label class="filter-label">
            <svg class="filter-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="9 11 12 14 22 4"/>
              <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
            </svg>
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
      <div class="empty-visual">
        <div class="empty-icon-wrapper">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
            <line x1="16" y1="13" x2="8" y2="13"/>
            <line x1="16" y1="17" x2="8" y2="17"/>
          </svg>
        </div>
        <div class="empty-glow"></div>
      </div>
      <h3>暂无测试用例</h3>
      <p>创建第一个测试用例来开始测试</p>
      <button @click="showCreateModal = true" class="btn-primary">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"/>
          <line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        创建用例
      </button>
    </div>

    <div v-else class="testcase-list">
      <div v-for="testcase in testcases" :key="testcase.id" class="testcase-card">
        <div class="card-header">
          <div class="testcase-title">{{ testcase.title }}</div>
          <div class="status-badges">
            <span class="badge module-badge">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/>
                <line x1="7" y1="7" x2="7.01" y2="7"/>
              </svg>
              {{ testcase.module }}
            </span>
            <span class="badge status-badge" :class="testcase.status">
              {{ getStatusText(testcase.status) }}
            </span>
          </div>
        </div>

        <div class="card-content">
          <div class="content-section">
            <div class="section-label">
              <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="20" x2="12" y2="10"/>
                <line x1="18" y1="20" x2="18" y2="4"/>
                <line x1="6" y1="20" x2="6" y2="16"/>
              </svg>
              执行步骤
              <button @click="showStepsDetail(testcase)" class="btn-detail">详情</button>
            </div>
            <p class="section-text steps-text">{{ testcase.steps }}</p>
          </div>

          <div class="content-section meta-info">
            <div class="meta-row">
              <div class="meta-item">
                <svg class="meta-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
                </svg>
                <span class="meta-label">项目:</span>
                <span class="meta-value">{{ testcase.project_name || '未知项目' }}</span>
              </div>
              <div class="meta-item">
                <svg class="meta-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                  <line x1="12" y1="9" x2="12" y2="13"/>
                  <line x1="12" y1="17" x2="12.01" y2="17"/>
                </svg>
                <span class="meta-label">优先级:</span>
                <span class="meta-value priority-badge" :class="testcase.priority">{{ getPriorityText(testcase.priority) }}</span>
              </div>
              <div class="meta-item">
                <svg class="meta-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                  <line x1="16" y1="2" x2="16" y2="6"/>
                  <line x1="8" y1="2" x2="8" y2="6"/>
                  <line x1="3" y1="10" x2="21" y2="10"/>
                </svg>
                <span class="meta-label">创建时间:</span>
                <span class="meta-value">{{ formatDate(testcase.created_at) }}</span>
              </div>
              <div class="meta-item">
                <svg class="meta-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"/>
                  <polyline points="12 6 12 12 16 14"/>
                </svg>
                <span class="meta-label">更新时间:</span>
                <span class="meta-value">{{ formatDate(testcase.updated_at) }}</span>
              </div>
            </div>
          </div>

          <div class="content-section">
            <div class="section-label">
              <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/>
                <circle cx="12" cy="12" r="6"/>
                <circle cx="12" cy="12" r="2"/>
              </svg>
              期望结果
            </div>
            <p class="section-text expected">{{ testcase.expected }}</p>
          </div>
        </div>

        <div class="card-footer">
          <div class="testcase-id">#{{ testcase.id }}</div>
          <div class="action-buttons">
            <button @click="editTestCase(testcase)" class="btn-edit" title="编辑">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
              </svg>
            </button>
            <button @click="deleteTestCase(testcase.id)" class="btn-delete" title="删除">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="3 6 5 6 21 6"/>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                <line x1="10" y1="11" x2="10" y2="17"/>
                <line x1="14" y1="11" x2="14" y2="17"/>
              </svg>
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
              <div class="modal-icon-wrapper" :class="editingTestCase ? 'icon-wrapper-teal' : 'icon-wrapper-ember'">
                <svg v-if="editingTestCase" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                </svg>
                <svg v-else width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="12" y1="5" x2="12" y2="19"/>
                  <line x1="5" y1="12" x2="19" y2="12"/>
                </svg>
              </div>
              <h2>{{ editingTestCase ? '编辑用例' : '创建新用例' }}</h2>
            </div>
            <button @click="closeModal" class="btn-close">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
          
          <form @submit.prevent="saveTestCase" class="modal-body">
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">
                  <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
                  </svg>
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
                  <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/>
                    <line x1="7" y1="7" x2="7.01" y2="7"/>
                  </svg>
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
                <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                  <line x1="16" y1="17" x2="8" y2="17"/>
                </svg>
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
                <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="12" y1="20" x2="12" y2="10"/>
                  <line x1="18" y1="20" x2="18" y2="4"/>
                  <line x1="6" y1="20" x2="6" y2="16"/>
                </svg>
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
                <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"/>
                  <circle cx="12" cy="12" r="6"/>
                  <circle cx="12" cy="12" r="2"/>
                </svg>
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
                <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                  <line x1="12" y1="9" x2="12" y2="13"/>
                  <line x1="12" y1="17" x2="12.01" y2="17"/>
                </svg>
                优先级
              </label>
              <div class="priority-selector">
                <button 
                  type="button"
                  v-for="priority in priorityOptions" 
                  :key="priority.value"
                  @click="testCaseForm.priority = priority.value"
                  :class="['priority-option', priority.value, { active: testCaseForm.priority === priority.value }]"
                >
                  <span class="priority-indicator"></span>
                  {{ priority.label }}
                </button>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">
                <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="9 11 12 14 22 4"/>
                  <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
                </svg>
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

    <Transition name="modal">
      <div v-if="showStepsModal" class="modal-overlay" @click="showStepsModal = false">
        <div class="modal-container glass-panel detail-modal" @click.stop>
          <div class="modal-header">
            <div class="modal-title">
              <div class="modal-icon-wrapper icon-wrapper-detail">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="12" y1="20" x2="12" y2="10"/>
                  <line x1="18" y1="20" x2="18" y2="4"/>
                  <line x1="6" y1="20" x2="6" y2="16"/>
                </svg>
              </div>
              <h2>执行步骤详情</h2>
            </div>
            <button @click="showStepsModal = false" class="btn-close">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
          
          <div class="modal-body" v-if="selectedTestCase">
            <div class="steps-detail-container">
              <div v-for="(step, index) in getStepsArray(selectedTestCase.steps)" :key="index" class="step-item">
                <span class="step-content">{{ step }}</span>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button @click="showStepsModal = false" class="btn-cancel">关闭</button>
          </div>
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
const projectSearchKeyword = ref('')
const showCreateModal = ref(false)
const editingTestCase = ref(null)
const loading = ref(false)
const showStepsModal = ref(false)
const selectedTestCase = ref(null)

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
  status: '有效',
  priority: 'p3'
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

const priorityOptions = [
  { value: 'p0', label: 'P0-最高' },
  { value: 'p1', label: 'P1-高' },
  { value: 'p2', label: 'P2-中' },
  { value: 'p3', label: 'P3-低' }
]

const statusMap = {
  '草稿': { text: '草稿', icon: '📝' },
  '有效': { text: '有效', icon: '✅' },
  '已弃用': { text: '已弃用', icon: '❌' },
  '阻塞': { text: '阻塞', icon: '🚫' }
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
  // 搜索功能已通过filteredProjects自动实现
  // 这个方法可以用于触发额外的操作，如日志记录
  console.log('搜索项目:', projectSearchKeyword.value)
}

onMounted(async () => {
  await loadProjects()
  await loadTestCases()
})

const loadProjects = async () => {
  try {
    const response = await projectAPI.getList(1, 100)
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
    status: '有效',
    priority: 'p3'
  }
}

const getStatusText = (status) => {
  return statusMap[status]?.text || status
}

const getPriorityText = (priority) => {
  const priorityMap = {
    'p0': 'P0-最高',
    'p1': 'P1-高',
    'p2': 'P2-中',
    'p3': 'P3-低'
  }
  return priorityMap[priority] || priority
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const showStepsDetail = (testcase) => {
  selectedTestCase.value = testcase
  showStepsModal.value = true
}

const getStepsArray = (steps) => {
  if (!steps) return []
  return steps.split('\n').filter(step => step.trim())
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
    radial-gradient(circle at 50% 50%, rgba(20, 184, 166, 0.25) 0%, rgba(20, 184, 166, 0.15) 30%, rgba(20, 184, 166, 0.08) 50%, transparent 70%);
}

.deco-blob-2 {
  width: 150px;
  height: 150px;
  bottom: -40%;
  left: 10%;
  background: 
    radial-gradient(circle at 50% 50%, rgba(94, 234, 212, 0.2) 0%, rgba(94, 234, 212, 0.12) 30%, rgba(94, 234, 212, 0.06) 50%, transparent 70%);
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
  background: linear-gradient(135deg, rgba(20, 184, 166, 0.25), rgba(94, 234, 212, 0.15));
  color: var(--teal-soft);
  border: 1px solid rgba(20, 184, 166, 0.3);
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
  min-width: 200px;
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

.meta-info {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.03), rgba(118, 75, 162, 0.02));
  border-radius: 12px;
  padding: 12px 16px;
  margin: 16px 0;
}

.meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.85rem;
}

.meta-icon {
  color: #667eea;
  flex-shrink: 0;
}

.meta-label {
  color: #6b7280;
  font-weight: 500;
}

.meta-value {
  color: #374151;
  font-weight: 600;
}

.priority-badge {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 700;
}

.priority-badge.p0 {
  background: linear-gradient(135deg, #dc2626, #ef4444);
  color: white;
}

.priority-badge.p1 {
  background: linear-gradient(135deg, #ea580c, #f97316);
  color: white;
}

.priority-badge.p2 {
  background: linear-gradient(135deg, #ca8a04, #eab308);
  color: white;
}

.priority-badge.p3 {
  background: linear-gradient(135deg, #16a34a, #22c55e);
  color: white;
}

.steps-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.btn-detail {
  margin-left: auto;
  padding: 4px 12px;
  border-radius: 6px;
  border: none;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.08));
  color: #667eea;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-detail:hover {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  transform: translateY(-1px);
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

.priority-selector {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.priority-option {
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

.priority-option .priority-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #e5e7eb;
  transition: all 0.3s;
}

.priority-option.p0 { border-color: #dc2626; }
.priority-option.p0 .priority-indicator { background: #dc2626; }
.priority-option.p1 { border-color: #ea580c; }
.priority-option.p1 .priority-indicator { background: #ea580c; }
.priority-option.p2 { border-color: #ca8a04; }
.priority-option.p2 .priority-indicator { background: #ca8a04; }
.priority-option.p3 { border-color: #16a34a; }
.priority-option.p3 .priority-indicator { background: #16a34a; }

.priority-option.active {
  color: white;
  transform: scale(1.05);
}

.priority-option.p0.active { background: #dc2626; border-color: #dc2626; }
.priority-option.p1.active { background: #ea580c; border-color: #ea580c; }
.priority-option.p2.active { background: #ca8a04; border-color: #ca8a04; }
.priority-option.p3.active { background: #16a34a; border-color: #16a34a; }

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

.glass-panel {
  background: white;
}

.detail-modal {
  max-width: 560px;
}

.icon-wrapper-detail {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.08));
  color: #667eea;
}

.steps-detail-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.step-item {
  padding: 12px;
  background: rgba(102, 126, 234, 0.03);
  border-radius: 8px;
  border: 1px solid rgba(102, 126, 234, 0.08);
}

.step-content {
  color: #374151;
  line-height: 1.6;
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
