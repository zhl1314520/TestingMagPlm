<template>
  <div class="projects-page">
    <div class="page-content">
      <div class="page-header">
        <div class="header-content">
          <div class="title-section">
            <div class="title-badge">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
              </svg>
              Project Hub
            </div>
            <h1 class="page-title">项目管理</h1>
            <p class="page-subtitle">管理和跟踪所有测试项目，构建质量防线</p>
          </div>
          <button v-if="canCreateProject" @click="showCreateModal = true" class="btn-create">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <line x1="12" y1="5" x2="12" y2="19"/>
              <line x1="5" y1="12" x2="19" y2="12"/>
            </svg>
            创建项目
          </button>
        </div>
        <div class="header-decoration">
          <div class="deco-blob deco-blob-1"></div>
          <div class="deco-blob deco-blob-2"></div>
        </div>
      </div>

      <div class="search-section">
        <div class="search-bar">
          <svg class="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"/>
            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="搜索项目名称或描述..."
            class="search-input"
          />
          <button v-if="searchQuery" @click="searchQuery = ''" class="search-clear">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        <div class="project-count">
          <span class="count-number">{{ filteredProjects.length }}</span>
          <span class="count-label">个项目</span>
        </div>
      </div>

      <div v-if="filteredProjects.length === 0 && projects.length > 0" class="empty-search">
        <div class="empty-search-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"/>
            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
        </div>
        <h3>未找到匹配项目</h3>
        <p>尝试使用其他关键词搜索</p>
      </div>

      <div v-else-if="projects.length === 0" class="empty-state">
        <div class="empty-visual">
          <div class="empty-icon-wrapper">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
              <line x1="12" y1="11" x2="12" y2="17"/>
              <line x1="9" y1="14" x2="15" y2="14"/>
            </svg>
          </div>
          <div class="empty-glow"></div>
        </div>
        <h3>暂无项目</h3>
        <p>创建第一个项目来开始您的测试之旅</p>
        <button v-if="canCreateProject" @click="showCreateModal = true" class="btn-primary">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          创建项目
        </button>
      </div>

      <div v-else class="projects-grid">
        <article
          v-for="(project, index) in filteredProjects"
          :key="project.id"
          class="project-card"
          :class="`card-theme-${(index % 4) + 1}`"
          @click="viewProject(project.id)"
        >
          <div class="card-accent-bar"></div>
          
          <div class="card-header">
            <div class="project-icon glass-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
              </svg>
            </div>
            <div class="status-dot"></div>
          </div>
          
          <div class="card-body">
            <h3 class="project-name">{{ project.name }}</h3>
            <p class="project-description">{{ project.description || '暂无描述' }}</p>
            
            <div class="project-meta">
              <div class="meta-item">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                  <line x1="16" y1="2" x2="16" y2="6"/>
                  <line x1="8" y1="2" x2="8" y2="6"/>
                  <line x1="3" y1="10" x2="21" y2="10"/>
                </svg>
                <span>{{ formatDate(project.created_at) }}</span>
              </div>
            </div>
          </div>

          <div class="card-footer">
            <div class="action-buttons" @click.stop>
              <button @click="openEditModal(project)" class="btn-action btn-edit" title="修改">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                </svg>
              </button>
              <button @click="deleteProject(project.id)" class="btn-action btn-delete" title="删除">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="3 6 5 6 21 6"/>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                  <line x1="10" y1="11" x2="10" y2="17"/>
                  <line x1="14" y1="11" x2="14" y2="17"/>
                </svg>
              </button>
            </div>
          </div>
        </article>
      </div>
    </div>

    <Transition name="modal">
      <div v-if="showCreateModal" class="modal-overlay" @click="showCreateModal = false">
        <div class="modal-container glass-panel" @click.stop>
          <div class="modal-header">
            <div class="modal-title">
              <div class="modal-icon-wrapper icon-wrapper-ember">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="12" y1="5" x2="12" y2="19"/>
                  <line x1="5" y1="12" x2="19" y2="12"/>
                </svg>
              </div>
              <h2>创建新项目</h2>
            </div>
            <button @click="showCreateModal = false" class="btn-close">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
          
          <form @submit.prevent="createProject" class="modal-body">
            <div class="form-group">
              <label class="form-label">
                <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                </svg>
                项目名称
              </label>
              <input 
                v-model="newProject.name" 
                type="text" 
                required 
                placeholder="输入项目名称"
                class="form-input"
              />
            </div>
            
            <div class="form-group">
              <label class="form-label">
                <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                  <line x1="16" y1="17" x2="8" y2="17"/>
                </svg>
                项目描述
              </label>
              <textarea 
                v-model="newProject.description" 
                rows="4" 
                required
                placeholder="描述项目目标和范围"
                class="form-textarea"
              ></textarea>
            </div>
          </form>

          <div class="modal-footer">
            <button @click="showCreateModal = false" class="btn-cancel">取消</button>
            <button @click="createProject" class="btn-submit">
              <span class="btn-spinner" v-if="loading"></span>
              <span v-else>创建项目</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <Transition name="modal">
      <div v-if="showEditModal" class="modal-overlay" @click="showEditModal = false">
        <div class="modal-container glass-panel" @click.stop>
          <div class="modal-header">
            <div class="modal-title">
              <div class="modal-icon-wrapper icon-wrapper-teal">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                </svg>
              </div>
              <h2>修改项目</h2>
            </div>
            <button @click="showEditModal = false" class="btn-close">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
          
          <form @submit.prevent="updateProject" class="modal-body">
            <div class="form-group">
              <label class="form-label">
                <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                </svg>
                项目名称
              </label>
              <input 
                v-model="editProject.name" 
                type="text" 
                required 
                placeholder="输入项目名称"
                class="form-input"
              />
            </div>
            
            <div class="form-group">
              <label class="form-label">
                <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                  <line x1="16" y1="17" x2="8" y2="17"/>
                </svg>
                项目描述
              </label>
              <textarea 
                v-model="editProject.description" 
                rows="4" 
                required
                placeholder="描述项目目标和范围"
                class="form-textarea"
              ></textarea>
            </div>
          </form>

          <div class="modal-footer">
            <button @click="showEditModal = false" class="btn-cancel">取消</button>
            <button @click="updateProject" class="btn-submit btn-teal">
              <span class="btn-spinner" v-if="loading"></span>
              <span v-else>保存修改</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <Transition name="modal">
      <div v-if="showDetailModal" class="modal-overlay" @click="showDetailModal = false">
        <div class="modal-container glass-panel detail-modal" @click.stop>
          <div class="modal-header">
            <div class="modal-title">
              <div class="modal-icon-wrapper icon-wrapper-detail">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
                </svg>
              </div>
              <h2>项目详情</h2>
            </div>
            <button @click="showDetailModal = false" class="btn-close">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
          
          <div class="modal-body" v-if="selectedProject">
            <div class="detail-section">
              <div class="detail-label">
                <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                </svg>
                项目名称
              </div>
              <div class="detail-value">{{ selectedProject.name }}</div>
            </div>
            
            <div class="detail-section">
              <div class="detail-label">
                <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                  <line x1="16" y1="17" x2="8" y2="17"/>
                </svg>
                项目描述
              </div>
              <div class="detail-value description-text">{{ selectedProject.description || '暂无描述' }}</div>
            </div>
            
            <div class="detail-row">
              <div class="detail-section half">
                <div class="detail-label">
                  <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                    <line x1="16" y1="2" x2="16" y2="6"/>
                    <line x1="8" y1="2" x2="8" y2="6"/>
                    <line x1="3" y1="10" x2="21" y2="10"/>
                  </svg>
                  创建时间
                </div>
                <div class="detail-value">{{ formatDate(selectedProject.created_at) }}</div>
              </div>
              
              <div class="detail-section half">
                <div class="detail-label">
                  <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"/>
                    <polyline points="12 6 12 12 16 14"/>
                  </svg>
                  更新时间
                </div>
                <div class="detail-value">{{ formatDate(selectedProject.updated_at) }}</div>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button @click="showDetailModal = false" class="btn-cancel">关闭</button>
            <button @click="editFromDetail" class="btn-submit btn-teal">
              编辑项目
            </button>
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
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { projectAPI } from '../api/index.js'

