<template>
  <div class="chat-window">
    <!-- 聊天消息列表 -->
    <div class="messages-container" ref="messagesContainer">
      <div v-if="messages.length === 0" class="welcome-section">
        <div class="welcome-content">
          <div class="welcome-icon">🤖</div>
          <h2>股票聊天室（毕业设计）</h2>
          <p class="welcome-description">
            欢迎来到股票聊天室！这里是多角色互动平台，用户和智能分析师可以实时讨论行情、投资策略和趋势预测。
          </p>
          
          <!-- 功能介绍 -->
          <div class="features-section">
            <h3>聊天室特色</h3>
            <div class="features-grid">
              <div class="feature-item">
                <div class="feature-icon">💬</div>
                <div class="feature-text">
                  <h4>实时讨论</h4>
                  <p>多角色智能分析师与用户即时互动交流</p>
                </div>
              </div>
              <div class="feature-item">
                <div class="feature-icon">✍️</div>
                <div class="feature-text">
                  <h4>行情分析</h4>
                  <p>实时掌握股票数据和走势</p>
                </div>
              </div>
              <div class="feature-item">
                <div class="feature-icon">💻</div>
                <div class="feature-text">
                  <h4>策略建议</h4>
                  <p>多角度分析投资策略</p>
                </div>
              </div>
              <div class="feature-item">
                <div class="feature-icon">📊</div>
                <div class="feature-text">
                  <h4>趋势预测</h4>
                  <p>结合数据和模型预测潜在市场走向</p>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 试试这样问 -->
          <div class="try-questions">
            <h3>试试这样问</h3>
            <div class="question-tags">
              <span 
                v-for="question in tryQuestions" 
                :key="question"
                class="question-tag"
                @click="insertQuestion(question)"
              >
                {{ question }}
              </span>
            </div>
          </div>
          
          <!-- 使用提示 -->
          <div class="usage-tip">
            <div class="tip-icon">💡</div>
            <div class="tip-text">
              <strong>小贴士：</strong>点击我头像可以@我，让我以特定身份回复您的问题
            </div>
          </div>
        </div>
      </div>
      
      <div v-else class="messages-list">
        <div 
          v-for="message in messages" 
          :key="message.id"
          class="message-item"
          :class="{
            'user-message': message.role === 'user',
            'assistant-message': message.role === 'assistant',
            'error-message': message.isError
          }"
        >
          <!-- 用户消息 -->
          <div v-if="message.role === 'user'" class="user-message-wrapper">
            <div class="message-content">
              <div class="message-bubble user-bubble">
                {{ message.content }}
              </div>
              <div class="message-time">
                {{ formatTime(message.timestamp) }}
              </div>
            </div>
            <div class="message-avatar user-avatar">
              <el-icon size="20"><User /></el-icon>
            </div>
          </div>
          
          <!-- AI助手消息 -->
          <div v-else class="assistant-message-wrapper">
            <div 
              class="message-avatar assistant-avatar clickable-avatar" 
              :style="{ backgroundColor: getAiRole(message.role)?.color || '#409EFF' }"
              @click="mentionRole(getAiRole(message.role).id)"
              :title="`点击@${getAiRole(message.role)?.name || 'AI助手'}`"
            >
              <span v-if="getAiRole(message.role)?.avatar">{{ getAiRole(message.role).avatar }}</span>
              <el-icon v-else size="20"><Cpu /></el-icon>
            </div>
            <div class="message-content">
              <div class="message-header">
                <span class="ai-name">{{ getAiRole(message.role)?.name || '智能助手' }}</span>
                <span class="message-time">{{ formatTime(message.timestamp) }}</span>
              </div>
              <div 
                class="message-bubble assistant-bubble"
                :class="{ 
                  'streaming': message.isStreaming,
                  'error-bubble': message.isError
                }"
              >
                <div class="message-text">
                  {{ message.content }}
                  <span v-if="message.isStreaming" class="typing-cursor">|</span>
                </div>
                
                <!-- 消息操作 -->
                <div class="message-actions" v-if="!message.isStreaming && !message.isError">
                  <el-button size="small" text @click="copyMessage(message.content)">
                    <el-icon><CopyDocument /></el-icon>
                  </el-button>
                  <el-button size="small" text @click="regenerateMessage(message.id)">
                    <el-icon><Refresh /></el-icon>
                  </el-button>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 加载指示器 -->
        <div v-if="isLoading" class="loading-message">
          <div class="message-avatar assistant-avatar">
            <el-icon size="20"><Cpu /></el-icon>
          </div>
          <div class="message-content">
            <div class="message-bubble assistant-bubble">
              <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { User, Cpu, CopyDocument, Refresh } from '@element-plus/icons-vue'
import { useChatStore } from '../stores/chatStore'
const chatStore = useChatStore()
// 从 store 获取 aiRoles
const props = defineProps({
  messages: {
    type: Array,
    default: () => []
  },
  isLoading: {
    type: Boolean,
    default: false
  },
  aiRoles: {
    type: Array,
    default: () => []
  }
})
const getAiRole = (roleId) => {
  return chatStore.aiRoles.find(role => role.id === roleId) || null
}
const emit = defineEmits(['regenerate-message', 'mention-role', 'insert-question'])

const messagesContainer = ref(null)

// 试试这样问的问题列表
const tryQuestions = ref([
  '分析一下特斯拉(TSLA)未来一周的股票走势',
  '推荐几只近期潜力股',
  '预测下周大盘指数的趋势',
  '科技板块哪只股票值得关注？',
  '分析苹果(AAPL)的财报对股价的影响',
  '提供当前热门股票的投资策略',
  '对冲基金常用的股票配置方法是什么？',
  '短期和长期投资策略如何选择？'
])

