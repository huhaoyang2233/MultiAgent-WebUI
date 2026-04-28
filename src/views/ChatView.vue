<template>
  <div class="chat-container">
    <Header />
    
    <div class="chat-main-content">
      <Sidebar 
        :collapsed="sidebarCollapsed"
        @toggle="toggleSidebar"
        @new-chat="createNewChat"
        @select-chat="selectChat"
        :current-chat-id="currentChatId"
        :chat-history="chatHistory"
      />
      
      <div class="chat-main">
        <ChatWindow 
          :messages="currentMessages"
          :is-loading="isLoading"
          :ai-roles="aiRoles"
          @mention-role="handleMentionRole"
          @insert-question="handleInsertQuestion"
        />
        
        <InputArea 
          v-model="userInput"
          :disabled="isLoading"
          :mention-mode="mentionMode"
          :mentioned-role="mentionedRole"
          @send="sendMessage"
          @mention-role="handleMentionRole"
          @keydown.enter="sendMessage"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, toRaw } from 'vue'
import { storeToRefs } from 'pinia'
import { useChatStore } from '../stores/chatStore'
import { streamChat } from '../services/chatApi'
import Sidebar from '../components/Sidebar.vue'
import ChatWindow from '../components/ChatWindow.vue'
import InputArea from '../components/InputArea.vue'
import Header from '../components/Header.vue'

const chatStore = useChatStore()

const userInput = ref('')
const isLoading = ref(false)
const sidebarCollapsed = ref(false)

const { currentChatId, chatHistory, currentMessages, aiRoles, mentionMode, mentionedRole } = storeToRefs(chatStore)

const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

const createNewChat = () => {
  chatStore.createNewChat()
}

const selectChat = (chatId) => {
  chatStore.selectChat(chatId)
}

const sendMessage = async (userMessage) => {
  if (!userInput.value.trim() || isLoading.value) return
  
  let message = userInput.value.trim()
  userInput.value = ''
  
  let aiRole
  let target_role = ""
  if (mentionMode.value && mentionedRole.value) {
    aiRole = mentionedRole.value
    target_role = mentionedRole.value.name
  } else {
    aiRole = aiRoles.value[Math.floor(Math.random() * aiRoles.value.length)]
  }
  
  chatStore.addMessage({
    id: Date.now(),
    role: 'user',
    content: message,
    target_role: target_role,
    timestamp: new Date()
  })
  
  isLoading.value = true
  
  try {
    await handleStreamingResponse(message, target_role)
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

const handleStreamingResponse = async (userMessage, target_role) => {
  let aiRole
  if (mentionMode.value && mentionedRole.value) {
    aiRole = mentionedRole.value
  } else {
    aiRole = ""
  }
  
  const messageId = currentChatId.value
  
  await streamChat(
    {
      message: userMessage,
      role: "user",
      target_role: target_role,
      chatId: messageId
    },
    (chunk) => {
      chatStore.addMessage({
        id: Date.now(),
        role: chunk.role,
        content: chunk.content,
        timestamp: new Date(),
        isStreaming: false
      })
    },
    (fullContent) => {
      chatStore.finishStreamingMessage(messageId)
    }
  )
}

const handleInsertQuestion = (question) => {
  userInput.value = question
  nextTick(() => {
    const inputElement = document.querySelector('.message-input textarea')
    if (inputElement) {
      inputElement.focus()
      const length = inputElement.value.length
      inputElement.setSelectionRange(length, length)
    }
  })
}

const handleMentionRole = (roleId) => {
  if (roleId) {
    const role = toRaw(chatStore.aiRoles).find(role => role.id === roleId) || null
    chatStore.startMention(roleId)
    if (!userInput.value.startsWith('@')) {
      userInput.value = `@${role.name} `
    }
    nextTick(() => {
      const inputElement = document.querySelector('.message-input textarea')
      if (inputElement) {
        inputElement.focus()
        const length = inputElement.value.length
        inputElement.setSelectionRange(length, length)
      }
    })
  } else {
    chatStore.cancelMention()
  }
}

onMounted(() => {
  if (chatHistory.value.length === 0) {
    chatStore.initUserChats()
    createNewChat()
  }
})
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f5f5f5;
}

.chat-main-content {
  flex: 1;
  display: flex;
  overflow: hidden;
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
</style>