const projects = ref([])
const searchQuery = ref('')
const showCreateModal = ref(false)
const showEditModal = ref(false)
const showDetailModal = ref(false)
const selectedProject = ref(null)
const loading = ref(false)
const userInfo = ref(null)

const canCreateProject = computed(() => {
  return userInfo.value && userInfo.value.role !== 'tester'
})

const filteredProjects = computed(() => {
  if (!searchQuery.value.trim()) {
    return projects.value
  }
  const query = searchQuery.value.toLowerCase().trim()
  return projects.value.filter(project => 
    project.name.toLowerCase().includes(query) ||
    (project.description && project.description.toLowerCase().includes(query))
  )
})

const newProject = ref({
  name: '',
  description: ''
})
const editProject = ref({
  id: null,
  name: '',
  description: ''
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

onMounted(async () => {
  const storedUserInfo = localStorage.getItem('user_info')
  if (storedUserInfo) {
    userInfo.value = JSON.parse(storedUserInfo)
  }
  await loadProjects()
})

const loadProjects = async () => {
  try {
    const response = await projectAPI.getList(1, 100)
    projects.value = response.data.items
  } catch (error) {
    console.error('加载项目列表失败:', error)
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

const createProject = async () => {
  if (!newProject.value.name.trim()) return
  if (!newProject.value.description || !newProject.value.description.trim()) {
    showToast('warning', '提示', '项目描述为必填项！')
    return
  }
  
  loading.value = true
  try {
    await projectAPI.create(newProject.value)
    showCreateModal.value = false
    newProject.value = { name: '', description: '' }
    await loadProjects()
    showToast('success', '成功', '创建成功！')
  } catch (error) {
    console.error('创建项目失败:', error)
    showToast('error', '错误', '创建项目失败')
  } finally {
    loading.value = false
  }
}

const deleteProject = async (id) => {
  showConfirm('确定要删除这个项目吗？此操作不可恢复。', async () => {
    try {
      await projectAPI.delete(id)
      await loadProjects()
      showToast('success', '成功', '删除成功！')
    } catch (error) {
      console.error('删除项目失败:', error)
      showToast('error', '错误', '删除项目失败')
    }
  })
}

const openEditModal = (project) => {
  editProject.value = {
    id: project.id,
    name: project.name,
    description: project.description || ''
  }
  showEditModal.value = true
}

const updateProject = async () => {
  if (!editProject.value.name.trim()) return
  if (!editProject.value.description || !editProject.value.description.trim()) {
    showToast('warning', '提示', '项目描述为必填项！')
    return
  }
  
  loading.value = true
  try {
    await projectAPI.update(editProject.value.id, {
      name: editProject.value.name,
      description: editProject.value.description
    })
    showEditModal.value = false
    await loadProjects()
    showToast('success', '成功', '修改成功！')
  } catch (error) {
    console.error('修改项目失败:', error)
    showToast('error', '错误', '修改项目失败')
  } finally {
    loading.value = false
  }
}

// 项目详情页
const viewProject = (projectId) => {
  const project = projects.value.find(p => p.id === projectId)
  if (project) {
    selectedProject.value = project
    showDetailModal.value = true
  }
}

const editFromDetail = () => {
  if (selectedProject.value) {
    showDetailModal.value = false
    openEditModal(selectedProject.value)
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style scoped>
.projects-page {
  min-height: 100%;
  padding: var(--space-md);
}

.page-content {
  border-radius: var(--radius-xl);
  overflow: hidden;
  box-shadow: var(--shadow-lg);
  border: 1px solid rgba(232, 93, 4, 0.08);
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
    radial-gradient(circle at 50% 50%, rgba(232, 93, 4, 0.25) 0%, rgba(232, 93, 4, 0.15) 30%, rgba(232, 93, 4, 0.08) 50%, transparent 70%);
}

.deco-blob-2 {
  width: 150px;
  height: 150px;
  bottom: -30%;
  left: 10%;
  background: 
    radial-gradient(circle at 50% 50%, rgba(20, 184, 166, 0.2) 0%, rgba(20, 184, 166, 0.12) 30%, rgba(20, 184, 166, 0.06) 50%, transparent 70%);
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
  background: linear-gradient(135deg, rgba(232, 93, 4, 0.25), rgba(250, 163, 7, 0.15));
  border: 1px solid rgba(232, 93, 4, 0.3);
  color: var(--ember-soft);
  margin-bottom: var(--space-sm);
}

.page-title {
  font-size: 2rem;
  font-weight: 800;
  margin: 0 0 var(--space-xs) 0;
  letter-spacing: -0.02em;
}

.page-subtitle {
  font-size: 1rem;
  opacity: 0.8;
  margin: 0;
}

.btn-create {
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-lg);
  border-radius: var(--radius-md);
  border: 2px solid rgba(255, 255, 255, 0.25);
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
}

.btn-create:hover {
  background: linear-gradient(135deg, var(--ember-core), var(--ember-glow));
  border-color: transparent;
}

.search-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-lg) var(--space-xl);
  background: white;
  border-bottom: 1px solid rgba(232, 93, 4, 0.08);
  gap: var(--space-lg);
}

.search-bar {
  display: flex;
  align-items: center;
  flex: 1;
  max-width: 400px;
  background: rgba(232, 93, 4, 0.04);
  border: 2px solid rgba(232, 93, 4, 0.1);
  border-radius: var(--radius-md);
  padding: var(--space-sm) var(--space-md);
  transition: all 0.3s var(--ease-smooth);
}

.search-bar:focus-within {
  border-color: var(--ember-core);
  background: white;
  box-shadow: 0 0 0 4px rgba(232, 93, 4, 0.1);
}

.search-icon {
  color: var(--ink-soft);
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  border: none;
  background: transparent;
  padding: 0 var(--space-sm);
  font-size: 0.95rem;
  color: var(--ink-primary);
  outline: none;
}

.search-input::placeholder {
  color: var(--ink-muted);
}

.search-clear {
  width: 28px;
  height: 28px;
  border: none;
  background: rgba(232, 93, 4, 0.1);
  border-radius: var(--radius-sm);
  color: var(--ink-soft);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s var(--ease-smooth);
  flex-shrink: 0;
}

.search-clear:hover {
  background: var(--ember-core);
  color: white;
}

.project-count {
  display: flex;
  align-items: baseline;
  gap: var(--space-xs);
  padding: var(--space-sm) var(--space-md);
  background: linear-gradient(135deg, rgba(232, 93, 4, 0.08), rgba(250, 163, 7, 0.06));
  border-radius: var(--radius-md);
  border: 1px solid rgba(232, 93, 4, 0.12);
}

.count-number {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--ember-core);
}

.count-label {
  font-size: 0.9rem;
  color: var(--ink-soft);
  font-weight: 500;
}

.empty-search {
  text-align: center;
  padding: var(--space-3xl) var(--space-xl);
}

.empty-search-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto var(--space-lg);
  border-radius: var(--radius-lg);
  background: linear-gradient(135deg, rgba(232, 93, 4, 0.08), rgba(250, 163, 7, 0.06));
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--ember-core);
}

