<template>
  <div class="projects-page">
    <div class="page-content">
      <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <span class="title-icon">📁</span>
            项目管理
          </h1>
          <p class="page-subtitle">管理和跟踪所有测试项目</p>
        </div>
        <button @click="showCreateModal = true" class="btn-create">
          <span class="btn-icon">+</span>
          创建项目
        </button>
      </div>
    </div>

    <div v-if="projects.length === 0" class="empty-state">
      <div class="empty-icon">📂</div>
      <h3>暂无项目</h3>
      <p>创建第一个项目来开始您的测试之旅</p>
      <button @click="showCreateModal = true" class="btn-primary">创建项目</button>
    </div>

    <div v-else class="projects-grid">
      <div v-for="project in projects" :key="project.id" class="project-card" @click="viewProject(project.id)">
        <div class="card-glow"></div>
        <div class="card-header">
          <div class="project-icon">
            <span class="icon-bg"></span>
            <span class="icon-emoji">🚀</span>
          </div>
          <div class="status-indicator"></div>
        </div>
        
        <div class="card-body">
          <h3 class="project-name">{{ project.name }}</h3>
          <p class="project-description">{{ project.description || '暂无描述' }}</p>
          
          <div class="project-stats">
            <div class="stat-item">
              <span class="stat-icon">📅</span>
              <span class="stat-label">创建时间</span>
              <span class="stat-value">{{ formatDate(project.created_at) }}</span>
            </div>
          </div>
        </div>

        <div class="card-footer">
          <div class="action-buttons" @click.stop>
            <button @click="viewProject(project.id)" class="btn-view" title="查看详情">
              <span>👁</span>
            </button>
            <button @click="deleteProject(project.id)" class="btn-delete" title="删除">
              <span>🗑</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <Transition name="modal">
      <div v-if="showCreateModal" class="modal-overlay" @click="showCreateModal = false">
        <div class="modal-container" @click.stop>
          <div class="modal-header">
            <div class="modal-title">
              <span class="modal-icon">✨</span>
              <h2>创建新项目</h2>
            </div>
            <button @click="showCreateModal = false" class="btn-close">×</button>
          </div>
          
          <form @submit.prevent="createProject" class="modal-body">
            <div class="form-group">
              <label class="form-label">
                <span class="label-icon">📝</span>
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
                <span class="label-icon">📄</span>
                项目描述
              </label>
              <textarea 
                v-model="newProject.description" 
                rows="4" 
                placeholder="描述项目目标和范围"
                class="form-textarea"
              ></textarea>
            </div>
            
            <div class="form-group">
              <label class="form-label">
                <span class="label-icon">👤</span>
                负责人
              </label>
              <select v-model="newProject.owner_id" required class="form-select">
                <option value="1">测试工程师</option>
                <option value="2">开发工程师</option>
                <option value="3">产品经理</option>
              </select>
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
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { projectAPI } from '../api/index.js'

const projects = ref([])
const showCreateModal = ref(false)
const loading = ref(false)
const newProject = ref({
  name: '',
  description: '',
  owner_id: 1
})

onMounted(async () => {
  await loadProjects()
})

const loadProjects = async () => {
  try {
    const response = await projectAPI.getList()
    projects.value = response.data.items
  } catch (error) {
    console.error('加载项目列表失败:', error)
  }
}

const createProject = async () => {
  if (!newProject.value.name.trim()) return
  
  loading.value = true
  try {
    await projectAPI.create(newProject.value)
    showCreateModal.value = false
    newProject.value = { name: '', description: '', owner_id: 1 }
    await loadProjects()
  } catch (error) {
    console.error('创建项目失败:', error)
    alert('创建项目失败')
  } finally {
    loading.value = false
  }
}

const deleteProject = async (id) => {
  if (!confirm('确定要删除这个项目吗？此操作不可恢复。')) return
  
  try {
    await projectAPI.delete(id)
    await loadProjects()
  } catch (error) {
    console.error('删除项目失败:', error)
    alert('删除项目失败')
  }
}

const viewProject = (id) => {
  console.log('查看项目:', id)
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

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
  padding: 0 24px 24px;
}

.project-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  border: 1px solid #e2e8f0;
}

.project-card:hover {
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

.project-card:hover .card-glow {
  opacity: 1;
}

.card-header {
  padding: 20px;
  position: relative;
}

.project-icon {
  width: 60px;
  height: 60px;
  border-radius: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.icon-bg {
  position: absolute;
  inset: -2px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 16px;
  opacity: 0.3;
  animation: rotate 3s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.icon-emoji {
  font-size: 1.8rem;
  position: relative;
  z-index: 1;
}

.status-indicator {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 12px;
  height: 12px;
  background: #10b981;
  border-radius: 50%;
  box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.2);
  animation: pulse-dot 2s ease-in-out infinite;
}

@keyframes pulse-dot {
  0%, 100% { box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.2); }
  50% { box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
}

.card-body {
  padding: 0 20px 20px;
}

.project-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 8px 0;
}

.project-description {
  color: #6b7280;
  font-size: 0.9rem;
  line-height: 1.5;
  margin: 0 0 16px 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.project-stats {
  border-top: 1px solid #e5e7eb;
  padding-top: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.85rem;
  color: #6b7280;
}

.stat-icon {
  font-size: 1rem;
}

.stat-label {
  color: #9ca3af;
}

.stat-value {
  font-weight: 500;
  color: #374151;
  margin-left: auto;
}

.card-footer {
  padding: 16px 20px;
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
}

.action-buttons {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.btn-view,
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

.btn-view {
  background: #e0e7ff;
  color: #4338ca;
}

.btn-view:hover {
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
  min-height: 100px;
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

  .projects-grid {
    grid-template-columns: 1fr;
    padding: 0 16px 16px;
  }

  .modal-container {
    margin: 16px;
  }
}
</style>
