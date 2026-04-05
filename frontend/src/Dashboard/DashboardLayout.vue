<template>
  <div class="dashboard">
    <!-- 顶部导航栏 -->
    <nav class="navbar">
      <div class="nav-container">
        <div class="nav-brand" @click="router.push('/dashboard')">
          <div class="brand-logo">
            <div class="logo-icon">◈</div>
          </div>
          <div class="brand-info">
            <span class="brand-name">HBNU-TMP</span>
            <span class="brand-slogan">Quality First</span>
          </div>
        </div>
        
        <div class="nav-menu">
          <router-link 
            v-for="item in navItems" 
            :key="item.path" 
            :to="item.path" 
            class="nav-item"
            :class="{ 'nav-item-active': isActive(item.path) }"
          >
            <span class="nav-icon">{{ item.icon }}</span>
            <span class="nav-label">{{ item.label }}</span>
            <span class="nav-indicator"></span>
          </router-link>
        </div>
        
        <div class="nav-actions">
          <div class="notification-bell">
            <span class="bell-icon">🔔</span>
            <span class="notification-dot"></span>
          </div>
          
          <div class="user-menu-container" @click="toggleUserMenu">
            <div class="user-avatar">
              <div class="avatar-ring"></div>
              <span class="avatar-text">{{ userInfo?.username?.charAt(0).toUpperCase() }}</span>
            </div>
            <span class="user-name">{{ userInfo?.username }}</span>
            <span class="user-role-badge">{{ userInfo?.role }}</span>
          </div>
          
          <div v-if="showUserMenu" class="user-dropdown-menu">
            <div class="dropdown-header">
              <div class="dropdown-avatar">{{ userInfo?.username?.charAt(0).toUpperCase() }}</div>
              <div class="dropdown-info">
                <div class="dropdown-name">{{ userInfo?.username }}</div>
                <div class="dropdown-role">{{ userInfo?.role }}</div>
              </div>
            </div>
            
            <div class="dropdown-section">
              <div class="dropdown-item" @click.stop="openProfileModal">
                <span class="dropdown-icon">👤</span>
                <span>个人资料</span>
                <span class="dropdown-arrow">›</span>
              </div>
            </div>
            
            <div class="dropdown-divider"></div>
            
            <div class="dropdown-item danger" @click="logout">
              <span class="dropdown-icon">🚪</span>
              <span>退出登录</span>
            </div>
          </div>
        </div>
      </div>
    </nav>
    
    <!-- 主内容区域 -->
    <main class="main-content">
      <div class="content-wrapper">
        <router-view />
      </div>
    </main>
    
    <!-- 个人资料模态框 -->
    <Transition name="modal">
      <div v-if="showProfileModal" class="modal-overlay" @click="showProfileModal = false">
        <div class="modal-container" @click.stop>
          <div class="modal-header">
            <div class="modal-title">
              <span class="modal-icon">👤</span>
              <h2>个人资料</h2>
            </div>
            <button @click="showProfileModal = false" class="btn-close">×</button>
          </div>
          
          <div class="modal-body">
            <div class="profile-section">
              <div class="section-title">基本信息</div>
              
              <div class="form-group">
                <label class="form-label">
                  <span class="label-icon">🆔</span>
                  用户 ID
                </label>
                <input 
                  v-model="profileForm.id" 
                  type="text" 
                  disabled 
                  class="form-input disabled"
                />
              </div>
              
              <div class="form-group">
                <label class="form-label">
                  <span class="label-icon">📝</span>
                  用户名
                </label>
                <input 
                  v-model="profileForm.username" 
                  type="text" 
                  disabled 
                  class="form-input disabled"
                />
              </div>
              
              <div class="form-group">
                <label class="form-label">
                  <span class="label-icon">🔒</span>
                  密码
                </label>
                <input 
                  v-model="profileForm.password" 
                  type="password" 
                  disabled 
                  class="form-input disabled"
                  placeholder="••••••••"
                />
              </div>
              
              <div class="form-group">
                <button @click="openPasswordModal" class="btn-change-password">
                  <span class="btn-icon">🔑</span>
                  修改密码
                </button>
              </div>
              
              <div class="form-row">
                <div class="form-group">
                  <label class="form-label">
                    <span class="label-icon">📧</span>
                    邮箱
                  </label>
                  <input 
                    v-model="profileForm.email" 
                    type="email" 
                    class="form-input"
                    placeholder="example@email.com"
                  />
                </div>
                
                <div class="form-group">
                  <label class="form-label">
                    <span class="label-icon">👑</span>
                    角色
                  </label>
                  <select v-model="profileForm.role" class="form-select">
                    <option value="tester">测试工程师</option>
                    <option value="developer">开发工程师</option>
                    <option value="manager">产品经理</option>
                  </select>
                </div>
              </div>
              
              <div class="form-group">
                <label class="form-label">
                  <span class="label-icon">📅</span>
                  创建时间
                </label>
                <input 
                  v-model="profileForm.created_at" 
                  type="text" 
                  disabled 
                  class="form-input disabled"
                />
              </div>
            </div>
          </div>
          
          <div class="modal-footer">
            <button @click="showProfileModal = false" class="btn-cancel">取消</button>
            <button @click="saveProfile" class="btn-submit">
              <span class="btn-spinner" v-if="loading"></span>
              <span v-else>保存修改</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>
    
    <!-- 修改密码模态框 -->
    <Transition name="modal">
      <div v-if="showPasswordModal" class="modal-overlay" @click="showPasswordModal = false">
        <div class="modal-container" @click.stop>
          <div class="modal-header">
            <div class="modal-title">
              <span class="modal-icon">🔑</span>
              <h2>修改密码</h2>
            </div>
            <button @click="showPasswordModal = false" class="btn-close">×</button>
          </div>
          
          <div class="modal-body">
            <div class="profile-section">
              <div class="form-group">
                <label class="form-label">
                  <span class="label-icon">📧</span>
                  当前邮箱
                </label>
                <input 
                  v-model="passwordForm.email" 
                  type="text" 
                  disabled 
                  class="form-input disabled"
                />
              </div>
              
              <div class="form-group">
                <label class="form-label">
                  <span class="label-icon">🔒</span>
                  加密后的原密码
                </label>
                <input 
                  v-model="profileForm.password" 
                  type="password" 
                  disabled 
                  class="form-input disabled"
                  placeholder="••••••••"
                />
              </div>
              
              <div class="form-group">
                <label class="form-label">
                  <span class="label-icon">🔐</span>
                  请输入原密码
                </label>
                <div class="password-wrapper">
                  <input 
                    v-model="passwordForm.oldPassword" 
                    :type="showOldPassword ? 'text' : 'password'" 
                    class="form-input"
                    placeholder="请输入原密码"
                  />
                  <button
                    type="button"
                    @click="showOldPassword = !showOldPassword"
                    class="password-toggle"
                  >
                    <svg v-if="showOldPassword" class="icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/>
                      <circle cx="12" cy="12" r="3"/>
                    </svg>
                    <svg v-else class="icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/>
                      <path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/>
                      <path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"/>
                      <line x1="2" x2="22" y1="2" y2="22"/>
                    </svg>
                  </button>
                </div>
              </div>
              
              <div class="form-group">
                <label class="form-label">
                  <span class="label-icon">🔑</span>
                  请输入新密码
                </label>
                <div class="password-wrapper">
                  <input 
                    v-model="passwordForm.newPassword" 
                    :type="showNewPassword ? 'text' : 'password'" 
                    class="form-input"
                    placeholder="请输入新密码"
                  />
                  <button
                    type="button"
                    @click="showNewPassword = !showNewPassword"
                    class="password-toggle"
                  >
                    <svg v-if="showNewPassword" class="icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/>
                      <circle cx="12" cy="12" r="3"/>
                    </svg>
                    <svg v-else class="icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/>
                      <path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/>
                      <path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"/>
                      <line x1="2" x2="22" y1="2" y2="22"/>
                    </svg>
                  </button>
                </div>
              </div>
              
              <div class="form-group">
                <label class="form-label">
                  <span class="label-icon">🔐</span>
                  请确认密码
                </label>
                <div class="password-wrapper">
                  <input 
                    v-model="passwordForm.confirmPassword" 
                    :type="showConfirmPassword ? 'text' : 'password'" 
                    class="form-input"
                    placeholder="请确认密码"
                  />
                  <button
                    type="button"
                    @click="showConfirmPassword = !showConfirmPassword"
                    class="password-toggle"
                  >
                    <svg v-if="showConfirmPassword" class="icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/>
                      <circle cx="12" cy="12" r="3"/>
                    </svg>
                    <svg v-else class="icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/>
                      <path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/>
                      <path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"/>
                      <line x1="2" x2="22" y1="2" y2="22"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <div class="modal-footer">
            <button @click="showPasswordModal = false" class="btn-cancel">取消</button>
            <button @click="changePassword" class="btn-submit">
              <span class="btn-spinner" v-if="passwordLoading"></span>
              <span v-else>确认修改</span>
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { authAPI, userAPI } from '../api/index.js'

