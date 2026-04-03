<template>
  <div class="reset-password-page">
    <!-- 左侧装饰区域 -->
    <div class="left-section">
      <div class="logo-section">
        <div class="logo-link" @click="animationKey++">
          <img
            src="https://i.postimg.cc/nLrDYrHW/icon.png"
            alt="REFRESH logo"
            class="logo-image"
          />
          <span>REFRESH</span>
        </div>
      </div>

      <div class="characters-section">
        <AnimatedCharacters
          :key="animationKey"
          :isTyping="isTyping"
          :showPassword="showPassword"
          :passwordLength="newPassword.length"
          :loginFailed="false"
          :loginSuccess="success"
        />
      </div>

      <div class="footer-links">
        <a href="/privacy-policy" class="footer-link">Privacy Policy</a>
        <a href="/terms" class="footer-link">Terms of Service</a>
      </div>

      <div class="grid-overlay"></div>
      <div class="blur-circle blur-circle-1"></div>
      <div class="blur-circle blur-circle-2"></div>
    </div>

    <!-- 右侧表单区域 -->
    <div class="right-section">
      <div class="form-wrapper">
        <!-- 移动端 Logo -->
        <div class="mobile-logo" @click="animationKey++">
          <img
            src="https://i.postimg.cc/nLrDYrHW/icon.png"
            alt="REFRESH logo"
            class="logo-image"
          />
          <span>REFRESH</span>
        </div>

        <!-- 表单头部 -->
        <div class="form-header">
          <h1 class="form-title">Set New Password</h1>
          <p class="form-subtitle">Create a new password for your account</p>
        </div>

        <!-- 重置密码表单 -->
        <form @submit.prevent="handleSubmit" class="reset-form">
          <!-- 新密码字段 -->
          <div class="form-group">
            <label for="newPassword" class="form-label">New Password</label>
            <div class="password-wrapper">
              <input
                id="newPassword"
                v-model="newPassword"
                :type="showPassword ? 'text' : 'password'"
                placeholder="••••••••"
                class="form-input"
                required
                @focus="isTyping = true"
                @blur="isTyping = false"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="password-toggle"
              >
                <svg v-if="showPassword" class="icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
            <p v-if="errors.newPassword" class="error-message">{{ errors.newPassword }}</p>
          </div>

          <!-- 确认密码字段 -->
          <div class="form-group">
            <label for="confirmPassword" class="form-label">Confirm Password</label>
            <div class="password-wrapper">
              <input
                id="confirmPassword"
                v-model="confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                placeholder="••••••••"
                class="form-input"
                required
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
            <p v-if="errors.confirmPassword" class="error-message">{{ errors.confirmPassword }}</p>
          </div>

          <!-- 错误提示 -->
          <div v-if="errorMessage" class="error-alert">
            {{ errorMessage }}
          </div>

          <!-- 成功提示 -->
          <div v-if="successMessage" class="success-alert">
            {{ successMessage }}
          </div>

          <!-- 提交按钮 -->
          <button
            type="submit"
            class="submit-button"
            :disabled="isLoading"
          >
            <span class="button-text">{{ isLoading ? 'Resetting...' : 'Reset Password' }}</span>
            <svg class="button-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M5 12h14"/>
              <path d="m12 5 7 7-7 7"/>
            </svg>
          </button>
        </form>

        <!-- 返回登录 -->
        <div class="back-to-login">
          <router-link to="/login" class="back-link">
            <svg class="back-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="m15 18-6-6 6-6"/>
            </svg>
            Back to Login
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import AnimatedCharacters from './AnimatedCharacters.vue'
import { authAPI } from '../api/index.js'

const router = useRouter()
const route = useRoute()

// 从路由参数或 localStorage 获取邮箱和验证码
const email = ref(route.query.email || localStorage.getItem('reset_email') || '')
const code = ref(route.query.code || localStorage.getItem('reset_code') || '')

// 表单数据
const newPassword = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const isTyping = ref(false)
const isLoading = ref(false)
const success = ref(false)
const animationKey = ref(0)

// 错误和成功消息
const errorMessage = ref('')
const successMessage = ref('')
const errors = ref({
  newPassword: '',
  confirmPassword: ''
})

// 验证表单
const validateForm = () => {
  errors.value = { newPassword: '', confirmPassword: '' }
  let isValid = true

  // 验证新密码
  if (!newPassword.value) {
    errors.value.newPassword = 'New password is required'
    isValid = false
  } else if (newPassword.value.length < 6) {
    errors.value.newPassword = 'Password must be at least 6 characters'
    isValid = false
  }

  // 验证确认密码
  if (!confirmPassword.value) {
    errors.value.confirmPassword = 'Please confirm your password'
    isValid = false
  } else if (confirmPassword.value !== newPassword.value) {
    errors.value.confirmPassword = 'Passwords do not match'
    isValid = false
  }

  // 验证邮箱和验证码是否存在
  if (!email.value || !code.value) {
    errorMessage.value = 'Missing email or verification code. Please restart the password reset process.'
    isValid = false
  }

  return isValid
}

