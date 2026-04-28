<template>
  <div class="chat-container">
    <!-- 左侧边栏 -->
    <Sidebar 
      :collapsed="sidebarCollapsed"
      @toggle="toggleSidebar"
      @new-chat="createNewChat"
      @select-chat="selectChat"
      :current-chat-id="currentChatId"
      :chat-history="chatHistory"
      @open-login="openLoginDialog"
    />
    
    <!-- 右侧聊天区域 -->
    <div class="chat-main">
      <!-- 聊天窗口 -->
      <ChatWindow 
        :messages="currentMessages"
        :is-loading="isLoading"
        :ai-roles="aiRoles"
        @mention-role="handleMentionRole"
        @insert-question="handleInsertQuestion"
      />
      
      <!-- 输入区域 -->
      <InputArea 
        v-model="userInput"
        :disabled="isLoading"
        :mention-mode="mentionMode"
        :mentioned-role="mentionedRole"
        @send="sendMessage"
        @mention-role="handleMentionRole"
        @keydown.enter="sendMessage"
      />
      <!-- 登录弹窗放在主页面，居中显示 -->
      <!-- 弹窗部分 -->
      <el-dialog
        :title="dialogTitle"
        v-model="loginDialogVisible"
        width="420px"
        :close-on-click-modal="false"
        class="auth-dialog"
        :before-close="handleBeforeClose"
      >
        <div class="login-form">
          <el-input 
            v-model="loginForm.username" 
            placeholder="用户名" 
            class="auth-input"
            prefix-icon="el-icon-user"
          />
          <el-input 
            v-model="loginForm.password" 
            placeholder="密码" 
            show-password 
            class="auth-input"
            prefix-icon="el-icon-lock"
          />
          <p class="login-error">{{ loginError }}</p>
        </div>

        <template #footer>
          <div class="auth-footer">
            <el-button @click="handleBeforeClose" plain>
              {{ authMode === 'switch' ? '取消切换' : '取消' }}
            </el-button>

            <el-button 
              type="primary" 
              :loading="loginLoading" 
              v-if="authMode === 'login' || authMode === 'switch'" 
              @click="handleLogin"
            >
              {{ authMode === 'switch' ? '切换用户登录' : '登录' }}
            </el-button>

            <el-button 
              type="success" 
              :loading="registerLoading" 
              v-if="authMode === 'register'" 
              @click="handleRegister"
            >注册</el-button>

            <span class="toggle-auth" @click="toggleAuthMode" v-if="authMode !== 'switch'">
              {{ authMode === 'login' ? '没有账号？去注册' : '已有账号？去登录' }}
            </span>
          </div>
        </template>
      </el-dialog>


    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick,toRaw} from 'vue'
import { storeToRefs } from 'pinia'
import { useChatStore} from '../stores/chatStore'
// import { simulateStreamingResponse } from '../services/chatApi'
import {streamChat,login,sign} from '../services/chatApi'
import Sidebar from '../components/Sidebar.vue'
import ChatWindow from '../components/ChatWindow.vue'
import InputArea from '../components/InputArea.vue'


const chatStore = useChatStore()
 


// 响应式数据

const userInput = ref('')
const isLoading = ref(false)
let currentMentionRole = null

// 从store获取数据
const { currentChatId, chatHistory, currentMessages, aiRoles, mentionMode, mentionedRole } = storeToRefs(chatStore)

// 折叠侧边栏
const sidebarCollapsed = ref(false)
const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}
//创建新的聊天
const createNewChat = () => {
  chatStore.createNewChat()
}
// 选择聊天
const selectChat = (chatId) => {
  chatStore.selectChat(chatId)
}


// 弹窗控制
const loginDialogVisible = ref(false)
const authMode = ref('login') // login / register / switch
const dialogTitle = ref('用户登录')

const loginLoading = ref(false)
const registerLoading = ref(false)
const loginError = ref('')

const loginForm = reactive({
  username: '',
  password: ''
})

// 打开弹窗
const openLoginDialog = () => {
  const token = localStorage.getItem("userToken")
  const userInfoStr = localStorage.getItem("userInfo")

  if (token && userInfoStr) {
    authMode.value = 'switch'
    const userInfo = JSON.parse(userInfoStr)
    loginForm.username = userInfo.username || ''
    loginForm.password = ''
    dialogTitle.value = '切换用户登录'
  } else {
    authMode.value = 'login'
    loginForm.username = ''
    loginForm.password = ''
    dialogTitle.value = '用户登录'
  }
  loginError.value = ''
  loginDialogVisible.value = true
}


//不登陆无法使用
const handleBeforeClose = () => {
  const token = localStorage.getItem("userToken")
  if (!token) {
    ElMessage.warning("请先登录")
    // 不关闭弹窗
    return
  }
  // 已登录才允许关闭
  loginDialogVisible.value = false
}

// 切换模式
const toggleAuthMode = () => {
  authMode.value = authMode.value === 'login' ? 'register' : 'login'
  loginError.value = ''
}

// 登录
const handleLogin = async () => {
  if (!loginForm.username || !loginForm.password) {
    loginError.value = '用户名或密码不能为空'
    return
  }
  loginLoading.value = true
  loginError.value = ''
  const result = await login(loginForm)
  loginLoading.value = false

  if (result?.success) {
    ElMessage.success('登录成功')
    loginDialogVisible.value = false
    loginForm.username = ''
    loginForm.password = ''
    // 刷新页面
    window.location.reload()
    chatStore.initUserChats()
  } else {
    loginError.value = result?.message || '登录失败'
  }
}