.empty-search h3 {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--ink-primary);
  margin: 0 0 var(--space-sm) 0;
}

.empty-search p {
  margin: 0;
  color: var(--ink-soft);
  font-size: 0.9rem;
}

.projects-grid {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
  padding: var(--space-xl);
}

.project-card {
  position: relative;
  background: white;
  border-radius: var(--radius-lg);
  overflow: hidden;
  cursor: pointer;
  border: 1px solid rgba(232, 93, 4, 0.08);
  transition: transform 0.3s var(--ease-bounce), box-shadow 0.3s var(--ease-smooth);
  display: flex;
  flex-direction: row;
  align-items: stretch;
}

.project-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.card-accent-bar {
  width: 6px;
  flex-shrink: 0;
  background: linear-gradient(180deg, var(--ember-core), var(--ember-soft));
}

.card-theme-1 .card-accent-bar { background: linear-gradient(180deg, var(--ember-core), var(--ember-soft)); }
.card-theme-2 .card-accent-bar { background: linear-gradient(180deg, var(--teal-primary), var(--teal-bright)); }
.card-theme-3 .card-accent-bar { background: linear-gradient(180deg, var(--coral-primary), var(--coral-bright)); }
.card-theme-4 .card-accent-bar { background: linear-gradient(180deg, var(--forest-primary), var(--forest-bright)); }

