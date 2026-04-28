<template>
  <div class="login-container">
    <div class="login-bg"></div>
    
    <div class="login-wrapper">
      <div class="login-box">
        <div class="login-header">
          <div class="logo">
            <el-icon class="logo-icon" size="48">robot</el-icon>
          </div>
          <h1 class="title">AI Agent Hub</h1>
          <p class="subtitle">智能对话助手平台</p>
        </div>

        <div class="login-form">
          <div class="form-header">
            <span 
              :class="['tab', { active: authMode === 'login' }]" 
              @click="setAuthMode('login')"
            >登录</span>
            <span 
              :class="['tab', { active: authMode === 'register' }]" 
              @click="setAuthMode('register')"
            >注册</span>
          </div>

          <div class="form-body">
            <div class="input-group">
              <el-icon class="input-icon">user</el-icon>
              <el-input 
                v-model="loginForm.username" 
                placeholder="请输入用户名" 
                class="custom-input"
                :prefix-icon="User"
              />
            </div>

            <div class="input-group">
              <el-icon class="input-icon">lock</el-icon>
              <el-input 
                v-model="loginForm.password" 
                placeholder="请输入密码" 
                show-password 
                class="custom-input"
                :prefix-icon="Lock"
              />
            </div>

            <div v-if="authMode === 'register'" class="input-group">
              <el-icon class="input-icon">lock</el-icon>
              <el-input 
                v-model="loginForm.confirmPassword" 
                placeholder="请确认密码" 
                show-password 
                class="custom-input"
                :prefix-icon="Lock"
              />
            </div>

            <div class="error-message" v-if="loginError">{{ loginError }}</div>

            <el-button 
              type="primary" 
              :loading="isLoading" 
              class="submit-btn"
              @click="handleSubmit"
            >
              {{ authMode === 'login' ? '登 录' : '注 册' }}
            </el-button>
          </div>

          <div class="form-footer">
            <div class="social-login">
              <span class="social-title">或使用以下方式登录</span>
              <div class="social-buttons">
                <el-button class="social-btn" icon="el-icon-user" @click="quickLogin('admin')">
                  管理员
                </el-button>
                <el-button class="social-btn" icon="el-icon-user" @click="quickLogin('user')">
                  普通用户
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="login-decoration">
        <div class="floating-circle circle-1"></div>
        <div class="floating-circle circle-2"></div>
        <div class="floating-circle circle-3"></div>
        <div class="floating-circle circle-4"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { User, Lock } from '@element-plus/icons-vue'
import { login, sign } from '../services/chatApi'
import { useChatStore } from '../stores/chatStore'

const chatStore = useChatStore()

const authMode = ref('login')
const isLoading = ref(false)
const loginError = ref('')

const loginForm = reactive({
  username: '',
  password: '',
  confirmPassword: ''
})

const setAuthMode = (mode) => {
  authMode.value = mode
  loginError.value = ''
  loginForm.confirmPassword = ''
}

const handleSubmit = async () => {
  if (!loginForm.username || !loginForm.password) {
    loginError.value = '用户名或密码不能为空'
    return
  }

  if (authMode.value === 'register') {
    if (loginForm.password !== loginForm.confirmPassword) {
      loginError.value = '两次输入的密码不一致'
      return
    }
  }

  isLoading.value = true
  loginError.value = ''

  try {
    const result = authMode.value === 'login' 
      ? await login(loginForm) 
      : await sign(loginForm)

    if (result?.success) {
      if (authMode.value === 'login') {
        ElMessage.success('登录成功')
        chatStore.initData()
        setTimeout(() => {
          window.location.href = '/chatflow'
        }, 1000)
      } else {
        ElMessage.success('注册成功，请登录')
        setAuthMode('login')
      }
    } else {
      loginError.value = result?.message || (authMode.value === 'login' ? '登录失败' : '注册失败')
    }
  } catch (error) {
    loginError.value = '网络异常，请稍后重试'
  } finally {
    isLoading.value = false
  }
}

const quickLogin = (type) => {
  if (type === 'admin') {
    loginForm.username = 'admin'
    loginForm.password = 'admin123'
  } else {
    loginForm.username = 'user'
    loginForm.password = 'user123'
  }
  handleSubmit()
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(255, 255, 255, 0.05) 0%, transparent 70%);
}

.login-wrapper {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 420px;
  padding: 20px;
}

.login-box {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  padding: 48px 40px;
  box-shadow: 
    0 20px 60px rgba(0, 0, 0, 0.15),
    0 10px 20px rgba(0, 0, 0, 0.1);
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo {
  margin-bottom: 16px;
}

.logo-icon {
  color: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  filter: drop-shadow(0 4px 8px rgba(102, 126, 234, 0.4));
}

.title {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a2e;
  margin: 0 0 8px 0;
  letter-spacing: -0.5px;
}

.subtitle {
  font-size: 14px;
  color: #888;
  margin: 0;
}

.login-form {
  display: flex;
  flex-direction: column;
}

.form-header {
  display: flex;
  margin-bottom: 32px;
  border-bottom: 2px solid #f0f0f0;
}

.tab {
  flex: 1;
  text-align: center;
  padding: 12px;
  font-size: 16px;
  font-weight: 500;
  color: #666;
  cursor: pointer;
  position: relative;
  transition: color 0.3s ease;
}

.tab:hover {
  color: #667eea;
}

.tab.active {
  color: #667eea;
}

.tab.active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 2px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 1px;
}

.form-body {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-group {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
  font-size: 16px;
  z-index: 1;
}

.custom-input {
  width: 100%;
  height: 48px;
  padding: 0 16px 0 48px;
  border: 2px solid #e8e8e8;
  border-radius: 12px;
  font-size: 14px;
  transition: all 0.3s ease;
}

.custom-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.custom-input::placeholder {
  color: #bbb;
}

.error-message {
  color: #f56c6c;
  font-size: 13px;
  text-align: center;
  min-height: 18px;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.submit-btn {
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  transition: all 0.3s ease;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.form-footer {
  margin-top: 32px;
}

.social-login {
  text-align: center;
}

.social-title {
  font-size: 13px;
  color: #999;
  margin-bottom: 16px;
  display: block;
}

.social-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.social-btn {
  padding: 10px 24px;
  border-radius: 20px;
  font-size: 14px;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  color: #666;
  transition: all 0.3s ease;
}

.social-btn:hover {
  background: #e8e8e8;
  border-color: #667eea;
  color: #667eea;
}

.login-decoration {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  overflow: hidden;
}

.floating-circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.08);
  animation: float 6s ease-in-out infinite;
}

.circle-1 {
  width: 120px;
  height: 120px;
  top: 10%;
  right: 5%;
  animation-delay: 0s;
}

.circle-2 {
  width: 80px;
  height: 80px;
  bottom: 20%;
  left: 10%;
  animation-delay: 2s;
}

.circle-3 {
  width: 60px;
  height: 60px;
  top: 50%;
  left: 5%;
  animation-delay: 4s;
}

.circle-4 {
  width: 100px;
  height: 100px;
  bottom: 10%;
  right: 15%;
  animation-delay: 1s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}

@media (max-width: 480px) {
  .login-box {
    padding: 32px 24px;
    margin: 16px;
  }

  .title {
    font-size: 24px;
  }
}
</style>