const router = useRouter()
const route = useRoute()
const userInfo = ref(null)
const showUserMenu = ref(false)
const showProfileModal = ref(false)
const showPasswordModal = ref(false)
const loading = ref(false)
const passwordLoading = ref(false)

const profileForm = ref({
  id: '',
  username: '',
  password: '',
  role: '',
  email: '',
  created_at: ''
})

const passwordForm = ref({
  email: '',
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const showOldPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)

const toast = ref({
  show: false,
  type: 'success',
  title: '',
  message: ''
})

const showToast = (type, title, message) => {
  toast.value = { show: true, type, title, message }
  setTimeout(() => {
    hideToast()
  }, 3000)
}

const hideToast = () => {
  toast.value.show = false
}

const isActive = (path) => {
  if (path === '/dashboard') {
    return route.path === '/dashboard' || route.path === '/dashboard/'
  }
  return route.path === path
}

const navItems = [
  { path: '/dashboard', label: '概览', icon: '◈' },
  { path: '/dashboard/projects', label: '项目', icon: '◐' },
  { path: '/dashboard/testcases', label: '用例', icon: '◑' },
  { path: '/dashboard/executions', label: '执行', icon: '▶' },
  { path: '/dashboard/bugs', label: '缺陷', icon: '◉' },
  { path: '/dashboard/reports', label: '报告', icon: '◈' }
]

onMounted(() => {
  const storedUserInfo = localStorage.getItem('user_info')
  if (storedUserInfo) {
    userInfo.value = JSON.parse(storedUserInfo)
  }
  
  document.addEventListener('click', handleOutsideClick)
})

onUnmounted(() => {
  document.removeEventListener('click', handleOutsideClick)
})

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

const loadProfile = async () => {
  if (!userInfo.value?.id) return
  
  try {
    const response = await userAPI.getDetail(userInfo.value.id)
    profileForm.value = response.data
  } catch (error) {
    console.error('加载个人资料失败:', error)
  }
}

const saveProfile = async () => {
  try {
    await userAPI.update(userInfo.value.id, {
      email: profileForm.value.email,
      role: profileForm.value.role
    })
    
    const updatedUserInfo = {
      ...userInfo.value,
      email: profileForm.value.email,
      role: profileForm.value.role
    }
    localStorage.setItem('user_info', JSON.stringify(updatedUserInfo))
    userInfo.value = updatedUserInfo
    
    showProfileModal.value = false
    showToast('success', '成功', '个人资料更新成功')
  } catch (error) {
    console.error('更新个人资料失败:', error)
    showToast('error', '错误', '更新失败：' + (error.response?.data?.detail || '未知错误'))
  }
}

// 打开个人资料模态框时加载数据
const openProfileModal = async () => {
  await loadProfile()
  showProfileModal.value = true
}

const handleOutsideClick = (event) => {
  const userMenuContainer = document.querySelector('.user-menu-container')
  const modalOverlay = document.querySelector('.modal-overlay')
  
  if (showProfileModal.value || showPasswordModal.value) return
  
  if (userMenuContainer && !userMenuContainer.contains(event.target)) {
    showUserMenu.value = false
  }
}

const openPasswordModal = () => {
  passwordForm.value = {
    email: profileForm.value.email,
    oldPassword: '',
    newPassword: '',
    confirmPassword: ''
  }
  showOldPassword.value = false
  showNewPassword.value = false
  showConfirmPassword.value = false
  showPasswordModal.value = true
}

const changePassword = async () => {
  if (!passwordForm.value.oldPassword) {
    showToast('warning', '提示', '请输入原密码')
    return
  }
  if (!passwordForm.value.newPassword) {
    showToast('warning', '提示', '请输入新密码')
    return
  }
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    showToast('warning', '提示', '两次输入的密码不一致')
    return
  }
  if (passwordForm.value.newPassword.length < 6) {
    showToast('warning', '提示', '新密码长度不能少于6位')
    return
  }
  
  passwordLoading.value = true
  try {
    await userAPI.changePassword(userInfo.value.id, {
      old_password: passwordForm.value.oldPassword,
      new_password: passwordForm.value.newPassword
    })
    showToast('success', '成功', '密码修改成功')
    showPasswordModal.value = false
  } catch (error) {
    console.error('修改密码失败:', error)
    const detail = error.response?.data?.detail
    if (detail === 'OLD_PASSWORD_INCORRECT') {
      showToast('error', '错误', '原密码错误')
    } else {
      showToast('error', '错误', '修改失败：' + (detail || '未知错误'))
    }
  } finally {
    passwordLoading.value = false
  }
}

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user_info')
  sessionStorage.removeItem('token')
  router.push('/login')
}
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
}

