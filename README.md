# AI对话界面

一个基于Vue3和Element Plus的现代化AI对话界面，支持多角色AI、流式响应和优雅的用户体验。

## 功能特性

### 🎨 界面设计
- **响应式布局**: 左侧可伸缩边栏 + 右侧聊天区域
- **现代化UI**: 圆润的输入框、渐变色彩、流畅动画
- **优雅交互**: 平滑过渡效果、悬停反馈、加载状态

### 🤖 多角色AI支持
- **智能助手** 🤖: 通用问题解答
- **写作专家** ✍️: 专业写作指导
- **编程助手** 💻: 技术问题解决
- **数据分析师** 📊: 数据洞察分析

### 💬 聊天功能
- **流式响应**: 实时显示AI回复过程
- **历史记录**: 自动保存对话历史
- **会话管理**: 创建、切换、删除对话
- **消息操作**: 复制、重新生成消息

### 🔧 技术特性
- **Vue3 Composition API**: 现代化Vue开发模式
- **Element Plus**: 企业级UI组件库
- **Pinia状态管理**: 响应式状态管理
- **流式API**: 支持Server-Sent Events
- **TypeScript支持**: 类型安全的开发体验

## 项目结构

```
src/
├── components/          # Vue组件
│   ├── Sidebar.vue     # 左侧边栏
│   ├── ChatWindow.vue  # 聊天窗口
│   └── InputArea.vue   # 输入区域
├── views/              # 页面视图
│   └── ChatView.vue    # 主聊天页面
├── stores/             # Pinia状态管理
│   └── chatStore.js    # 聊天状态管理
├── services/           # API服务
│   └── chatApi.js      # 聊天API接口
├── router/             # 路由配置
│   └── index.js        # 路由定义
└── main.js             # 应用入口
```

## 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 启动开发服务器

```bash
npm run dev
```

### 3. 构建生产版本

```bash
npm run build
```

## 配置说明

### API配置

在 `src/services/chatApi.js` 中配置您的后端API地址：

```javascript
const API_CONFIG = {
  baseUrl: 'http://localhost:8080/api', // 修改为您的API地址
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'text/stream'
  }
}
```

### 流式响应格式

后端API应返回Server-Sent Events格式的流式数据：

```
data: {"type": "role_info", "role": "assistant", "name": "智能助手", "avatar": "🤖", "color": "#409EFF"}

data: {"type": "content", "content": "您好！", "role": "assistant", "timestamp": "2024-01-01T00:00:00.000Z"}

data: {"type": "content", "content": "我是", "role": "assistant", "timestamp": "2024-01-01T00:00:00.000Z"}

data: [DONE]
```

## 自定义配置

### 添加新的AI角色

在 `src/stores/chatStore.js` 中的 `aiRoles` 数组添加新角色：

```javascript
{
  id: 'custom_role',
  name: '自定义角色',
  avatar: '🎯',
  color: '#FF6B6B',
  description: '角色的描述信息'
}
```

### 修改主题色彩

在组件样式中修改CSS变量：

```css
:root {
  --primary-color: #667eea;
  --secondary-color: #764ba2;
  --accent-color: #409EFF;
}
```

### 自定义快捷提示

在 `src/components/InputArea.vue` 中修改 `quickPrompts` 数组：

```javascript
const quickPrompts = ref([
  '您的自定义提示1',
  '您的自定义提示2',
  // ...
])
```

## 浏览器支持

- Chrome >= 87
- Firefox >= 78
- Safari >= 14
- Edge >= 88

## 开发指南

### 添加新功能

1. 在相应的组件中添加功能代码
2. 更新状态管理（如需要）
3. 添加相应的API接口
4. 更新文档

### 样式规范

- 使用CSS Grid和Flexbox布局
- 遵循Element Plus设计规范
- 保持响应式设计
- 使用CSS变量管理主题色彩

### 代码规范

- 使用Vue3 Composition API
- 遵循ES6+语法
- 使用async/await处理异步操作
- 添加适当的错误处理

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 更新日志

### v1.0.0
- 初始版本发布
- 支持多角色AI对话
- 实现流式响应
- 完整的UI组件系统
- 响应式设计
