<template>
  <header class="header">
    <div class="header-left">
      <div class="logo">
        <span class="logo-icon">🤖</span>
        <span class="logo-text">{{ isEnglish ? 'AI Agent Hub' : 'AI智能助手' }}</span>
      </div>
    </div>

    <div class="header-center">
      <div class="mode-switch">
        <button 
          :class="['mode-btn', { active: currentMode === 'group' }]"
          @click="switchMode('group')"
        >
          <span class="btn-icon">👥</span>
          <span class="btn-text">{{ isEnglish ? 'Group Mode' : '群组模式' }}</span>
        </button>
      </div>
    </div>

    <div class="header-right">
      <button class="lang-switch" @click="toggleLanguage">
        {{ isEnglish ? '中' : 'EN' }}
      </button>
      
      <el-dropdown @command="handleCommand">
        <div class="user-info">
          <img 
            :src="userInfo?.avatar || 'https://i.pravatar.cc/40'" 
            alt="User Avatar" 
            class="avatar"
          />
          <span class="username">{{ userInfo?.username || (isEnglish ? 'User' : '用户') }}</span>
          <span class="arrow-icon">▼</span>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="profile">{{ isEnglish ? 'Profile' : '个人信息' }}</el-dropdown-item>
            <el-dropdown-item command="settings">{{ isEnglish ? 'Settings' : '设置' }}</el-dropdown-item>
            <el-dropdown-item divided command="logout">{{ isEnglish ? 'Logout' : '退出登录' }}</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const currentMode = ref('chatflow')
const isEnglish = ref(false)

const userInfo = ref(null)

onMounted(() => {
  const userInfoStr = localStorage.getItem('userInfo')
  if (userInfoStr) {
    userInfo.value = JSON.parse(userInfoStr)
  }
  
  const path = window.location.pathname
  if (path === '/group') {
    currentMode.value = 'group'
  } else if (path === '/chatflow') {
    currentMode.value = 'chatflow'
  }
  
  const lang = localStorage.getItem('language')
  isEnglish.value = lang === 'en'
})

const switchMode = (mode) => {
  if (currentMode.value === mode) return
  currentMode.value = mode
  if (mode === 'chatflow') {
    window.location.href = '/chatflow'
  } else {
    window.location.href = '/group'
  }
}

const toggleLanguage = () => {
  isEnglish.value = !isEnglish.value
  localStorage.setItem('language', isEnglish.value ? 'en' : 'zh')
  ElMessage.success(isEnglish.value ? 'Switched to English' : '已切换为中文')
}

const handleCommand = (command) => {
  switch(command) {
    case 'profile':
      ElMessage.info(isEnglish ? 'Profile feature coming soon...' : '个人信息功能开发中...')
      break
    case 'settings':
      ElMessage.info(isEnglish ? 'Settings feature coming soon...' : '设置功能开发中...')
      break
    case 'logout':
      ElMessageBox.confirm(
        isEnglish ? 'Are you sure you want to logout?' : '确定要退出登录吗？', 
        isEnglish ? 'Logout' : '退出登录', 
        {
          confirmButtonText: isEnglish ? 'Confirm' : '确定',
          cancelButtonText: isEnglish ? 'Cancel' : '取消',
          type: 'warning'
        }
      ).then(() => {
        localStorage.removeItem('userToken')
        localStorage.removeItem('userInfo')
        ElMessage.success(isEnglish ? 'Logged out successfully' : '已退出登录')
        window.location.href = '/login'
      }).catch(() => {})
      break
  }
}
</script>

<style scoped>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-left {
  flex: 1;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-icon {
  font-size: 26px;
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
  color: white;
}

.header-center {
  flex: 2;
  display: flex;
  justify-content: center;
}

.mode-switch {
  display: flex;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  padding: 4px;
}

.mode-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 28px;
  border-radius: 16px;
  font-size: 14px;
  font-weight: 500;
  border: none;
  background: transparent;
  color: rgba(255, 255, 255, 0.9);
  cursor: pointer;
  transition: all 0.3s ease;
}

.mode-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.mode-btn.active {
  background: white;
  color: #667eea;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.btn-icon {
  font-size: 16px;
}

.btn-text {
  display: inline-block;
}

.header-right {
  flex: 1;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 16px;
}

.lang-switch {
  padding: 8px 16px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.lang-switch:hover {
  background: rgba(255, 255, 255, 0.3);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  cursor: pointer;
  border-radius: 20px;
  transition: background 0.3s ease;
}

.user-info:hover {
  background: rgba(255, 255, 255, 0.2);
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.5);
}

.username {
  font-size: 14px;
  font-weight: 500;
  color: white;
}

.arrow-icon {
  font-size: 10px;
  color: rgba(255, 255, 255, 0.8);
}
</style>