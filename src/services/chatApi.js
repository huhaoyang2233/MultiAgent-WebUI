/**
 * AI聊天API服务
 * 支持流式响应和多角色AI
 */

// API配置
const API_CONFIG = {
  baseUrl: 'http://127.0.0.1:8083', // 根据您的后端API地址修改
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'text/stream'
  }
}

/**
 * 流式聊天API
 * @param {Object} params - 请求参数
 * @param {string} params.message - 用户消息
 * @param {string} params.role - AI角色ID
 * @param {string} params.chatId - 聊天ID
 * @param {Function} onChunk - 接收数据块的回调函数
 * @param {Function} onComplete - 完成回调函数
 * @param {Function} onError - 错误回调函数
 */
export const streamChat = async ({ message, role, target_role, chatId }, onChunk, onComplete, onError) => {
  const userInfoStr = localStorage.getItem("userInfo")
  const userInfo = userInfoStr ? JSON.parse(userInfoStr) : null
  const userToken = localStorage.getItem("userToken")
  try {
    const response = await fetch(`${API_CONFIG.baseUrl}/chat`, {
      method: 'POST',
      headers: API_CONFIG.headers,
      body: JSON.stringify({
        user_config: {
          "user_ID": userInfo.userID,
          "user_TOKEN": userToken,
          "chat_ID": chatId || "chat_ID"
        },
        user_message: {
          "target_role": target_role,
          "query": message
        }
      }),
      //长连接超时关闭
      // signal: AbortSignal.timeout(API_CONFIG.timeout)
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    try {
      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop()
        
        for (const line of lines) {
          if (!line.trim() || !line.startsWith('data: ')) continue
          const data = line.slice(6).trim()
          if (data === '[DONE]') {
            onComplete?.()
            return
          }
          try {
            const parsed = JSON.parse(data)
            // 每个块就是完整的一条消息，直接触发回调
            onChunk?.({
              role: parsed.role,
              content: parsed.content
            })
          } catch (e) {
            console.warn('解析流式数据失败:', e, line)
          }
        }
      }
    } finally {
      reader.releaseLock()
    }

    onComplete?.()
  } catch (error) {
    console.error('流式聊天请求失败:', error)
    onError?.(error)
  }
}

/**
 * 登录
 */
export const login = async ({ username, password }) => {
  try {
    if (!username || !password) {
      return { success: false, message: '用户名或密码不能为空' }
    }
    const response = await fetch(`${API_CONFIG.baseUrl}/user/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username, password }),
      signal: AbortSignal.timeout(API_CONFIG.timeout)
    })

    if (!response.ok) {
      const errorText = await response.text()
      return { success: false, message: `HTTP错误: ${response.status} ${errorText}` }
    }

    const data = await response.json()

    // 假设后端返回结构 { token: string, user: { ... } }
    if (data.userToken) {
      // 可以存储到 localStorage 或全局状态
      console.log(data)
      localStorage.setItem('userToken', data.userToken)
      localStorage.setItem('userInfo', JSON.stringify(data.userInfo))
      return { success: true, data, message: '登录成功' }
    } else {
      return { success: false, message: data.message || '登录失败' }
    }
  } catch (error) {
    console.error('登录失败', error)
    return { success: false, message: error.message || '登录请求异常' }
  }
}

/**
 * 注册
 */
export const sign = async() =>{
  try {
    //动态获取
    const response = await fetch(`${API_CONFIG.baseUrl}/user/sign`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
  
    if (data.success=="1"){
      console.warn('注册成功，请重新登录！', error)
    }
  } catch (error) {
    console.warn('注册失败', error)
  }
}

/**
 * 注销
 */
export const logout = async() =>{
  try {
    //动态获取
    const response = await fetch(`${API_CONFIG.baseUrl}/user/logout`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    return await response.json()
  } catch (error) {
    console.warn('注册失败', error)
  }
}


/**
 * 获取AI角色列表
 */
export const getAiRoles = async () => {
  try {
    //动态获取
    const response = await fetch(`${API_CONFIG.baseUrl}/roles`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    return await response.json()
  } catch (error) {
    console.warn('获取AI角色失败，使用默认角色:', error)
    // 返回默认角色列表
    return [
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
      },
    ]
  }
}


/**
 * 获取聊天历史
 */
/**
 * 获取聊天历史
 * @param {string} userToken - 用户token
 * @param {Object} userInfo - 用户信息对象
 */
export const getChatHistory = async () => {
  try {
    const userToken = localStorage.getItem("userToken")
    const userInfoStr = localStorage.getItem("userInfo")
    const userInfo = userInfoStr ? JSON.parse(userInfoStr) : null
    const response = await fetch(`${API_CONFIG.baseUrl}/chat/history`, {
      method: 'POST', // 改成POST，方便传用户信息
      headers: {
        'Content-Type': 'application/json'
      },
      
      body: JSON.stringify({
        userID: userInfo.userID,
        chatID:""
      }),
    })
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.warn('获取聊天历史失败:', error)
    return []
  }
}