// 监听消息变化，自动滚动到底部
watch(() => props.messages, async () => {
  await nextTick()
  scrollToBottom()
}, { deep: true })

watch(() => props.isLoading, async (newVal) => {
  if (newVal) {
    await nextTick()
    scrollToBottom()
  }
})

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const insertQuestion = (question) => {
  emit('insert-question', question)
}

const copyMessage = async (content) => {
  try {
    await navigator.clipboard.writeText(content)
    ElMessage.success('已复制到剪贴板')
  } catch (error) {
    ElMessage.error('复制失败')
  }
}

const regenerateMessage = (messageId) => {
  emit('regenerate-message', messageId)
}

const mentionRole = (role) => {
  console.log(role)
  if (role) {
    emit('mention-role', role)
  }
}

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) { // 1分钟内
    return '刚刚'
  } else if (diff < 3600000) { // 1小时内
    return `${Math.floor(diff / 60000)}分钟前`
  } else if (diff < 86400000) { // 24小时内
    return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  } else {
    return date.toLocaleString('zh-CN', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
  }
}
</script>

<style scoped>
.chat-window {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #ffffff;
  overflow: hidden;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.messages-container::-webkit-scrollbar {
  width: 6px;
}

.messages-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.messages-container::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.messages-container::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

.welcome-section {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  min-height: 400px;
}

.welcome-content {
  text-align: center;
  max-width: 600px;
  padding: 40px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.welcome-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.welcome-content h2 {
  color: #333;
  margin-bottom: 12px;
  font-size: 28px;
  font-weight: 600;
}

.welcome-content p {
  color: #666;
  margin-bottom: 30px;
  font-size: 16px;
}

.welcome-description {
  color: #666;
  margin-bottom: 30px;
  font-size: 16px;
  line-height: 1.6;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.features-section {
  margin: 30px 0;
}

.features-section h3 {
  color: #333;
  margin-bottom: 20px;
  font-size: 20px;
  font-weight: 600;
  text-align: center;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
  margin-bottom: 30px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: white;
  border-radius: 12px;
  border: 1px solid #e4e7ed;
  transition: all 0.3s ease;
}

.feature-item:hover {
  border-color: #409EFF;
  box-shadow: 0 2px 12px rgba(64, 158, 255, 0.1);
}

.feature-icon {
  font-size: 24px;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  border-radius: 12px;
  flex-shrink: 0;
}

.feature-text h4 {
  margin: 0 0 4px;
  color: #333;
  font-size: 14px;
  font-weight: 600;
}

.feature-text p {
  margin: 0;
  color: #666;
  font-size: 13px;
  line-height: 1.4;
}

.try-questions {
  margin: 30px 0;
}

.try-questions h3 {
  color: #333;
  margin-bottom: 16px;
  font-size: 20px;
  font-weight: 600;
  text-align: center;
}

.question-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  max-width: 700px;
  margin: 0 auto;
}

.question-tag {
  padding: 8px 16px;
  background: #f5f7fa;
  border: 1px solid #e4e7ed;
  border-radius: 20px;
  font-size: 14px;
  color: #666;
  cursor: pointer;
  transition: all 0.2s ease;
}

.question-tag:hover {
  background: #e6f7ff;
  border-color: #91d5ff;
  color: #409EFF;
  transform: translateY(-1px);
}

.usage-tip {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: linear-gradient(135deg, #fff7e6 0%, #fff2cc 100%);
  border: 1px solid #ffd591;
  border-radius: 12px;
  margin-top: 30px;
}

.tip-icon {
  font-size: 20px;
  flex-shrink: 0;
}

.tip-text {
  color: #d46b08;
  font-size: 14px;
  line-height: 1.5;
}

.messages-list {
  max-width: 800px;
  margin: 0 auto;
}

.message-item {
  margin-bottom: 24px;
}

.user-message-wrapper {
  display: flex;
  justify-content: flex-end;
  align-items: flex-start;
  gap: 12px;
}

.assistant-message-wrapper {
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 12px;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 18px;
}

.user-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.assistant-avatar {
  color: white;
  font-size: 20px;
}

.clickable-avatar {
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.clickable-avatar:hover {
  transform: scale(1.1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.clickable-avatar:hover::after {
  content: '@';
  position: absolute;
  top: -5px;
  right: -5px;
  background: #409EFF;
  color: white;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  font-size: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.message-content {
  max-width: 70%;
  min-width: 200px;
}

.message-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.ai-name {
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.message-time {
  font-size: 12px;
  color: #999;
}

.message-bubble {
  padding: 16px 20px;
  border-radius: 20px;
  position: relative;
  word-wrap: break-word;
  line-height: 1.5;
}

.user-bubble {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-bottom-right-radius: 6px;
}

.assistant-bubble {
  background: white;
  color: #333;
  border: 1px solid #e4e7ed;
  border-bottom-left-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.error-bubble {
  background: #fef0f0;
  border-color: #fbc4c4;
  color: #f56c6c;
}

.message-text {
  position: relative;
}

.typing-cursor {
  animation: blink 1s infinite;
  color: #409EFF;
  font-weight: bold;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

.message-actions {
  position: absolute;
  top: 8px;
  right: 8px;
  opacity: 0;
  transition: opacity 0.2s ease;
  display: flex;
  gap: 4px;
}

.assistant-bubble:hover .message-actions {
  opacity: 1;
}

.loading-message {
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 12px;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 16px 20px;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #409EFF;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) {
  animation-delay: -0.32s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes typing {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}
</style>