.dashboard::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
  pointer-events: none;
  z-index: 0;
}

/* 顶部导航栏 */
.navbar {
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(20px) saturate(180%);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
  border-bottom: 1px solid rgba(102, 126, 234, 0.1);
  overflow: visible;
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 75px;
  overflow: visible;
}

/* 品牌区域 */
.nav-brand {
  display: flex;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-brand:hover {
  transform: translateX(-4px);
}

.brand-logo {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  animation: logoFloat 3s ease-in-out infinite;
}

.logo-icon {
  font-size: 1.75rem;
  color: white;
  font-weight: 300;
}

@keyframes logoFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

.brand-info {
  display: flex;
  flex-direction: column;
}

.brand-name {
  font-size: 1.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
  letter-spacing: -0.5px;
}

.brand-slogan {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 500;
  letter-spacing: 0.5px;
}

/* 导航菜单 */
.nav-menu {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.nav-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border-radius: 1rem;
  color: #64748b;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.875rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.nav-item::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
  opacity: 0;
  transition: opacity 0.3s;
}

.nav-item:hover::before {
  opacity: 1;
}

.nav-item:hover {
  color: #667eea;
  transform: translateY(-2px);
}

.nav-item-active {
  color: #667eea;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
}

.nav-item-active .nav-indicator {
  width: 100%;
}

.nav-icon {
  font-size: 1.125rem;
  transition: transform 0.3s;
}

.nav-item:hover .nav-icon {
  transform: scale(1.2) rotate(5deg);
}

.nav-label {
  position: relative;
  z-index: 1;
}

.nav-indicator {
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #667eea, #764ba2);
  transition: all 0.3s;
  transform: translateX(-50%);
}

/* 导航操作区 */
.nav-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
}

