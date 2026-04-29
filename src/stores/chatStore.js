import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getChatHistory, getAiRoles, getFriends, getGroups, getCustomAgents, toggleSubscribeAgent as toggleSubscribeAgentApi } from '../services/chatApi'

export const useChatStore = defineStore('chat', () => {
  const chatHistory = ref([])
  const currentChatId = ref(null)
  const messages = ref({})
  const mentionMode = ref(false)
  const mentionedRole = ref(null)
  
  const aiRoles = ref([])
  const friends = ref([])
  const groups = ref([])
  const customAgents = ref([])
  
  const currentGroupId = ref(null)
  const groupMessages = ref({})
  const currentSelectedFriendId = ref(null)
  const friendMessages = ref({})
  const currentTab = ref('friends')
  const currentView = ref('chat')
  const isEnglish = ref(false)
  const isDataLoaded = ref(false)

  const getAiRole = (roleId) => {
    return aiRoles.value.find(r => r.id === roleId) || null
  }

  const initData = async (force = false) => {
    console.log('initData called, force:', force, 'isDataLoaded:', isDataLoaded.value)
    if (!force && isDataLoaded.value) {
      console.log('Data already loaded, returning')
      return
    }
    
    try {
      console.log('Fetching data from backend...')
      const [roles, friendsData, groupsData, agents] = await Promise.all([
        getAiRoles(),
        getFriends(),
        getGroups(),
        getCustomAgents()
      ])
      console.log('Data fetched successfully:', { roles: roles.length, friends: friendsData.length, groups: groupsData.length, agents: agents.length })
      
      aiRoles.value = roles.map(r => ({
        id: r.id,
        name: r.name,
        avatar: r.avatar,
        color: r.color || '#409EFF',
        description: r.description,
        ability: r.ability,
        personality: r.personality
      }))
      
      friends.value = friendsData.map(f => ({
        id: f.id,
        name: f.name,
        avatar: f.avatar,
        status: f.status,
        type: f.type,
        roleId: f.role_id
      }))
      
      groups.value = groupsData.map(g => ({
        id: g.id,
        name: g.name,
        avatar: g.avatar,
        members: g.members || [],
        memberCount: g.member_count || g.memberCount,
        lastMessage: g.last_message || '',
        lastTime: g.last_time || '',
        unread: g.unread || 0
      }))
      
      customAgents.value = agents.map(a => ({
        id: a.id,
        name: a.name,
        avatar: a.avatar,
        ability: a.ability,
        personality: a.personality,
        description: a.description,
        subscribed: a.subscribed,
        createdAt: a.created_at
      }))
      
      isDataLoaded.value = true
    } catch (err) {
      console.error('初始化数据失败:', err)
    }
  }

  const addCustomAgent = (agent) => {
    const newAgent = {
      id: Date.now().toString(),
      ...agent,
      subscribed: false,
      createdAt: new Date().toISOString().split('T')[0]
    }
    customAgents.value.push(newAgent)
    return newAgent
  }

  const toggleSubscribeAgent = async (agentId) => {
    const agent = customAgents.value.find(a => a.id === agentId)
    if (!agent) return
    
    try {
      const result = await toggleSubscribeAgentApi(agentId)
      if (result.success) {
        agent.subscribed = !agent.subscribed
        if (agent.subscribed && result.data.friend_id) {
          const newFriend = {
            id: result.data.friend_id,
            name: agent.name,
            avatar: agent.avatar,
            status: 'online',
            type: 'ai',
            roleId: agentId
          }
          friends.value = [...friends.value, newFriend]
        } else if (!agent.subscribed) {
          const index = friends.value.findIndex(f => f.roleId === agentId)
          if (index !== -1) {
            friends.value = friends.value.filter((_, i) => i !== index)
          }
        }
      }
    } catch (error) {
      console.error('订阅操作失败:', error)
    }
  }

  const setCurrentView = (view) => {
    currentView.value = view
  }

  const initUserChats = async () => {
    try {
      const data = await getChatHistory()
      const chatRecords = data.chat_history || []
      console.log('获取聊天记录:', chatRecords)

      const grouped = {}
      chatRecords.forEach(record => {
        const chatId = record.chat_id
        if (!grouped[chatId]) grouped[chatId] = []
        grouped[chatId].push({
          id: Date.now() + Math.random(),
          role: record.role == "Chat_User"? "user":record.role,
          content: record.content,
          timestamp: record.timestamp,
          isStreaming: false
        })
      })

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

      currentChatId.value = chatHistory.value.length > 0 ? chatHistory.value[0].id : null

    } catch (err) {
      console.warn('初始化聊天记录失败:', err)
      chatHistory.value = []
      messages.value = {}
      currentChatId.value = null
    }
  }
  
  const currentMessages = computed(() => {
    return currentChatId.value ? messages.value[currentChatId.value] || [] : []
  })
  
  const currentChat = computed(() => {
    return chatHistory.value.find(chat => chat.id === currentChatId.value)
  })
  
  const createNewChat = () => {
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
    
    const chat = chatHistory.value.find(c => c.id === currentChatId.value)
    if (chat) {
      chat.messageCount = chatMessages.length
      chat.updatedAt = new Date()
      
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

  const selectFriend = (friendId) => {
    currentSelectedFriendId.value = friendId
    currentGroupId.value = null
    if (!friendMessages.value[friendId]) {
      friendMessages.value = {
        ...friendMessages.value,
        [friendId]: []
      }
    }
  }

  const selectGroup = (groupId) => {
    currentGroupId.value = groupId
    currentSelectedFriendId.value = null
    if (!groupMessages.value[groupId]) {
      groupMessages.value = {
        ...groupMessages.value,
        [groupId]: []
      }
    }
  }

  const addFriendMessage = (friendId, message) => {
    const current = friendMessages.value[friendId] || []
    friendMessages.value = {
      ...friendMessages.value,
      [friendId]: [...current, message]
    }
  }

  const setFriendMessages = (friendId, messages) => {
    friendMessages.value = {
      ...friendMessages.value,
      [friendId]: messages
    }
  }

  const addGroupMessage = (groupId, message) => {
    const current = groupMessages.value[groupId] || []
    groupMessages.value = {
      ...groupMessages.value,
      [groupId]: [...current, message]
    }
  }

  const setGroupMessages = (groupId, messages) => {
    groupMessages.value = {
      ...groupMessages.value,
      [groupId]: messages
    }
  }

  const clearFriendMessages = (friendId) => {
    if (friendMessages.value[friendId]) {
      friendMessages.value[friendId] = []
    }
  }

  const clearGroupMessages = (groupId) => {
    if (groupMessages.value[groupId]) {
      groupMessages.value[groupId] = []
    }
    const group = groups.value.find(g => g.id === groupId)
    if (group) {
      group.unread = 0
    }
  }

  const setCurrentTab = (tab) => {
    currentTab.value = tab
  }

  const currentFriend = computed(() => {
    return friends.value.find(f => f.id === currentSelectedFriendId.value)
  })

  const currentGroup = computed(() => {
    return groups.value.find(g => g.id === currentGroupId.value)
  })

  const currentFriendMessages = computed(() => {
    return currentSelectedFriendId.value ? friendMessages.value[currentSelectedFriendId.value] || [] : []
  })

  const currentGroupMessages = computed(() => {
    return currentGroupId.value ? groupMessages.value[currentGroupId.value] || [] : []
  })
  
  return {
    chatHistory,
    currentChatId,
    messages,
    aiRoles,
    mentionMode,
    mentionedRole,
    friends,
    groups,
    currentGroupId,
    groupMessages,
    currentSelectedFriendId,
    friendMessages,
    currentTab,
    currentView,
    customAgents,
    isEnglish,
    isDataLoaded,
    getAiRole,
    addCustomAgent,
    toggleSubscribeAgent,
    setCurrentView,
    initData,
    initUserChats,
    currentMessages,
    currentChat,
    createNewChat,
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
    selectFriend,
    selectGroup,
    addFriendMessage,
    setFriendMessages,
    addGroupMessage,
    setGroupMessages,
    clearFriendMessages,
    clearGroupMessages,
    setCurrentTab,
    currentFriend,
    currentGroup,
    currentFriendMessages,
    currentGroupMessages
  }
})