<template>
  <div class="reset-password-page noise-texture">
    <div class="left-section">
      <div class="logo-section">
        <a href="/" class="logo-link">
          <div class="logo-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 2L2 7L12 12L22 7L12 2Z"/>
              <path d="M2 17L12 22L22 17"/>
              <path d="M2 12L12 17L22 12"/>
            </svg>
          </div>
          <span>HBNU-TMP</span>
        </a>
      </div>

      <div class="characters-section">
        <AnimatedCharacters
          :isTyping="isTyping"
          :showPassword="showPassword"
          :passwordLength="newPassword.length"
          :loginFailed="false"
          :loginSuccess="success"
        />
      </div>

      <div class="footer-links">
        <a href="/privacy-policy" class="footer-link">隐私政策</a>
        <a href="/terms" class="footer-link">服务条款</a>
      </div>

      <div class="deco-grid"></div>
      <div class="deco-blob deco-blob-1"></div>
      <div class="deco-blob deco-blob-2"></div>
      <div class="deco-blob deco-blob-3"></div>
    </div>

    <div class="right-section">
      <div class="form-wrapper">
        <div class="mobile-logo">
          <div class="logo-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 2L2 7L12 12L22 7L12 2Z"/>
              <path d="M2 17L12 22L22 17"/>
              <path d="M2 12L12 17L22 12"/>
            </svg>
          </div>
          <span>HBNU-TMP</span>
        </div>

        <div class="form-header">
          <div class="header-badge">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            </svg>
            Secure Reset
          </div>
          <h1 class="form-title">设置新密码</h1>
          <p class="form-subtitle">请为您的新账户创建一个新密码</p>
        </div>

        <form @submit.prevent="handleSubmit" class="reset-form">
          <div class="form-group">
            <label for="newPassword" class="form-label">
              <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>
              新密码
            </label>
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
                <svg v-if="showPassword" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/>
                  <circle cx="12" cy="12" r="3"/>
                </svg>
                <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/>
                  <path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/>
                  <path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"/>
                  <line x1="2" x2="22" y1="2" y2="22"/>
                </svg>
              </button>
            </div>
            <p v-if="errors.newPassword" class="error-message">{{ errors.newPassword }}</p>
          </div>

          <div class="form-group">
            <label for="confirmPassword" class="form-label">
              <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
              </svg>
              确认密码
            </label>
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
                <svg v-if="showConfirmPassword" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/>
                  <circle cx="12" cy="12" r="3"/>
                </svg>
                <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/>
                  <path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/>
                  <path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"/>
                  <line x1="2" x2="22" y1="2" y2="22"/>
                </svg>
              </button>
            </div>
            <p v-if="errors.confirmPassword" class="error-message">{{ errors.confirmPassword }}</p>
          </div>

          <div v-if="errorMessage" class="error-alert">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="12"/>
              <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
            {{ errorMessage }}
          </div>

          <div v-if="successMessage" class="success-alert">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
            {{ successMessage }}
          </div>

          <button
            type="submit"
            class="submit-button"
            :disabled="isLoading"
          >
            <span class="button-text">{{ isLoading ? '重置中...' : '重置密码' }}</span>
            <svg class="button-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M5 12h14"/>
              <path d="m12 5 7 7-7 7"/>
            </svg>
          </button>
        </form>

        <div class="back-to-login">
          <router-link to="/login" class="back-link">
            <svg class="back-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="m15 18-6-6 6-6"/>
            </svg>
            返回登录
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

const email = ref(route.query.email || localStorage.getItem('reset_email') || '')
const code = ref(route.query.code || localStorage.getItem('reset_code') || '')

const newPassword = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const isTyping = ref(false)
const isLoading = ref(false)
const success = ref(false)

const errorMessage = ref('')
const successMessage = ref('')
const errors = ref({
  newPassword: '',
  confirmPassword: ''
})

