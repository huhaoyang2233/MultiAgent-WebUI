import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getChatHistory } from '../services/chatApi'  //加载历史记录

export const useChatStore = defineStore('chat', () => {
  // 状态
  const chatHistory = ref([])
  const currentChatId = ref(null)
  const messages = ref({}) // 存储每个聊天的消息
  const mentionMode = ref(false) // @模式状态
  const mentionedRole = ref(null) // 被@的角色
  
  // AI角色配置
  const aiRoles = ref([
    {
      id: 'MarketScount',
      name: '市场观察员',
      avatar: '💻',
      color: '#409EFF',
      description: '擅长大盘及板块分析，掌握资金流向、行业热度及分化情况，能够发现潜在龙头股。主要负责整体市场板块观察，为个股和板块提供趋势参考。'
    },
    {
      id: 'TrendSeer',
      name: '趋势与短期预测分析师',
      avatar: '📊',
      color: '#67C23A',
      description: '擅长对指定的股票专注长短期的趋势分析与股票预测，擅长识别金叉/死叉、极值点和趋势延续/反转信号。能量化支撑位、压力位及潜在价格区间，为操作提供参考。'
    },
    {
      id: 'PatternMaster',
      name: '技术形态与波动分析师',
      avatar: '🤖',
      color: '#E6A23C',
      description: '擅长对指定的股票做K线形态识别与波动分析，能够判断头肩顶、W底、M顶等典型技术形态，结合RSI、MACD、布林带等指标分析市场波动。主要负责发现形态信号、预测潜在反转和支撑压力区域。'
    }
  ])
  const getAiRole = (roleId) => {
    return aiRoles.find(r => r.id === roleId) || null
  }

   // 初始化用户聊天记录
  const initUserChats = async () => {
    try {
      const data = await getChatHistory() // 调用后端接口
      const chatRecords = data.chat_history || []
      console.log('获取聊天记录:', chatRecords)

      // 按 chat_id 分组
      const grouped = {}
      chatRecords.forEach(record => {
        const chatId = record.chat_id
        if (!grouped[chatId]) grouped[chatId] = []
        grouped[chatId].push({
          id: Date.now() + Math.random(),       // 每条消息唯一 id
          role: record.role == "Chat_User"? "user":record.role,
          content: record.content,
          timestamp: record.timestamp,
          isStreaming: false
        })
      })

      // 构建 chatHistory 和 messages
      chatHistory.value = []
      messages.value = {}
      Object.keys(grouped).forEach(chatId => {
        const msgs = grouped[chatId]
        chatHistory.value.push({
          id: chatId,
          title: msgs[0].content.slice(0, 20) + "...",
          createdAt: msgs[0].timestamp,
          updatedAt: msgs[msgs.length - 1].timestamp,
          messageCount: msgs.length
        })
        messages.value[chatId] = msgs
      })
      console.log('最终 messages:', messages.value)

      // 默认选中第一个会话
      currentChatId.value = chatHistory.value.length > 0 ? chatHistory.value[0].id : null

    } catch (err) {
      console.warn('初始化聊天记录失败:', err)
      chatHistory.value = []
      messages.value = {}
      currentChatId.value = null
    }
  }
  
  //返回消息列表
  const currentMessages = computed(() => {
    return currentChatId.value ? messages.value[currentChatId.value] || [] : []
  })
  
  //消息元数据
  const currentChat = computed(() => {
    return chatHistory.value.find(chat => chat.id === currentChatId.value)
  })
  
  // 创建一个新会话
  const createNewChat = () => {
    //会话id
    const newChat = {
      id: Date.now().toString(),
      title: '新对话',
      createdAt: new Date(),
      updatedAt: new Date(),
      messageCount: 0
    }
    
    chatHistory.value.unshift(newChat)
    currentChatId.value = newChat.id
    messages.value[newChat.id] = []
    
    return newChat
  }
  
  const selectChat = (chatId) => {
    currentChatId.value = chatId
  }
  
  const addMessage = (message) => {
    if (!currentChatId.value) return
    
    const chatMessages = messages.value[currentChatId.value] || []
    chatMessages.push(message)
    messages.value[currentChatId.value] = chatMessages
    
    // 更新聊天记录信息
    const chat = chatHistory.value.find(c => c.id === currentChatId.value)
    if (chat) {
      chat.messageCount = chatMessages.length
      chat.updatedAt = new Date()
      
      // 如果是第一条用户消息，更新标题
      if (message.role === 'user' && chat.title === '新对话') {
        chat.title = message.content.length > 20 
          ? message.content.substring(0, 20) + '...' 
          : message.content
      }
    }
  }
  
  const updateStreamingMessage = (messageId, content) => {
    if (!currentChatId.value) return
    
    const chatMessages = messages.value[currentChatId.value] || []
    const messageIndex = chatMessages.findIndex(m => m.id === messageId)
    
    if (messageIndex !== -1) {
      chatMessages[messageIndex].content = content
    }
  }
  
  const finishStreamingMessage = (messageId) => {
    if (!currentChatId.value) return
    
    const chatMessages = messages.value[currentChatId.value] || []
    const messageIndex = chatMessages.findIndex(m => m.id === messageId)
    
    if (messageIndex !== -1) {
      chatMessages[messageIndex].isStreaming = false
    }
  }
  
  const updateMessageRole = (messageId, roleInfo) => {
    if (!currentChatId.value) return
    
    const chatMessages = messages.value[currentChatId.value] || []
    const messageIndex = chatMessages.findIndex(m => m.id === messageId)
    
    if (messageIndex !== -1) {
      chatMessages[messageIndex].aiRole = {
        id: roleInfo.role,
        name: roleInfo.name,
        avatar: roleInfo.avatar,
        color: roleInfo.color
      }
    }
  }
  
  const deleteChat = (chatId) => {
    const index = chatHistory.value.findIndex(chat => chat.id === chatId)
    if (index !== -1) {
      chatHistory.value.splice(index, 1)
      delete messages.value[chatId]
      
      // 如果删除的是当前聊天，选择第一个聊天
      if (currentChatId.value === chatId) {
        currentChatId.value = chatHistory.value.length > 0 ? chatHistory.value[0].id : null
      }
    }
  }
  
  const clearAllChats = () => {
    chatHistory.value = []
    messages.value = {}
    currentChatId.value = null
  }
  
  // @功能相关方法
  const startMention = (role) => {
    mentionMode.value = true
    mentionedRole.value = role
  }
  
  const cancelMention = () => {
    mentionMode.value = false
    mentionedRole.value = null
  }
  
  const formatMentionText = (text, role) => {
    if (!role) return text
    return `@${role.name} ${text}`
  }
  
  return {
    // 状态
    chatHistory,
    currentChatId,
    messages,
    aiRoles,
    mentionMode,
    mentionedRole,
    
    // 计算属性
    currentMessages,
    currentChat,
    
    // 方法
    createNewChat,
    getAiRole,
    selectChat,
    addMessage,
    updateStreamingMessage,
    finishStreamingMessage,
    updateMessageRole,
    deleteChat,
    clearAllChats,
    startMention,
    cancelMention,
    formatMentionText,
    initUserChats
  }
})