// 提交表单
const handleSubmit = async () => {
  if (!validateForm()) return

  isLoading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    // 调用重置密码 API
    await authAPI.resetPassword(email.value, code.value, newPassword.value)
    
    success.value = true
    successMessage.value = 'Password reset successful! Redirecting to login...'
    
    // 清除临时存储
    localStorage.removeItem('reset_email')
    localStorage.removeItem('reset_code')
    
    // 延迟跳转到登录页
    setTimeout(() => {
      router.push('/login')
    }, 1500)
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Failed to reset password. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.reset-password-page {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 100vh;
  max-height: 100vh;
  overflow: hidden;
}

.left-section {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background: linear-gradient(to bottom right, #9ca3af, #6b7280, #4b5563);
  padding: 3rem;
  color: white;
}

.logo-section {
  position: relative;
  z-index: 20;
  display: inline-block;
  width: auto;
}

.logo-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.125rem;
  font-weight: 600;
  text-decoration: none;
  color: inherit;
  padding: 0.5rem;
  margin: -0.5rem;
  border-radius: 0.5rem;
  transition: background-color 0.2s;
  cursor: pointer;
}

.logo-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.logo-image {
  width: 32px;
  height: 32px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(4px);
  padding: 0.25rem;
  border-radius: 0.5rem;
}

.characters-section {
  position: relative;
  z-index: 20;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  height: 500px;
}

.footer-links {
  position: relative;
  z-index: 20;
  display: flex;
  align-items: center;
  gap: 2rem;
  font-size: 0.875rem;
  color: #4b5563;
}

.footer-link {
  color: inherit;
  text-decoration: none;
  transition: color 0.2s;
}

.footer-link:hover {
  color: #1f2937;
}

.grid-overlay {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.05) 1px, transparent 1px);
  background-size: 20px 20px;
}

.blur-circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(96px);
}

.blur-circle-1 {
  top: 25%;
  right: 25%;
  width: 16rem;
  height: 16rem;
  background: rgba(156, 163, 175, 0.2);
}

.blur-circle-2 {
  bottom: 25%;
  left: 25%;
  width: 24rem;
  height: 24rem;
  background: rgba(209, 213, 219, 0.2);
}

.right-section {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: white;
}

.form-wrapper {
  width: 100%;
  max-width: 420px;
}

.mobile-logo {
  display: none;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 3rem;
  cursor: pointer;
}

.form-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.form-title {
  font-size: 1.875rem;
  font-weight: 700;
  letter-spacing: -0.025em;
  margin-bottom: 0.5rem;
  color: #111827;
}

.form-subtitle {
  font-size: 0.875rem;
  color: #6b7280;
}

.reset-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.form-input {
  width: 100%;
  height: 3rem;
  padding: 0 1rem;
  background: white;
  border: 1.5px solid rgba(229, 231, 235, 0.6);
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: all 0.2s;
  outline: none;
}

.form-input:focus {
  border-color: #6366f1;
}

.password-wrapper {
  position: relative;
}

.password-wrapper .form-input {
  padding-right: 2.5rem;
}

.password-toggle {
  position: absolute;
  right: 0.75rem;
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
  color: #111827;
}

.icon {
  width: 20px;
  height: 20px;
}

.error-message {
  font-size: 0.875rem;
  color: #dc2626;
}

.error-alert {
  padding: 0.75rem;
  font-size: 0.875rem;
  color: #dc2626;
  background: rgba(220, 38, 38, 0.1);
  border: 1px solid rgba(220, 38, 38, 0.3);
  border-radius: 0.5rem;
}

.success-alert {
  padding: 0.75rem;
  font-size: 0.875rem;
  color: #16a34a;
  background: rgba(22, 163, 74, 0.1);
  border: 1px solid rgba(22, 163, 74, 0.3);
  border-radius: 0.5rem;
}

.submit-button {
  position: relative;
  width: 100%;
  height: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 1rem;
  font-weight: 500;
  border-radius: 0.5rem;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s;
  background: #111827;
  color: white;
  border: none;
}

.submit-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.button-text {
  transition: transform 0.3s;
}

.button-icon {
  width: 20px;
  height: 20px;
  transition: transform 0.3s;
}

.submit-button:hover:not(:disabled) .button-text {
  transform: translateX(-8px);
}

.submit-button:hover:not(:disabled) .button-icon {
  transform: translateX(8px);
}

.back-to-login {
  margin-top: 1.5rem;
  text-align: center;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #6b7280;
  text-decoration: none;
  transition: color 0.2s;
}

.back-link:hover {
  color: #111827;
}

.back-icon {
  width: 16px;
  height: 16px;
}

@media (max-width: 1024px) {
  .reset-password-page {
    grid-template-columns: 1fr;
  }

  .left-section {
    display: none;
  }

  .mobile-logo {
    display: flex;
  }
}
</style>