const validateForm = () => {
  errors.value = { newPassword: '', confirmPassword: '' }
  let isValid = true

  if (!newPassword.value) {
    errors.value.newPassword = '请输入新密码'
    isValid = false
  } else if (newPassword.value.length < 6) {
    errors.value.newPassword = '密码长度至少为 6 位'
    isValid = false
  }

  if (!confirmPassword.value) {
    errors.value.confirmPassword = '请确认密码'
    isValid = false
  } else if (confirmPassword.value !== newPassword.value) {
    errors.value.confirmPassword = '两次密码输入不一致'
    isValid = false
  }

  if (!email.value || !code.value) {
    errorMessage.value = '缺少邮箱或验证码，请重新开始密码重置流程。'
    isValid = false
  }

  return isValid
}

const handleSubmit = async () => {
  if (!validateForm()) return

  isLoading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    await authAPI.resetPassword(email.value, code.value, newPassword.value)
    
    success.value = true
    successMessage.value = '密码重置成功！正在跳转到登录页...'
    
    localStorage.removeItem('reset_email')
    localStorage.removeItem('reset_code')
    
    setTimeout(() => {
      router.push('/login')
    }, 1500)
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || '密码重置失败，请重试。'
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
  padding: var(--space-2xl);
  color: white;
  background: 
    radial-gradient(ellipse at 20% 30%, rgba(232, 93, 4, 0.15), transparent 50%),
    radial-gradient(ellipse at 80% 70%, rgba(20, 184, 166, 0.12), transparent 45%),
    radial-gradient(ellipse at 50% 50%, rgba(244, 63, 94, 0.08), transparent 40%),
    linear-gradient(145deg, var(--ink-primary) 0%, var(--ink-deep) 50%, #0a0f1a 100%);
  overflow: hidden;
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
  gap: var(--space-sm);
  font-size: 1.125rem;
  font-weight: 700;
  text-decoration: none;
  color: inherit;
  padding: var(--space-sm);
  margin: calc(var(--space-sm) * -1);
  border-radius: var(--radius-md);
  transition: all 0.3s var(--ease-smooth);
}

.logo-link:hover {
  background: rgba(255, 255, 255, 0.08);
}

.logo-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, var(--ember-core), var(--ember-glow));
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: var(--shadow-md), 0 0 20px rgba(232, 93, 4, 0.3);
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
  gap: var(--space-xl);
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.5);
}

.footer-link {
  color: inherit;
  text-decoration: none;
  transition: all 0.3s var(--ease-smooth);
}

.footer-link:hover {
  color: var(--ember-soft);
}

.deco-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  pointer-events: none;
}

.deco-blob {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
  transition: transform 0.8s var(--ease-smooth);
}

.deco-blob-1 {
  top: 10%;
  right: 15%;
  width: 250px;
  height: 250px;
  background: 
    radial-gradient(circle at 50% 50%, rgba(232, 93, 4, 0.22) 0%, rgba(232, 93, 4, 0.14) 30%, rgba(232, 93, 4, 0.06) 50%, transparent 70%);
}

.deco-blob-2 {
  bottom: 20%;
  left: 10%;
  width: 200px;
  height: 200px;
  background: 
    radial-gradient(circle at 50% 50%, rgba(20, 184, 166, 0.18) 0%, rgba(20, 184, 166, 0.1) 30%, rgba(20, 184, 166, 0.04) 50%, transparent 70%);
}

.deco-blob-3 {
  top: 50%;
  right: 30%;
  width: 150px;
  height: 150px;
  background: 
    radial-gradient(circle at 50% 50%, rgba(244, 63, 94, 0.14) 0%, rgba(244, 63, 94, 0.08) 30%, rgba(244, 63, 94, 0.03) 50%, transparent 70%);
}

.left-section:hover .deco-blob-1 {
  transform: translate(12px, -12px);
}

.left-section:hover .deco-blob-2 {
  transform: translate(-8px, 8px);
}

.left-section:hover .deco-blob-3 {
  transform: translate(6px, -6px);
}

.right-section {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-2xl);
  background: var(--paper-cream);
}