.notification-bell {
  position: relative;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: rgba(102, 126, 234, 0.05);
  cursor: pointer;
  transition: all 0.3s;
}

.notification-bell:hover {
  background: rgba(102, 126, 234, 0.1);
  transform: scale(1.1);
}

.bell-icon {
  font-size: 1.25rem;
}

.notification-dot {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 8px;
  height: 8px;
  background: linear-gradient(135deg, #f093fb, #f5576c);
  border-radius: 50%;
  border: 2px solid white;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.2); opacity: 0.8; }
}

/* 用户菜单 */
.user-menu-container {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  cursor: pointer;
  transition: all 0.3s;
  background: rgba(255, 255, 255, 0.8);
}

.user-menu-container:hover {
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
  transform: translateY(-2px);
}

.user-avatar {
  position: relative;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 1.125rem;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.avatar-ring {
  position: absolute;
  inset: -2px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  z-index: -1;
  animation: ringRotate 3s linear infinite;
}

@keyframes ringRotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.avatar-text {
  animation: avatarPulse 2s ease-in-out infinite;
}

@keyframes avatarPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.8; }
}

.user-name {
  font-weight: 600;
  color: #1e293b;
  font-size: 0.875rem;
}

.user-role-badge {
  font-size: 0.75rem;
  color: #667eea;
  background: rgba(102, 126, 234, 0.1);
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-weight: 600;
  text-transform: capitalize;
}

