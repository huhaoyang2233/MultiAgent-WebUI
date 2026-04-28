/**
 * 演示数据
 * 用于展示AI对话界面的功能
 */

export const demoChatHistory = [
  {
    id: '1',
    title: 'Vue3开发问题咨询',
    createdAt: new Date('2024-01-15T10:30:00'),
    updatedAt: new Date('2024-01-15T11:45:00'),
    messageCount: 6
  },
  {
    id: '2', 
    title: '如何写一份技术文档',
    createdAt: new Date('2024-01-14T14:20:00'),
    updatedAt: new Date('2024-01-14T15:30:00'),
    messageCount: 8
  },
  {
    id: '3',
    title: '数据分析方法讨论',
    createdAt: new Date('2024-01-13T09:15:00'),
    updatedAt: new Date('2024-01-13T10:00:00'),
    messageCount: 4
  }
]

export const demoMessages = {
  '1': [
    {
      id: 1,
      role: 'user',
      content: '我想学习Vue3的Composition API，有什么好的建议吗？',
      timestamp: new Date('2024-01-15T10:30:00')
    },
    {
      id: 2,
      role: 'assistant',
      content: '很高兴为您介绍Vue3的Composition API！这是一个非常强大的特性，让我为您详细讲解：\n\n## Composition API的优势\n\n1. **更好的逻辑复用**: 可以将相关逻辑组织在一起\n2. **更灵活的类型推断**: 对TypeScript支持更好\n3. **更清晰的代码结构**: 按功能而不是选项来组织代码\n\n## 学习建议\n\n- 从基础的`ref`和`reactive`开始\n- 学习`computed`和`watch`的使用\n- 掌握组合式函数（Composables）的概念\n- 实践一些实际项目\n\n您想从哪个方面开始深入了解呢？',
      timestamp: new Date('2024-01-15T10:31:00'),
      aiRole: {
        id: 'coder',
        name: '编程助手',
        avatar: '💻',
        color: '#E6A23C'
      }
    },
    {
      id: 3,
      role: 'user',
      content: '能给我一个简单的例子吗？',
      timestamp: new Date('2024-01-15T10:35:00')
    },
    {
      id: 4,
      role: 'assistant',
      content: '当然！让我给您展示一个简单的计数器例子：\n\n```vue\n<template>\n  <div>\n    <p>计数: {{ count }}</p>\n    <button @click="increment">增加</button>\n    <button @click="decrement">减少</button>\n  </div>\n</template>\n\n<script setup>\nimport { ref } from \'vue\'\n\n// 响应式数据\nconst count = ref(0)\n\n// 方法\nconst increment = () => {\n  count.value++\n}\n\nconst decrement = () => {\n  count.value--\n}\n</script>\n```\n\n这个例子展示了：\n- 使用`ref`创建响应式数据\n- 在模板中直接使用\n- 通过`.value`访问和修改数据\n\n您觉得这个例子怎么样？',
      timestamp: new Date('2024-01-15T10:36:00'),
      aiRole: {
        id: 'coder',
        name: '编程助手',
        avatar: '💻',
        color: '#E6A23C'
      }
    }
  ],
  '2': [
    {
      id: 5,
      role: 'user',
      content: '我需要写一份API接口文档，有什么建议吗？',
      timestamp: new Date('2024-01-14T14:20:00')
    },
    {
      id: 6,
      role: 'assistant',
      content: '写一份好的API文档是非常重要的！让我为您提供一些专业的建议：\n\n## 文档结构建议\n\n1. **概述部分**\n   - API简介和用途\n   - 认证方式\n   - 基础URL和版本\n\n2. **接口详情**\n   - 请求方法（GET/POST/PUT/DELETE）\n   - 请求路径和参数\n   - 请求体格式\n   - 响应格式和状态码\n\n3. **示例代码**\n   - 不同语言的调用示例\n   - 错误处理示例\n\n## 最佳实践\n\n- 使用清晰的命名规范\n- 提供完整的错误码说明\n- 包含真实的示例数据\n- 定期更新文档\n\n您想从哪个部分开始？我可以帮您制定具体的文档大纲。',
      timestamp: new Date('2024-01-14T14:21:00'),
      aiRole: {
        id: 'writer',
        name: '写作专家',
        avatar: '✍️',
        color: '#67C23A'
      }
    }
  ]
}

export const demoQuickPrompts = [
  '请解释一下Vue3的响应式原理',
  '帮我写一个React组件',
  '如何优化网站性能？',
  '数据分析的最佳实践',
  '写一份产品需求文档',
  '解释一下微服务架构',
  '如何设计一个RESTful API？',
  '机器学习入门指南'
]

export const demoAiRoles = [
  {
    id: 'assistant',
    name: '智能助手',
    avatar: '🤖',
    color: '#409EFF',
    description: '您的智能助手，随时为您解答问题'
  },
  {
    id: 'writer',
    name: '写作专家',
    avatar: '✍️',
    color: '#67C23A',
    description: '专业的写作顾问，帮助您创作优质内容'
  },
  {
    id: 'coder',
    name: '编程助手',
    avatar: '💻',
    color: '#E6A23C',
    description: '经验丰富的程序员，协助您解决技术问题'
  },
  {
    id: 'analyst',
    name: '数据分析师',
    avatar: '📊',
    color: '#F56C6C',
    description: '专业的数据分析师，提供深入的数据洞察'
  },
  {
    id: 'designer',
    name: 'UI设计师',
    avatar: '🎨',
    color: '#9C27B0',
    description: '创意设计师，提供界面设计和用户体验建议'
  },
  {
    id: 'manager',
    name: '项目管理专家',
    avatar: '📋',
    color: '#607D8B',
    description: '项目管理专家，协助您规划和管理项目'
  }
]
