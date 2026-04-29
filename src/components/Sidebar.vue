<template>
  <div class="sidebar" :class="{ collapsed: collapsed }">
    <!-- 头部 -->
    <div class="sidebar-header">
      <div class="logo" v-show="!collapsed">
        <el-icon size="24" color="#409EFF"><ChatDotRound /></el-icon>
        <span>智能多AGENT股票推荐聊天室</span>
      </div>
      <el-button 
        :icon="collapsed ? Expand : Fold" 
        @click="$emit('toggle')"
        circle
        size="small"
        class="toggle-btn"
      />
    </div>

    <!-- 新建对话按钮 -->
    <div class="new-chat-section">
      <el-button 
        type="primary" 
        @click="$emit('new-chat')"
        :class="{ 'collapsed-btn': collapsed }"
        class="new-chat-btn"
      >
        <el-icon v-if="!collapsed"><Plus /></el-icon>
        <el-icon v-else><Edit /></el-icon>
        <span v-if="!collapsed">新建对话</span>
      </el-button>
    </div>

    <!-- 历史对话列表 -->
    <div class="chat-history">
      <div class="section-title" v-show="!collapsed">
        <el-icon><Clock /></el-icon>
        <span>历史记录</span>
      </div>
      
      <div class="chat-list">
        <div 
          v-for="chat in sortedChatHistory" 
          :key="chat.id"
          class="chat-item"
          :class="{ active: currentChatId === chat.id, collapsed: collapsed }"
          @click="$emit('select-chat', chat.id)"
        >
          <div class="chat-content">
            <div class="chat-title" v-show="!collapsed">{{ chat.title }}</div>
            <div class="chat-meta" v-show="!collapsed">
              <span class="message-count">{{ chat.messageCount }} 条消息</span>
              <span class="update-time">{{ formatTime(chat.updatedAt) }}</span>
            </div>
            <div class="chat-icon" v-show="collapsed">
              <el-icon><ChatDotRound /></el-icon>
            </div>
          </div>
          <div class="chat-actions" v-show="!collapsed && currentChatId === chat.id">
            <el-button :icon="Delete" size="small" text @click.stop="deleteChat(chat.id)" />
          </div>
        </div>

        <div v-if="chatHistory.length === 0" class="empty-state">
          <el-icon size="48" color="#C0C4CC"><ChatDotRound /></el-icon>
          <p v-show="!collapsed">暂无对话记录</p>
        </div>
      </div>
    </div>

    <!-- 底部操作 -->
    <div class="sidebar-footer" v-show="!collapsed">
      <el-dropdown @command="handleCommand">
        <el-button text>
          <el-icon><Setting /></el-icon>
          <span>设置</span>
          <el-icon class="el-icon--right"><ArrowDown /></el-icon>
        </el-button>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="clear">清空所有对话</el-dropdown-item>
            <el-dropdown-item command="export">导出对话</el-dropdown-item>
            <el-dropdown-item command="import">导入对话</el-dropdown-item>
            <el-dropdown-item command="logout">注销账户</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>

      <!-- 用户头像按钮 -->
      <el-button circle size="large" class="avatar-btn" @click="openLogin">
        <img src="https://i.pravatar.cc/40" alt="用户头像" class="avatar-img" />
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useChatStore } from '../stores/chatStore'
import { ChatDotRound, Plus, Edit, Clock, Delete, Setting, ArrowDown, Expand, Fold } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const props = defineProps({
  collapsed: { type: Boolean, default: false },
  currentChatId: { type: String, default: null },
  chatHistory: { type: Array, default: () => [] }
})

const emit = defineEmits(['toggle', 'new-chat', 'select-chat'])

const chatStore = useChatStore()

// 历史聊天排序（按更新时间降序）
const sortedChatHistory = computed(() => {
  return [...props.chatHistory].sort((a, b) => new Date(b.updatedAt || 0) - new Date(a.updatedAt || 0))
})