.card-header {
  padding: var(--space-lg);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: var(--space-sm);
  min-width: 80px;
}

.project-icon {
  width: 52px;
  height: 52px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: saturate(180%) blur(20px);
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: var(--shadow-md);
  transition: all 0.3s var(--ease-smooth);
}

.card-theme-1 .project-icon.glass-icon,
.card-theme-2 .project-icon.glass-icon,
.card-theme-3 .project-icon.glass-icon,
.card-theme-4 .project-icon.glass-icon {
  background: rgba(255, 255, 255, 0.1);
  color: var(--ink-primary);
}

.card-theme-1:hover .project-icon.glass-icon,
.card-theme-2:hover .project-icon.glass-icon,
.card-theme-3:hover .project-icon.glass-icon,
.card-theme-4:hover .project-icon.glass-icon {
  background: rgba(255, 255, 255, 0.2);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--forest-bright);
  box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.2);
}

.card-body {
  padding: var(--space-lg);
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-width: 0;
}

.project-name {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--ink-primary);
  margin: 0 0 var(--space-sm) 0;
}

.project-description {
  color: var(--ink-soft);
  font-size: 0.9rem;
  line-height: 1.6;
  margin: 0 0 var(--space-md) 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.project-meta {
  display: flex;
  align-items: center;
  gap: var(--space-lg);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-size: 0.85rem;
  color: var(--ink-soft);
}

.meta-item svg {
  color: var(--ember-core);
}

.card-footer {
  padding: var(--space-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  border-left: 1px solid rgba(232, 93, 4, 0.08);
  background: linear-gradient(90deg, rgba(232, 93, 4, 0.02), rgba(250, 163, 7, 0.01));
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.btn-action {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-edit {
  background: linear-gradient(135deg, rgba(20, 184, 166, 0.1), rgba(94, 234, 212, 0.08));
  color: var(--teal-primary);
}

.btn-edit:hover {
  background: linear-gradient(135deg, var(--teal-deep), var(--teal-bright));
  color: white;
}

.btn-delete {
  background: linear-gradient(135deg, rgba(244, 63, 94, 0.1), rgba(253, 164, 175, 0.08));
  color: var(--coral-primary);
}

.btn-delete:hover {
  background: linear-gradient(135deg, var(--coral-deep), var(--coral-bright));
  color: white;
}

.empty-state {
  text-align: center;
  padding: var(--space-3xl) var(--space-xl);
}

.empty-visual {
  position: relative;
  display: inline-block;
  margin-bottom: var(--space-xl);
}

.empty-icon-wrapper {
  width: 100px;
  height: 100px;
  border-radius: var(--radius-xl);
  background: linear-gradient(135deg, rgba(232, 93, 4, 0.08), rgba(250, 163, 7, 0.06));
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--ember-core);
  position: relative;
  z-index: 1;
}

.empty-glow {
  position: absolute;
  inset: -20px;
  background: radial-gradient(circle, rgba(232, 93, 4, 0.12) 0%, rgba(232, 93, 4, 0.06) 40%, transparent 70%);
  box-shadow: 0 0 60px rgba(232, 93, 4, 0.1);
  border-radius: 50%;
}

.empty-state h3 {
  font-size: 1.35rem;
  font-weight: 700;
  color: var(--ink-primary);
  margin: 0 0 var(--space-sm) 0;
}

.empty-state p {
  margin: 0 0 var(--space-xl) 0;
  color: var(--ink-soft);
  font-size: 0.95rem;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-xl);
  border-radius: var(--radius-md);
  border: none;
  background: linear-gradient(135deg, var(--ember-core), var(--ember-glow));
  color: white;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s var(--ease-smooth);
  box-shadow: var(--shadow-md), 0 0 15px rgba(232, 93, 4, 0.2);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg), 0 0 25px rgba(232, 93, 4, 0.3);
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(10, 15, 26, 0.5);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  z-index: 1000;
  padding: 100px var(--space-xl) var(--space-xl);
  overflow-y: auto;
}

.modal-container {
  border-radius: var(--radius-xl);
  width: 100%;
  max-width: 500px;
  max-height: calc(100vh - 160px);
  box-shadow: var(--shadow-xl);
  animation: scale-bounce 0.4s var(--ease-bounce);
  overflow-y: auto;
  border: 1px solid rgba(232, 93, 4, 0.08);
}

.modal-header {
  padding: var(--space-xl);
  border-bottom: 1px solid rgba(232, 93, 4, 0.08);
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  background: inherit;
  z-index: 1;
}

.modal-title {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.modal-icon-wrapper {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
}

.icon-wrapper-ember {
  background: linear-gradient(135deg, rgba(232, 93, 4, 0.1), rgba(250, 163, 7, 0.08));
  color: var(--ember-core);
}

.icon-wrapper-teal {
  background: linear-gradient(135deg, rgba(20, 184, 166, 0.1), rgba(94, 234, 212, 0.08));
  color: var(--teal-primary);
}

.icon-wrapper-detail {
  background: linear-gradient(135deg, rgba(232, 93, 4, 0.1), rgba(20, 184, 166, 0.08));
  color: var(--ember-core);
}

.modal-title h2 {
  margin: 0;
  font-size: 1.25rem;
  color: var(--ink-primary);
  font-weight: 700;
}

.btn-close {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  border: none;
  background: rgba(232, 93, 4, 0.04);
  color: var(--ink-soft);
  cursor: pointer;
  transition: all 0.3s var(--ease-smooth);
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-close:hover {
  background: rgba(232, 93, 4, 0.08);
  color: var(--ember-core);
  transform: rotate(90deg);
}

.modal-body {
  padding: var(--space-xl);
}

.detail-modal {
  max-width: 560px;
}

.detail-section {
  margin-bottom: var(--space-lg);
}

.detail-section.half {
  flex: 1;
}

.detail-row {
  display: flex;
  gap: var(--space-xl);
}

.detail-label {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  margin-bottom: var(--space-sm);
  font-weight: 600;
  color: var(--ink-secondary);
  font-size: 0.9rem;
}

.detail-label .label-icon {
  color: var(--ember-core);
}

.detail-value {
  padding: var(--space-sm) var(--space-md);
  background: rgba(232, 93, 4, 0.03);
  border-radius: var(--radius-md);
  color: var(--ink-primary);
  font-size: 0.95rem;
  border: 1px solid rgba(232, 93, 4, 0.08);
}

.detail-value.description-text {
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.6;
}

.form-group {
  margin-bottom: var(--space-lg);
}

.form-label {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  margin-bottom: var(--space-sm);
  font-weight: 600;
  color: var(--ink-secondary);
  font-size: 0.9rem;
}

.label-icon {
  color: var(--ember-core);
}

.form-input,
.form-textarea {
  width: 100%;
  padding: var(--space-sm) var(--space-md);
  border: 2px solid rgba(232, 93, 4, 0.1);
  border-radius: var(--radius-md);
  font-size: 0.95rem;
  font-family: inherit;
  transition: all 0.3s var(--ease-smooth);
  background: white;
  color: var(--ink-primary);
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--ember-core);
  box-shadow: 0 0 0 4px rgba(232, 93, 4, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.modal-footer {
  padding: var(--space-xl);
  border-top: 1px solid rgba(232, 93, 4, 0.08);
  display: flex;
  gap: var(--space-md);
  justify-content: flex-end;
  position: sticky;
  bottom: 0;
  background: inherit;
}

.btn-cancel,
.btn-submit {
  padding: var(--space-sm) var(--space-xl);
  border-radius: var(--radius-md);
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s var(--ease-smooth);
  border: none;
}

.btn-cancel {
  background: rgba(232, 93, 4, 0.04);
  color: var(--ink-muted);
}

.btn-cancel:hover {
  background: rgba(232, 93, 4, 0.08);
  color: var(--ink-primary);
}

.btn-submit {
  background: linear-gradient(135deg, var(--ember-core), var(--ember-glow));
  color: white;
  box-shadow: var(--shadow-md), 0 0 15px rgba(232, 93, 4, 0.15);
}

.btn-submit:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg), 0 0 25px rgba(232, 93, 4, 0.25);
}

.btn-submit.btn-teal {
  background: linear-gradient(135deg, var(--teal-deep), var(--teal-bright));
  box-shadow: var(--shadow-md), 0 0 15px rgba(20, 184, 166, 0.15);
}

.btn-submit.btn-teal:hover {
  box-shadow: var(--shadow-lg), 0 0 25px rgba(20, 184, 166, 0.25);
}

.btn-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
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
  border-radius: var(--radius-lg);
  padding: var(--space-lg) var(--space-xl);
  box-shadow: var(--shadow-xl);
  display: flex;
  align-items: center;
  gap: var(--space-md);
  max-width: 400px;
  animation: scale-bounce 0.4s var(--ease-bounce);
  border: 1px solid rgba(232, 93, 4, 0.08);
}

.toast-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.toast-icon.success {
  background: linear-gradient(135deg, var(--forest-primary), var(--forest-bright));
  box-shadow: 0 0 20px rgba(34, 197, 94, 0.3);
}

.toast-icon.error {
  background: linear-gradient(135deg, var(--coral-deep), var(--coral-bright));
  box-shadow: 0 0 20px rgba(244, 63, 94, 0.3);
}

.toast-icon.warning {
  background: linear-gradient(135deg, var(--amber-primary), var(--amber-soft));
  box-shadow: 0 0 20px rgba(251, 191, 36, 0.3);
}

.toast-content {
  flex: 1;
}

.toast-title {
  margin: 0 0 4px 0;
  font-size: 1rem;
  font-weight: 700;
  color: var(--ink-primary);
}

.toast-message {
  margin: 0;
  font-size: 0.875rem;
  color: var(--ink-soft);
}

.toast-close {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm);
  border: none;
  background: transparent;
  color: var(--ink-soft);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s var(--ease-smooth);
  flex-shrink: 0;
}

