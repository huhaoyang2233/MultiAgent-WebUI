<template>
  <div class="input-area">
    <div class="input-container">
      <!-- 工具栏 -->
      <div class="input-toolbar">
        <div class="toolbar-left">
          <el-button size="small" text @click="attachFile">
            <!-- <el-icon><Paperclip /></el-icon> -->
            <!-- <span>附件</span> -->
          </el-button>
        </div>
        
        <div class="toolbar-right">
          <el-button size="small" text @click="clearInput" :disabled="!modelValue.trim()">
            <el-icon><Delete /></el-icon>
          </el-button>
        </div>
      </div>
      
      <!-- @提示 -->
      <div v-if="mentionMode && mentionedRole" class="mention-indicator">
        <div class="mention-info">
          <div class="mention-avatar" :style="{ backgroundColor: mentionedRole.color }">
            {{ getAiRole(mentionedRole).avatar }}
          </div>
          <span class="mention-text">正在@{{ getAiRole(mentionedRole).name }}</span>
          <el-button size="small" text @click="cancelMention">
            <el-icon><Delete /></el-icon>
          </el-button>
        </div>
      </div>
      
      <!-- 输入框区域 -->
      <div class="input-wrapper">
        <el-input
          v-model="inputValue"
          type="textarea"
          :rows="1"
          :autosize="{ minRows: 1, maxRows: 6 }"
          :placeholder="mentionMode && mentionedRole ? `@${mentionedRole.name} ` : '输入您的问题...'"
          :disabled="disabled"
          @keydown="handleKeydown"
          @input="handleInput"
          class="message-input"
          :class="{ 'mention-input': mentionMode && mentionedRole }"
          ref="inputRef"
        />
        
        <div class="input-actions">
          <el-button 
            type="primary" 
            :disabled="!inputValue.trim() || disabled"
            @click="sendMessage"
            class="send-button"
            :loading="disabled"
          >
            <el-icon><Position /></el-icon>
            <span>发送</span>
          </el-button>
        </div>
      </div>
      
      <!-- 快捷提示 -->
      <div class="quick-prompts" v-if="!modelValue.trim()">
        <div class="prompt-title">快捷提问：</div>
        <div class="prompt-tags">
          <span 
            v-for="prompt in quickPrompts" 
            :key="prompt"
            class="prompt-tag"
            @click="insertPrompt(prompt)"
          >
            {{ prompt }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { 
  User, 
  ArrowDown, 
  Paperclip, 
  Delete, 
  Position 
} from '@element-plus/icons-vue'
import { useChatStore } from '../stores/chatStore'
const chatStore = useChatStore()
const getAiRole = (roleId) => {
  return chatStore.aiRoles.find(role => role.id === roleId) || null
}
const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  mentionMode: {
    type: Boolean,
    default: false
  },
  mentionedRole: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'send', 'mention-role'])

const inputRef = ref(null)

// 计算属性
const inputValue = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 快捷提示
const quickPrompts = ref([
  '分析这只股票走势',
  '推荐潜力股',
  '预测大盘趋势',
  '财报对股价影响',
  '热门股票策略',
  '股票组合建议'
])


// 方法
const handleKeydown = (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    sendMessage()
  }
}

const handleInput = (value) => {
  emit('update:modelValue', value)
}

const sendMessage = () => {
  if (!inputValue.value.trim() || props.disabled) return
  
  emit('send')
}

const clearInput = () => {
  inputValue.value = ''
  nextTick(() => {
    inputRef.value?.focus()
  })
}

const attachFile = () => {
  ElMessage.info('文件上传功能开发中...')
}

const insertPrompt = (prompt) => {
  inputValue.value = prompt
  nextTick(() => {
    inputRef.value?.focus()
  })
}

const cancelMention = () => {
  emit('mention-role', null)
}

</script>

<style scoped>
.input-area {
  background: white;
  border-top: 1px solid #e4e7ed;
  padding: 16px 20px;
  box-shadow: 0 -2px 12px rgba(0, 0, 0, 0.05);
}

.input-container {
  max-width: 800px;
  margin: 0 auto;
  position: relative;
}

.input-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding: 0 4px;
}

.mention-indicator {
  margin-bottom: 12px;
  padding: 8px 12px;
  background: linear-gradient(135deg, #e6f7ff 0%, #bae7ff 100%);
  border: 1px solid #91d5ff;
  border-radius: 12px;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.mention-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.mention-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: white;
  flex-shrink: 0;
}

.mention-text {
  flex: 1;
  color: #1890ff;
  font-size: 14px;
  font-weight: 500;
}

.mention-input :deep(.el-textarea__inner) {
  border-color: #91d5ff;
  background: #f6ffed;
}

.toolbar-left {
  display: flex;
  gap: 8px;
}

.toolbar-left .el-button {
  color: #666;
  font-size: 13px;
  padding: 4px 8px;
  height: auto;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.toolbar-left .el-button:hover {
  background: #f5f7fa;
  color: #409EFF;
}




.input-wrapper {
  display: flex;
  gap: 12px;
  align-items: flex-end;
}

.message-input {
  flex: 1;
}

.message-input :deep(.el-textarea__inner) {
  border-radius: 20px;
  border: 2px solid #e4e7ed;
  padding: 16px 20px;
  font-size: 15px;
  line-height: 1.5;
  resize: none;
  transition: all 0.3s ease;
  background: #fafafa;
}

.message-input :deep(.el-textarea__inner):focus {
  border-color: #409EFF;
  background: white;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.1);
}

.message-input :deep(.el-textarea__inner):hover {
  border-color: #c0c4cc;
  background: white;
}

.input-actions {
  display: flex;
  align-items: flex-end;
}

.send-button {
  height: 44px;
  padding: 0 24px;
  border-radius: 22px;
  font-weight: 500;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
  transition: all 0.3s ease;
}

.send-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.send-button:disabled {
  background: #c0c4cc;
  transform: none;
  box-shadow: none;
}

.quick-prompts {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

.prompt-title {
  font-size: 13px;
  color: #666;
  margin-bottom: 8px;
  font-weight: 500;
}

.prompt-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.prompt-tag {
  padding: 6px 12px;
  background: #f5f7fa;
  border: 1px solid #e4e7ed;
  border-radius: 16px;
  font-size: 12px;
  color: #666;
  cursor: pointer;
  transition: all 0.2s ease;
}

.prompt-tag:hover {
  background: #e6f7ff;
  border-color: #91d5ff;
  color: #409EFF;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .input-area {
    padding: 12px 16px;
  }
  
  .input-wrapper {
    flex-direction: column;
    gap: 8px;
  }
  
  .send-button {
    width: 100%;
    height: 40px;
    border-radius: 20px;
  }
  
  .prompt-tags {
    flex-direction: column;
  }
  
  .prompt-tag {
    text-align: center;
  }
}
</style>
