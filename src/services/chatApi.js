/**
 * AI聊天API服务
 * 对接FastAPI后端
 */

const API_CONFIG = {
  baseUrl: 'http://localhost:8000',
  timeout: 30000
}

const getHeaders = () => {
  const token = localStorage.getItem('userToken')
  const headers = {
    'Content-Type': 'application/json'
  }
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  return headers
}

export const streamChat = async ({ message, role, target_role, chatId }, onChunk, onComplete, onError) => {
  const userInfoStr = localStorage.getItem("userInfo")
  const userInfo = userInfoStr ? JSON.parse(userInfoStr) : null
  try {
    const response = await fetch(`${API_CONFIG.baseUrl}/chat`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({
        user_config: {
          "user_ID": userInfo?.userID || userInfo?.id || 'unknown',
          "user_TOKEN": localStorage.getItem('userToken'),
          "chat_ID": chatId || "chat_ID"
        },
        user_message: {
          "target_role": target_role,
          "query": message
        }
      }),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const result = await response.json()
    onChunk?.({
      role: result.role,
      name: result.name,
      content: result.content
    })
    onComplete?.()
  } catch (error) {
    console.error('聊天请求失败:', error)
    onError?.(error)
  }
}

export const chatWithAgent = async (agentId, message) => {
  const userInfoStr = localStorage.getItem("userInfo")
  const userInfo = userInfoStr ? JSON.parse(userInfoStr) : null
  
  try {
    const response = await fetch(`${API_CONFIG.baseUrl}/chat/agent/${agentId}`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({
        user_config: {
          "user_ID": userInfo?.userID || userInfo?.id || 'unknown'
        },
        user_message: {
          "query": message
        }
      }),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error('与智能体聊天失败:', error)
    return {
      id: Date.now(),
      role: 'assistant',
      name: '系统',
      content: '服务异常，正在抢修'
    }
  }
}

export const chatWithFriend = async (friendId, message) => {
  const userInfoStr = localStorage.getItem("userInfo")
  const userInfo = userInfoStr ? JSON.parse(userInfoStr) : null
  
  try {
    const response = await fetch(`${API_CONFIG.baseUrl}/chat/friend/${friendId}`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({
        user_config: {
          "user_ID": userInfo?.userID || userInfo?.id || 'unknown'
        },
        user_message: {
          "query": message
        }
      }),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error('与用户聊天失败:', error)
    return {
      id: Date.now(),
      role: 'assistant',
      name: '系统',
      content: '服务异常，正在抢修'
    }
  }
}

export const chatInGroup = async (groupId, message) => {
  const userInfoStr = localStorage.getItem("userInfo")
  const userInfo = userInfoStr ? JSON.parse(userInfoStr) : null
  
  try {
    const response = await fetch(`${API_CONFIG.baseUrl}/chat/group/${groupId}`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({
        user_config: {
          "user_ID": userInfo?.userID || userInfo?.id || 'unknown'
        },
        user_message: {
          "query": message
        }
      }),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error('群聊失败:', error)
    return {
      id: Date.now(),
      role: 'assistant',
      name: '系统',
      content: '服务异常，正在抢修'
    }
  }
}

export const checkOrCreateSession = async (chatType, targetId) => {
  try {
    const response = await fetch(`${API_CONFIG.baseUrl}/chat/session/${chatType}/${targetId}`, {
      method: 'GET',
      headers: getHeaders(),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error('检查或创建会话失败:', error)
    throw error
  }
}

export const createGroup = async (name, avatar, members) => {
  try {
    const response = await fetch(`${API_CONFIG.baseUrl}/groups`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({
        name,
        avatar,
        members
      }),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error('创建群聊失败:', error)
    throw error
  }
}

export const getChatHistory = async (chatType, targetId) => {
  try {
    const response = await fetch(`${API_CONFIG.baseUrl}/chat/history/${chatType}/${targetId}`, {
      method: 'GET',
      headers: getHeaders(),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error('获取聊天历史失败:', error)
    throw error
  }
}

export const getUserSessions = async () => {
  try {
    const response = await fetch(`${API_CONFIG.baseUrl}/chat/sessions`, {
      method: 'GET',
      headers: getHeaders(),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error('获取会话列表失败:', error)
    return { sessions: [] }
  }
}

export const deleteSession = async (sessionId) => {
  try {
    const response = await fetch(`${API_CONFIG.baseUrl}/chat/session/${sessionId}`, {
      method: 'DELETE',
      headers: getHeaders(),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error('删除会话失败:', error)
    throw error
  }
}

export const login = async ({ username, password }) => {
  try {
    if (!username || !password) {
      return { success: false, message: '用户名或密码不能为空' }
    }

    if (process.env.NODE_ENV === 'development') {
      if ((username === 'admin' && password === 'admin123') || 
          (username === 'user' && password === 'user123')) {
        const mockData = {
          access_token: `mock_token_${username}_${Date.now()}`,
          token_type: 'bearer',
          user: {
            id: username === 'admin' ? 'user-1' : 'user-2',
            username: username,
            role: username === 'admin' ? 'admin' : 'user',
            avatar: `https://i.pravatar.cc/40?u=${username}`,
            email: `${username}@example.com`
          }
        }
        localStorage.setItem('userToken', mockData.access_token)
        localStorage.setItem('userInfo', JSON.stringify(mockData.user))
        return { success: true, data: mockData, message: '登录成功' }
      }
      return { success: false, message: '用户名或密码错误，请使用 admin/admin123 或 user/user123' }
    }

    const response = await fetch(`${API_CONFIG.baseUrl}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams({
        username: username,
        password: password
      }),
      signal: AbortSignal.timeout(API_CONFIG.timeout)
    })

    if (!response.ok) {
      const errorText = await response.text()
      return { success: false, message: `HTTP错误: ${response.status} ${errorText}` }
    }

    const data = await response.json()

    if (data.access_token) {
      localStorage.setItem('userToken', data.access_token)
      localStorage.setItem('userInfo', JSON.stringify(data.user))
      return { success: true, data, message: '登录成功' }
    } else {
      return { success: false, message: data.message || '登录失败' }
    }
  } catch (error) {
    console.error('登录失败', error)
    return { success: false, message: error.message || '登录请求异常' }
  }
}

export const register = async ({ username, password, email }) => {
  try {
    if (!username || !password) {
      return { success: false, message: '用户名或密码不能为空' }
    }

    if (process.env.NODE_ENV === 'development') {
      if (username.length < 3 || password.length < 6) {
        return { success: false, message: '用户名至少3个字符，密码至少6个字符' }
      }
      console.log(`模拟注册用户: ${username}`)
      return { success: true, message: '注册成功，请登录' }
    }

    const response = await fetch(`${API_CONFIG.baseUrl}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username, password, email: email || `${username}@example.com` }),
      signal: AbortSignal.timeout(API_CONFIG.timeout)
    })

    if (!response.ok) {
      const error = await response.json()
      return { success: false, message: error.detail || `注册失败 ${response.status}` }
    }

    const data = await response.json()
    return { success: true, data, message: '注册成功，请登录' }
  } catch (error) {
    console.warn('注册失败', error)
    return { success: false, message: error.message || '注册请求异常' }
  }
}

export const sign = register

export const logout = async () => {
  try {
    const response = await fetch(`${API_CONFIG.baseUrl}/auth/logout`, {
      method: 'POST',
      headers: getHeaders()
    })
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    localStorage.removeItem('userToken')
    localStorage.removeItem('userInfo')
    return await response.json()
  } catch (error) {
    console.warn('注销失败', error)
    localStorage.removeItem('userToken')
    localStorage.removeItem('userInfo')
    return { success: true }
  }
}

export const getAiRoles = async () => {
  try {
    const response = await fetch(`${API_CONFIG.baseUrl}/ai-roles`, {
      headers: getHeaders()
    })
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    return data.ai_roles || data
  } catch (error) {
    console.warn('获取AI角色失败，使用默认角色:', error)
    return [
      {
        id: 'role-1',
        name: '市场观察员',
        avatar: '📊',
        color: '#409EFF',
        description: '专业的市场分析助手，能够提供实时市场行情分析和投资建议。'
      },
      {
        id: 'role-2',
        name: '趋势分析师',
        avatar: '📈',
        color: '#67C23A',
        description: '擅长分析市场趋势，预测未来走势，帮助用户做出明智决策。'
      },
      {
        id: 'role-3',
        name: '技术分析师',
        avatar: '💻',
        color: '#E6A23C',
        description: '精通技术分析，能够解读各种技术指标和图表模式。'
      },
    ]
  }
}



export const getFriends = async () => {
  try {
    const response = await fetch(`${API_CONFIG.baseUrl}/friends`, {
      headers: getHeaders()
    })
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    return data.friends || data
  } catch (error) {
    console.warn('获取好友列表失败:', error)
    return []
  }
}

export const getGroups = async () => {
  try {
    const response = await fetch(`${API_CONFIG.baseUrl}/groups`, {
      headers: getHeaders()
    })
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    return data.groups || data
  } catch (error) {
    console.warn('获取群聊列表失败:', error)
    return []
  }
}

export const getCustomAgents = async () => {
  try {
    const response = await fetch(`${API_CONFIG.baseUrl}/custom-agents`, {
      headers: getHeaders()
    })
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    return data.custom_agents || data
  } catch (error) {
    console.warn('获取自定义智能体失败:', error)
    return []
  }
}

export const createCustomAgent = async (agent) => {
  try {
    const response = await fetch(`${API_CONFIG.baseUrl}/custom-agents`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(agent)
    })
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || `创建失败 ${response.status}`)
    }
    const data = await response.json()
    return { success: true, data, message: '创建成功' }
  } catch (error) {
    console.error('创建智能体失败:', error)
    return { success: false, message: error.message || '创建失败' }
  }
}

export const toggleSubscribeAgent = async (agentId) => {
  try {
    const response = await fetch(`${API_CONFIG.baseUrl}/custom-agents/${agentId}/subscribe`, {
      method: 'PUT',
      headers: getHeaders()
    })
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    return { success: true, data, message: data.message }
  } catch (error) {
    console.error('订阅智能体失败:', error)
    return { success: false, message: error.message || '操作失败' }
  }
}

export const deleteCustomAgent = async (agentId) => {
  try {
    const response = await fetch(`${API_CONFIG.baseUrl}/custom-agents/${agentId}`, {
      method: 'DELETE',
      headers: getHeaders()
    })
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    return { success: true, data, message: data.message }
  } catch (error) {
    console.error('删除智能体失败:', error)
    return { success: false, message: error.message || '删除失败' }
  }
}

export const sendMessage = async (targetId, targetType, message) => {
  try {
    const response = await fetch(`${API_CONFIG.baseUrl}/chat-history/${targetId}/${targetType}/messages`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(message)
    })
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    return { success: true, data: data.message, message: '发送成功' }
  } catch (error) {
    console.error('发送消息失败:', error)
    return { success: false, message: error.message || '发送失败' }
  }
}

export const getChatMessages = async (targetId, targetType) => {
  try {
    const response = await fetch(`${API_CONFIG.baseUrl}/chat-history/${targetId}/${targetType}`, {
      headers: getHeaders()
    })
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    return data.chat?.messages || []
  } catch (error) {
    console.warn('获取聊天消息失败:', error)
    return []
  }
}

export const clearChatHistory = async (targetId, targetType) => {
  try {
    const response = await fetch(`${API_CONFIG.baseUrl}/chat-history/${targetId}/${targetType}`, {
      method: 'DELETE',
      headers: getHeaders()
    })
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    return { success: true, message: data.message }
  } catch (error) {
    console.error('清空聊天记录失败:', error)
    return { success: false, message: error.message || '操作失败' }
  }
}

export const getUsers = async () => {
  try {
    const response = await fetch(`${API_CONFIG.baseUrl}/admin/users`, {
      method: 'GET',
      headers: getHeaders()
    })
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    return await response.json()
  } catch (error) {
    console.error('获取用户列表失败:', error)
    return []
  }
}

export const createUser = async (userData) => {
  try {
    const response = await fetch(`${API_CONFIG.baseUrl}/admin/users`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(userData)
    })
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    return { success: true, data, message: '创建成功' }
  } catch (error) {
    console.error('创建用户失败:', error)
    return { success: false, message: error.message || '创建失败' }
  }
}

export const updateUser = async (userId, userData) => {
  try {
    const response = await fetch(`${API_CONFIG.baseUrl}/admin/users/${userId}`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify(userData)
    })
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    return { success: true, data, message: '更新成功' }
  } catch (error) {
    console.error('更新用户失败:', error)
    return { success: false, message: error.message || '更新失败' }
  }
}

export const deleteUser = async (userId) => {
  try {
    const response = await fetch(`${API_CONFIG.baseUrl}/admin/users/${userId}`, {
      method: 'DELETE',
      headers: getHeaders()
    })
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    return { success: true, data, message: data.message }
  } catch (error) {
    console.error('删除用户失败:', error)
    return { success: false, message: error.message || '删除失败' }
  }
}

export const getAllSessions = async () => {
  try {
    const response = await fetch(`${API_CONFIG.baseUrl}/admin/sessions`, {
      method: 'GET',
      headers: getHeaders()
    })
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    return await response.json()
  } catch (error) {
    console.error('获取会话列表失败:', error)
    return {}
  }
}

export const deleteAdminSession = async (sessionId) => {
  try {
    const response = await fetch(`${API_CONFIG.baseUrl}/admin/sessions/${sessionId}`, {
      method: 'DELETE',
      headers: getHeaders()
    })
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    return { success: true, message: data.message }
  } catch (error) {
    console.error('删除会话失败:', error)
    return { success: false, message: error.message || '删除失败' }
  }
}