.toast-close:hover {
  background: rgba(232, 93, 4, 0.06);
  color: var(--ember-core);
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
  border-radius: var(--radius-xl);
  padding: var(--space-xl);
  min-width: 360px;
  max-width: 90vw;
  box-shadow: var(--shadow-xl);
  text-align: center;
  animation: scale-bounce 0.4s var(--ease-bounce);
  border: 1px solid rgba(232, 93, 4, 0.08);
}

.confirm-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto var(--space-lg);
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.1), rgba(217, 119, 6, 0.08));
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--amber-primary);
}

.confirm-title {
  margin: 0 0 var(--space-sm) 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--ink-primary);
}

.confirm-message {
  margin: 0 0 var(--space-xl) 0;
  font-size: 0.9375rem;
  color: var(--ink-soft);
  line-height: 1.6;
}

.confirm-actions {
  display: flex;
  gap: var(--space-md);
  justify-content: center;
}

.confirm-btn {
  padding: var(--space-sm) var(--space-xl);
  border-radius: var(--radius-md);
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s var(--ease-smooth);
  border: none;
}

.confirm-btn.cancel {
  background: rgba(232, 93, 4, 0.04);
  color: var(--ink-muted);
}

.confirm-btn.cancel:hover {
  background: rgba(232, 93, 4, 0.08);
  color: var(--ink-primary);
}