// 删除会话
const deleteChat = (chatId) => {
  ElMessageBox.confirm('确定要删除这个对话吗？', '确认删除', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    chatStore.deleteChat(chatId)
    ElMessage.success('删除成功')
  }).catch(() => {})
}

// 设置菜单命令处理
const handleCommand = (command) => {
  switch(command){
    case 'clear':
      ElMessageBox.confirm('确定要清空所有对话吗？此操作不可恢复！', '确认清空', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        chatStore.clearAllChats()
        ElMessage.success('已清空所有对话')
      })
      break
    case 'export':
      ElMessage.info('导出功能开发中...')
      break
    case 'import':
      ElMessage.info('导入功能开发中...')
      break
    case 'logout':
      ElMessageBox.confirm('确定要注销账户吗？', '注销账户', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        localStorage.removeItem('userToken')
        localStorage.removeItem('userInfo')
        chatStore.clearAllChats()
        ElMessage.success('已注销账户，请重新登录')
        window.location.href = '/login'
      }).catch(() => {})
      break
  }
}

// 时间格式化
const formatTime = (date) => {
  const now = new Date()
  const chatDate = new Date(date)
  const diff = now - chatDate
  if(diff < 60000) return '刚刚'
  if(diff < 3600000) return `${Math.floor(diff/60000)}分钟前`
  if(diff < 86400000) return `${Math.floor(diff/3600000)}小时前`
  if(diff < 604800000) return `${Math.floor(diff/86400000)}天前`
  return chatDate.toLocaleDateString()
}


</script>


<style scoped>
.sidebar {
  width: 400px;
  height: 100vh;
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  overflow: hidden;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
}

.sidebar.collapsed {
  width: 72px;
}

.sidebar-header {
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
  font-size: 18px;
  font-weight: 600;
}

.toggle-btn {
  background: rgba(255, 255, 255, 0.2) !important;
  border: none !important;
  color: white !important;
}

.toggle-btn:hover {
  background: rgba(255, 255, 255, 0.3) !important;
}

.new-chat-section {
  padding: 20px;
}

.new-chat-btn {
  width: 100%;
  height: 45px;
  border-radius: 12px;
  font-weight: 500;
  background: rgba(255, 255, 255, 0.9) !important;
  color: #667eea !important;
  border: none !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.new-chat-btn:hover {
  background: white !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.new-chat-btn.collapsed-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  padding: 0;
}

.chat-history {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.section-title {
  padding: 0 20px 10px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 12px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 6px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.chat-list {
  flex: 1;
  overflow-y: auto;
  padding: 0 10px;
}

.chat-list::-webkit-scrollbar {
  width: 4px;
}

.chat-list::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
}

.chat-list::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
}

.chat-item {
  margin: 4px 0;
  padding: 12px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
}

.chat-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.chat-item.active {
  background: rgba(255, 255, 255, 0.2);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.chat-item.collapsed {
  justify-content: center;
  padding: 12px;
}

.chat-content {
  flex: 1;
  min-width: 0;
}

.chat-title {
  color: white;
  font-weight: 500;
  font-size: 14px;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.chat-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 11px;
  color: rgba(255, 255, 255, 0.7);
}

.message-count {
  background: rgba(255, 255, 255, 0.2);
  padding: 2px 6px;
  border-radius: 8px;
}

.chat-icon {
  color: white;
  font-size: 18px;
}

.chat-actions {
  opacity: 0;
  transition: opacity 0.2s ease;
}

.chat-item:hover .chat-actions {
  opacity: 1;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: rgba(255, 255, 255, 0.6);
  text-align: center;
}

.empty-state p {
  margin: 12px 0 0;
  font-size: 14px;
}

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;            
  justify-content: space-between; 
  align-items: center;    
}

.footer-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.footer-btn {
  color: rgba(255, 255, 255, 0.8);
  border: none;
  background: transparent;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  border-radius: 8px;
}

.footer-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}
</style>