// 注册
const handleRegister = async () => {
  if (!loginForm.username || !loginForm.password) {
    loginError.value = '用户名或密码不能为空'
    return
  }
  registerLoading.value = true
  loginError.value = ''
  const result = await sign(loginForm)
  registerLoading.value = false

  if (result?.success) {
    ElMessage.success('注册成功，请登录')
    toggleAuthMode()
  } else {
    loginError.value = result?.message || '注册失败'
  }
}

// 向Agents-flask发送信息
const sendMessage = async (userMessage) => {

  if (!userInput.value.trim() || isLoading.value) return
  
  let message = userInput.value.trim()
  userInput.value = ''
  // 处理@功能
  let aiRole
  let target_role=""
  if (mentionMode.value && mentionedRole.value) {
    aiRole = mentionedRole.value
    target_role=mentionedRole.value.name
  } else {
    aiRole = aiRoles.value[Math.floor(Math.random() * aiRoles.value.length)]
  }
  // 添加用户消息
  chatStore.addMessage({
    id: Date.now(),
    role: 'user',
    content: message,
    target_role:target_role,
    timestamp: new Date()
  })
  
  isLoading.value = true
  
  try {
    // 使用流式AI响应
    await handleStreamingResponse(message,target_role)
  } catch (error) {
    console.error('发送消息失败:', error)
    chatStore.addMessage({
      id: Date.now(),
      role: 'assistant',
      content: '抱歉，发生了错误，请稍后重试。',
      timestamp: new Date(),
      isError: true
    })
  } finally {
    isLoading.value = false
  }
}

// 使用流式API响应
const handleStreamingResponse = async (userMessage,target_role) => {
  // 如果用户@了特定角色，优先使用被@的角色
  let aiRole
  if (mentionMode.value && mentionedRole.value) {
    aiRole = mentionedRole.value
  } else {
    // aiRole = aiRoles.value[Math.floor(Math.random() * aiRoles.value.length)]
    aiRole=""
  }
  // const messageId = Date.now()
  const messageId=currentChatId.value
  
  console.log("目标角色",target_role)
    // 使用流式API服务
  await streamChat(
    {
        message: userMessage,
        role: "user",
        target_role:target_role,
        chatId: messageId
    },
    // onChunk回调
    (chunk) => {
      console.log(chunk.role)
      chatStore.addMessage({
          id: Date.now(), // 每条独立id
          role: chunk.role, // 服务端返回的角色
          content: chunk.content,
          timestamp: new Date(),
          isStreaming: false
        })
        console.log("下一个角色")
    },
    // onComplete回调
    (fullContent) => {
      chatStore.finishStreamingMessage(messageId)
    }
  )
  
  // 使用模拟流式API服务
//   await simulateStreamingResponse(
//     userMessage,
//     aiRole,
//     // onChunk回调
//     (chunk) => {
//       if (chunk.type === 'content') {
//         chatStore.updateStreamingMessage(messageId, chunk.fullContent)
//       } else if (chunk.type === 'role_info') {
//         // 更新消息的角色信息
//         chatStore.updateMessageRole(messageId, chunk)
//       }
//     },
//     // onComplete回调
//     (fullContent) => {
//       chatStore.finishStreamingMessage(messageId)
//     }
//   )
}

const handleInsertQuestion = (question) => {
  userInput.value = question
  // 聚焦到输入框
  nextTick(() => {
    const inputElement = document.querySelector('.message-input textarea')
    if (inputElement) {
      inputElement.focus()
      const length = inputElement.value.length
      inputElement.setSelectionRange(length, length)
    }
  })
}

//处理用户的@事件
const handleMentionRole = (roleId) => {
  
  if (roleId) {
    // role=chatStore.aiRoles.find(role => role.id === roleId).name
    const role=toRaw(chatStore.aiRoles).find(role => role.id === roleId) || null
    chatStore.startMention(roleId)
    // 自动在输入框中添加@前缀
    if (!userInput.value.startsWith('@')) {
      userInput.value = `@${role.name} `
    }
    // 聚焦到输入框
    nextTick(() => {
      const inputElement = document.querySelector('.message-input textarea')
      if (inputElement) {
        inputElement.focus()
        // 将光标移到输入框末尾
        const length = inputElement.value.length
        inputElement.setSelectionRange(length, length)
      }
    })
  } else {
    chatStore.cancelMention()
  }
}

onMounted(() => {
  //判断是否有登录
  const token = localStorage.getItem("userToken")
  if (!token) {
    loginDialogVisible.value = true  // 自动弹出登录框
  }
  // 初始化聊天
  if (chatHistory.value.length === 0) {
    const userToken = localStorage.getItem("userToken")
    const userInfo = localStorage.getItem("userInfo")
    chatStore.initUserChats()
    createNewChat()
  }
})
</script>

<style scoped>
.chat-container {
  display: flex;
  height: 100vh;
  background-color: #f5f5f5;
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  margin-left: 0;
  transition: margin-left 0.3s ease;
}

.chat-main.sidebar-collapsed {
  margin-left: 0;
}
.auth-dialog .el-dialog__header {
  font-size: 20px;
  font-weight: 600;
  text-align: center;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 10px;
}

.auth-input {
  width: 100%;
}

.login-error {
  color: #f56c6c;
  font-size: 13px;
  text-align: center;
  margin-top: -8px;
  min-height: 18px;
}

.auth-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

.auth-footer .el-button {
  min-width: 80px;
}

.toggle-auth {
  font-size: 13px;
  color: #409eff;
  cursor: pointer;
  user-select: none;
}

.toggle-auth:hover {
  text-decoration: underline;
}
</style>
