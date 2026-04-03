<template>
  <div class="forgot-password-page">
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
          :showPassword="false"
          :passwordLength="0"
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
          <h1 class="form-title">Forgot Password?</h1>
          <p class="form-subtitle">Enter your email to reset your password</p>
        </div>

        <!-- 重置密码表单 -->
        <form @submit.prevent="handleSubmit" class="reset-form">
          <!-- 邮箱字段 -->
          <div class="form-group">
            <label for="email" class="form-label">Email</label>
            <input
              id="email"
              v-model="email"
              type="email"
              placeholder="you@example.com"
              class="form-input"
              autocomplete="off"
              required
              @focus="isTyping = true"
              @blur="isTyping = false"
            />
            <p v-if="errors.email" class="error-message">{{ errors.email }}</p>
          </div>

          <!-- 验证码字段 -->
          <div class="form-group">
            <label for="code" class="form-label">Verification Code</label>
            <div class="code-wrapper">
              <input
                id="code"
                v-model="code"
                type="text"
                placeholder="Enter verification code"
                class="form-input code-input"
                autocomplete="off"
                required
              />
              <button
                type="button"
                @click="handleSendCode"
                class="send-code-btn"
                :disabled="isSending || countdown > 0"
              >
                {{ countdown > 0 ? `${countdown}s` : 'Get Code' }}
              </button>
            </div>
            <p v-if="errors.code" class="error-message">{{ errors.code }}</p>
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
            <span class="button-text">{{ isLoading ? 'Verifying...' : 'Verify & Continue' }}</span>
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
import { useRouter } from 'vue-router'
import AnimatedCharacters from './AnimatedCharacters.vue'
import { authAPI } from '../api/index.js'

const router = useRouter()

// 表单数据
const email = ref('')
const code = ref('')
const isTyping = ref(false)
const isLoading = ref(false)
const isSending = ref(false)
const countdown = ref(0)
const success = ref(false)
const animationKey = ref(0)

// 错误和成功消息
const errorMessage = ref('')
const successMessage = ref('')
const errors = ref({
  email: '',
  code: ''
})

// 验证表单
const validateForm = () => {
  errors.value = { email: '', code: '' }
  let isValid = true

  // 验证邮箱
  if (!email.value) {
    errors.value.email = 'Email is required'
    isValid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    errors.value.email = 'Please enter a valid email address'
    isValid = false
  }

  // 验证验证码
  if (!code.value) {
    errors.value.code = 'Verification code is required'
    isValid = false
  } else if (code.value.length < 4) {
    errors.value.code = 'Verification code must be at least 4 characters'
    isValid = false
  }

  return isValid
}

// 发送验证码
const handleSendCode = async () => {
  // 验证邮箱
  if (!email.value) {
    errors.value.email = 'Email is required'
    return
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    errors.value.email = 'Please enter a valid email address'
    return
  }

  errors.value.email = ''
  isSending.value = true
  errorMessage.value = ''

  try {
    // 调用发送验证码 API
    await authAPI.sendResetCode(email.value)
    
    successMessage.value = 'Verification code sent to your email!'
    
    // 开始倒计时
    countdown.value = 60
    const timer = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0) {
        clearInterval(timer)
      }
    }, 1000)
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Failed to send verification code. Please try again.'
  } finally {
    isSending.value = false
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!validateForm()) return

  isLoading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    // 调用验证验证码 API
    await authAPI.verifyResetCode(email.value, code.value)
    
    success.value = true
    successMessage.value = 'Verification successful! Redirecting...'
    
    // 保存邮箱和验证码到 localStorage，供重置密码页面使用
    localStorage.setItem('reset_email', email.value)
    localStorage.setItem('reset_code', code.value)
    
    // 延迟跳转到重置密码页面
    setTimeout(() => {
      router.push({
        path: '/reset-password',
        query: { email: email.value, code: code.value }
      })
    }, 1000)
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Invalid verification code. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.forgot-password-page {
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

.code-wrapper {
  display: flex;
  gap: 0.5rem;
}

.code-input {
  flex: 1;
}

.send-code-btn {
  height: 3rem;
  padding: 0 1rem;
  background: white;
  border: 1.5px solid rgba(229, 231, 235, 0.6);
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.send-code-btn:hover:not(:disabled) {
  background: #f9fafb;
  border-color: #6366f1;
  color: #6366f1;
}

.send-code-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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
  .forgot-password-page {
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