.confirm-btn.delete {
  background: linear-gradient(135deg, var(--coral-deep), var(--coral-bright));
  color: white;
  box-shadow: var(--shadow-sm), 0 0 15px rgba(244, 63, 94, 0.2);
}

.confirm-btn.delete:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md), 0 0 20px rgba(244, 63, 94, 0.3);
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s var(--ease-smooth);
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.toast-enter-active {
  animation: scale-bounce 0.4s var(--ease-bounce);
}

.toast-leave-active {
  animation: fade-out 0.2s var(--ease-smooth);
}

@keyframes fade-out {
  to {
    opacity: 0;
    transform: scale(0.9);
  }
}

.confirm-enter-active {
  animation: scale-bounce 0.4s var(--ease-bounce);
}

.confirm-leave-active {
  animation: fade-out 0.2s var(--ease-smooth);
}

@media (max-width: 768px) {
  .page-header {
    padding: var(--space-lg);
  }

  .header-content {
    flex-direction: column;
    gap: var(--space-md);
    align-items: flex-start;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .search-section {
    flex-direction: column;
    align-items: stretch;
    padding: var(--space-md) var(--space-lg);
  }

  .search-bar {
    max-width: none;
  }

  .project-count {
    justify-content: center;
  }

  .projects-grid {
    padding: var(--space-lg);
    gap: var(--space-sm);
  }

  .project-card {
    flex-direction: column;
  }

  .card-accent-bar {
    width: 100%;
    height: 4px;
  }

  .card-theme-1 .card-accent-bar { background: linear-gradient(90deg, var(--ember-core), var(--ember-soft)); }
  .card-theme-2 .card-accent-bar { background: linear-gradient(90deg, var(--teal-primary), var(--teal-bright)); }
  .card-theme-3 .card-accent-bar { background: linear-gradient(90deg, var(--coral-primary), var(--coral-bright)); }
  .card-theme-4 .card-accent-bar { background: linear-gradient(90deg, var(--forest-primary), var(--forest-bright)); }

  .card-header {
    flex-direction: row;
    justify-content: space-between;
    padding: var(--space-md) var(--space-lg);
  }

  .card-body {
    padding: 0 var(--space-lg) var(--space-md);
  }

  .card-footer {
    border-left: none;
    border-top: 1px solid rgba(232, 93, 4, 0.08);
    padding: var(--space-md) var(--space-lg);
  }

  .action-buttons {
    flex-direction: row;
    justify-content: flex-end;
  }

  .modal-overlay {
    padding: var(--space-lg);
  }

  .modal-container {
    margin-top: var(--space-lg);
  }
}
</style>
