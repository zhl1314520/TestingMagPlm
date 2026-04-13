<template>
  <div class="forgot-password-page noise-texture">
    <div class="left-section">
      <div class="logo-section">
        <div class="logo-link" @click="refreshAnimation" style="cursor: pointer;">
          <div class="logo-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 2L2 7L12 12L22 7L12 2Z"/>
              <path d="M2 17L12 22L22 17"/>
              <path d="M2 12L12 17L22 12"/>
            </svg>
          </div>
          <span>HBNU-TMP</span>
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
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
            </svg>
            Password Recovery
          </div>
          <h1 class="form-title">忘记密码</h1>
          <p class="form-subtitle">请输入您的邮箱地址以重置密码</p>
        </div>

        <form @submit.prevent="handleSubmit" class="reset-form">
          <div class="form-group">
            <label for="email" class="form-label">
              <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                <polyline points="22,6 12,13 2,6"/>
              </svg>
              邮箱地址
            </label>
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

          <div class="form-group">
            <label for="code" class="form-label">
              <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
              </svg>
              验证码
            </label>
            <div class="code-wrapper">
              <input
                id="code"
                v-model="code"
                type="text"
                placeholder="请输入验证码"
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
                {{ countdown > 0 ? `${countdown}s` : '获取验证码' }}
              </button>
            </div>
            <p v-if="errors.code" class="error-message">{{ errors.code }}</p>
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
            <span class="button-text">{{ isLoading ? '验证中...' : '验证并继续' }}</span>
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
import { useRouter } from 'vue-router'
import AnimatedCharacters from './AnimatedCharacters.vue'
import { authAPI } from '../api/index.js'

const router = useRouter()

const email = ref('')
const code = ref('')
const isTyping = ref(false)
const isLoading = ref(false)
const isSending = ref(false)
const countdown = ref(0)
const success = ref(false)
const animationKey = ref(0)

const refreshAnimation = () => {
  animationKey.value++
}

const errorMessage = ref('')
const successMessage = ref('')
const errors = ref({
  email: '',
  code: ''
})

const validateForm = () => {
  errors.value = { email: '', code: '' }
  let isValid = true

  if (!email.value) {
    errors.value.email = '请输入邮箱地址'
    isValid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    errors.value.email = '请输入有效的邮箱地址'
    isValid = false
  }

  if (!code.value) {
    errors.value.code = '请输入验证码'
    isValid = false
  } else if (code.value.length < 4) {
    errors.value.code = '验证码至少为 4 位'
    isValid = false
  }

  return isValid
}

const handleSendCode = async () => {
  if (!email.value) {
    errors.value.email = '请输入邮箱地址'
    return
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    errors.value.email = '请输入有效的邮箱地址'
    return
  }

  errors.value.email = ''
  isSending.value = true
  errorMessage.value = ''

  try {
    await authAPI.sendResetCode(email.value)
    
    successMessage.value = '验证码已发送到您的邮箱！'
    
    countdown.value = 60
    const timer = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0) {
        clearInterval(timer)
      }
    }, 1000)
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || '发送验证码失败，请重试。'
  } finally {
    isSending.value = false
  }
}

const handleSubmit = async () => {
  if (!validateForm()) return

  isLoading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    await authAPI.verifyResetCode(email.value, code.value)
    
    success.value = true
    successMessage.value = '验证成功！正在跳转...'
    
    localStorage.setItem('reset_email', email.value)
    localStorage.setItem('reset_code', code.value)
    
    setTimeout(() => {
      router.push({
        path: '/reset-password',
        query: { email: email.value, code: code.value }
      })
    }, 1000)
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || '验证码无效，请重试。'
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

.code-wrapper {
  display: flex;
  gap: var(--space-sm);
}

.code-input {
  flex: 1;
}

.send-code-btn {
  height: 3.25rem;
  padding: 0 var(--space-md);
  background: white;
  border: 2px solid rgba(232, 93, 4, 0.1);
  border-radius: var(--radius-md);
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--ember-core);
  cursor: pointer;
  transition: all 0.3s var(--ease-smooth);
  white-space: nowrap;
}

.send-code-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, rgba(232, 93, 4, 0.04), rgba(250, 163, 7, 0.02));
  border-color: var(--ember-core);
}

.send-code-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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
  .forgot-password-page {
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

  .code-wrapper {
    flex-direction: column;
  }

  .send-code-btn {
    width: 100%;
  }
}
</style>