.form-wrapper {
  width: 100%;
  max-width: 420px;
}

.mobile-logo {
  display: none;
  align-items: center;
  justify-content: center;
  gap: var(--space-sm);
  font-size: 1.125rem;
  font-weight: 700;
  margin-bottom: var(--space-2xl);
  color: var(--ink-primary);
}

.form-header {
  text-align: center;
  margin-bottom: var(--space-2xl);
}

.header-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 1.75rem;
  padding: 4px 14px;
  border-radius: var(--radius-full);
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  background: linear-gradient(135deg, rgba(232, 93, 4, 0.08), rgba(250, 163, 7, 0.06));
  color: var(--ember-core);
  margin-bottom: var(--space-md);
}

.form-title {
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  margin: 0 0 var(--space-sm) 0;
  color: var(--ink-primary);
}

.form-subtitle {
  font-size: 0.95rem;
  color: var(--ink-soft);
  margin: 0;
}

.reset-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.form-label {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--ink-secondary);
}

.label-icon {
  color: var(--ember-core);
}

.form-input {
  width: 100%;
  height: 3.25rem;
  padding: 0 var(--space-md);
  background: white;
  border: 2px solid rgba(232, 93, 4, 0.1);
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-family: inherit;
  transition: all 0.3s var(--ease-smooth);
  outline: none;
  color: var(--ink-primary);
}

.form-input:focus {
  border-color: var(--ember-core);
  box-shadow: 0 0 0 4px rgba(232, 93, 4, 0.1);
}

.form-input::placeholder {
  color: var(--slate-pale);
}

.password-wrapper {
  position: relative;
}

.password-wrapper .form-input {
  padding-right: 3rem;
}

.password-toggle {
  position: absolute;
  right: var(--space-md);
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--ink-soft);
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  transition: color 0.3s var(--ease-smooth);
}

.password-toggle:hover {
  color: var(--ember-core);
}

.error-message {
  font-size: 0.85rem;
  color: var(--coral-primary);
  margin: 0;
}

.error-alert {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-md);
  font-size: 0.9rem;
  color: var(--coral-deep);
  background: linear-gradient(135deg, rgba(244, 63, 94, 0.08), rgba(253, 164, 175, 0.06));
  border: 1px solid rgba(244, 63, 94, 0.2);
  border-radius: var(--radius-md);
}

.success-alert {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-md);
  font-size: 0.9rem;
  color: var(--forest-primary);
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.08), rgba(134, 239, 172, 0.06));
  border: 1px solid rgba(34, 197, 94, 0.2);
  border-radius: var(--radius-md);
}

.submit-button {
  position: relative;
  width: 100%;
  height: 3.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-sm);
  font-size: 1rem;
  font-weight: 700;
  border-radius: var(--radius-md);
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s var(--ease-smooth);
  background: linear-gradient(135deg, var(--ember-core), var(--ember-glow));
  color: white;
  border: none;
  box-shadow: var(--shadow-md), 0 0 20px rgba(232, 93, 4, 0.2);
}

.submit-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg), 0 0 30px rgba(232, 93, 4, 0.3);
}

.submit-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.button-text {
  transition: transform 0.3s var(--ease-smooth);
}

.button-icon {
  width: 20px;
  height: 20px;
  transition: transform 0.3s var(--ease-smooth);
}

.submit-button:hover:not(:disabled) .button-text {
  transform: translateX(-8px);
}

.submit-button:hover:not(:disabled) .button-icon {
  transform: translateX(8px);
}

.back-to-login {
  margin-top: var(--space-lg);
  text-align: center;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  font-size: 0.875rem;
  color: var(--ember-core);
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s var(--ease-smooth);
}

.back-link:hover {
  color: var(--ember-glow);
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

  .right-section {
    padding: var(--space-xl);
  }
}

@media (max-width: 480px) {
  .right-section {
    padding: var(--space-lg);
  }

  .form-title {
    font-size: 1.75rem;
  }
}
</style>