/* 用户下拉菜单 */
.user-dropdown-menu {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  width: 280px;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  padding: 0.75rem;
  animation: dropdownSlide 0.3s ease-out;
  z-index: 1001;
}

@keyframes dropdownSlide {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05));
}

.dropdown-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 1.25rem;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.dropdown-info {
  flex: 1;
}

.dropdown-name {
  font-weight: 700;
  color: #1e293b;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.dropdown-role {
  font-size: 0.75rem;
  color: #64748b;
  text-transform: capitalize;
}

.dropdown-divider {
  height: 1px;
  background: rgba(0, 0, 0, 0.05);
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1.25rem;
  cursor: pointer;
  transition: all 0.2s;
  color: #64748b;
}

.dropdown-item:hover {
  background: rgba(102, 126, 234, 0.05);
  color: #667eea;
  padding-left: 1.5rem;
}

.dropdown-icon {
  font-size: 1.125rem;
}

.dropdown-section {
  padding: 0.5rem 0;
}

.dropdown-section-title {
  padding: 0.5rem 1.25rem;
  font-size: 0.75rem;
  color: #94a3b8;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.dropdown-arrow {
  margin-left: auto;
  font-size: 1.25rem;
  color: #94a3b8;
  transition: transform 0.3s;
}

.dropdown-item:hover .dropdown-arrow {
  transform: translateX(4px);
  color: #667eea;
}

.dropdown-item.danger {
  color: #ef4444;
}

.dropdown-item.danger:hover {
  background: rgba(239, 68, 68, 0.1);
  color: #dc2626;
}

/* 个人资料模态框 */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
}

.modal-container {
  background: white;
  border-radius: 20px;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.2);
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
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

.profile-section {
  margin-bottom: 24px;
}

.section-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #e5e7eb;
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
.form-select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
}

.form-input.disabled {
  background: #f3f4f6;
  color: #9ca3af;
  cursor: not-allowed;
}

.password-wrapper {
  position: relative;
}

.password-wrapper .form-input {
  padding-right: 45px;
}

.password-toggle {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  transition: color 0.2s;
}

.password-toggle:hover {
  color: #374151;
}

.password-toggle .icon {
  width: 20px;
  height: 20px;
}

.btn-change-password {
  width: 100%;
  padding: 12px 24px;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid #667eea;
  background: white;
  color: #667eea;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-change-password:hover {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.btn-icon {
  font-size: 1.1rem;
}

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

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

/* 主内容区域 */
.main-content {
  padding: 2rem 0;
  min-height: calc(100vh - 75px);
  position: relative;
  z-index: 1;
}

.content-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .nav-container {
    padding: 0 1rem;
  }
  
  .nav-label {
    display: none;
  }
  
  .content-wrapper {
    padding: 0 1rem;
  }
}

@media (max-width: 768px) {
  .nav-menu {
    display: none;
  }
  
  .brand-name {
    font-size: 1.25rem;
  }
  
  .brand-slogan {
    display: none;
  }
  
  .user-name {
    display: none;
  }
  
  .user-role-badge {
    display: none;
  }
  
  .main-content {
    padding: 1rem 0;
  }
}

.toast-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3000;
}

.toast-container {
  background: #ffffff;
  border-radius: 16px;
  padding: 24px 32px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  gap: 16px;
  max-width: 400px;
  animation: toastIn 0.3s ease;
}

@keyframes toastIn {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.toast-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
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
  font-size: 1.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
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
</style>
