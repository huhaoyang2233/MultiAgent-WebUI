# 🤖 多智能体平台 (Multi-Agent Platform)

> 🚀 **快速接入智能体的平台** - 支持单一智能体对话和多智能体群聊，零配置快速部署

<p align="center">
  <img src="https://img.shields.io/badge/Vue-3.4+-green.svg" alt="Vue3">
  <img src="https://img.shields.io/badge/FastAPI-0.100+-blue.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/Element_Plus-2.4+-blue.svg" alt="Element Plus">
  <img src="https://img.shields.io/badge/File_Storage-JSON-orange.svg" alt="File Storage">
  <img src="https://img.shields.io/badge/Deploy-Easy-success.svg" alt="Easy Deploy">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</p>

## 🎯 核心特点

### ⚡ 快速接入

- **零配置启动**: 无需复杂的数据库配置，使用 JSON 文件存储
- **一键部署**: 单命令启动前后端服务
- **快速集成**: 支持主流大模型 API（OpenAI、火山引擎等）

### 🤖 智能体支持

- **单一智能体**: 1对1专属AI对话，个性化服务
- **多智能体群聊**: 多个AI同时参与讨论，模拟真实群聊场景
- **智能体市场**: 创建、分享、订阅智能体
- **可见性控制**: 公有/私有智能体，灵活管理权限

### 💾 文件存储

- **JSON 文件存储**: 无需数据库，数据以 JSON 格式存储
- **易于备份**: 直接复制文件即可备份全部数据
- **便于迁移**: 轻松在不同环境间迁移数据
- **可读性强**: 数据文件可直接查看和编辑

### 🚀 快速部署

- **轻量级**: 低资源占用，适合个人服务器部署
- **Docker 支持**: 提供 Dockerfile 一键容器化（开发中）
- **无依赖**: 不依赖外部数据库或缓存服务

## 📋 目录

- [核心特点](#-核心特点)
- [功能特性](#-功能特性)
- [技术栈](#-技术栈)
- [快速开始](#-快速开始)
- [项目结构](#-项目结构)
- [配置说明](#-配置说明)
- [API 文档](#-api-文档)
- [开发指南](#-开发指南)
- [更新日志](#-更新日志)

## ✨ 功能特性

### 🎨 界面设计

- **响应式布局**: 适配桌面和移动端
- **现代化UI**: 渐变色彩、圆角设计、流畅动画
- **中英双语**: 完整的中英文切换支持
- **深色模式**: 支持深色主题（开发中）

### 🤖 智能体管理

- **自定义智能体**: 创建个性化的AI智能体
- **能力配置**: 设置智能体的能力和性格
- **订阅机制**: 订阅/取消订阅智能体
- **可见性控制**: 公有/私有智能体设置
  - **Public**: 所有用户可见
  - **Private**: 仅创建者和管理员可见

### 👥 群组聊天

- **多人群聊**: 支持多人同时在线聊天
- **群成员管理**: 邀请、移除群成员
- **消息历史**: 完整的聊天记录保存
- **实时响应**: 流式消息展示

### 💬 会话管理

- **会话列表**: 查看所有历史会话
- **会话详情**: 查看会话元数据（AI名称、群成员等）
- **消息搜索**: 搜索历史消息（开发中）
- **数据导出**: 导出会话记录（开发中）

### 🔐 用户系统

- **多用户支持**: 支持用户注册和登录
- **角色权限**: 普通用户和管理员角色
- **后台管理**: 管理员可管理所有用户、智能体和会话

## 🛠 技术栈

### 前端

- **Vue 3.4+**: Composition API，响应式系统
- **Element Plus**: 企业级UI组件库
- **Pinia**: 状态管理
- **Vue Router**: 路由管理
- **Vite**: 构建工具

### 后端

- **FastAPI**: 高性能Python Web框架
- **Uvicorn**: ASGI服务器
- **JSON File Storage**: 文件存储，无需数据库

### 部署

- **轻量级部署**: 单服务器即可运行
- **Docker**: 容器化部署支持（开发中）
- **Nginx**: 反向代理和静态文件服务

## 🚀 快速开始

### 环境要求

- Node.js >= 18
- Python >= 3.9
- npm 或 yarn

### 1. 克隆项目

```bash
git clone <repository-url>
cd MultiAgent-WebUI
```

### 2. 安装前端依赖

```bash
npm install
# 或
yarn install
```

### 3. 安装后端依赖

```bash
cd backend
pip install -r requirements.txt
```

### 4. 配置模型（可选）

默认使用模拟数据，如需接入真实AI模型，配置环境变量：

```bash
export VOLCENGINE_API_KEY=your_api_key
export VOLCENGINE_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
export VOLCENGINE_MODEL=your_model_endpoint
```

### 5. 启动服务

**启动后端：**

```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**启动前端：**

```bash
# 在项目根目录
npm run dev
```

### 6. 访问应用

- 前端: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

**默认账号**: admin / admin123

## 📁 项目结构

```
MultiAgent-WebUI/
├── backend/                    # 后端代码
│   ├── data/                   # 数据存储（JSON文件）
│   │   ├── files/              # 数据文件
│   │   │   ├── users.json      # 用户数据
│   │   │   ├── sessions.json   # 会话索引
│   │   │   ├── friends.json    # 好友数据
│   │   │   ├── groups.json     # 群组数据
│   │   │   ├── ai_roles.json   # AI角色配置
│   │   │   └── custom_agents.json  # 自定义智能体
│   │   └── sessions/           # 会话消息存储
│   ├── routes/                 # API路由
│   ├── main.py                 # 应用入口
│   └── requirements.txt        # Python依赖
├── src/                        # 前端代码
│   ├── components/             # Vue组件
│   ├── views/                  # 页面视图
│   ├── stores/                 # Pinia状态管理
│   ├── services/               # API服务
│   └── main.js                 # 应用入口
├── package.json                # Node依赖
└── README.md                   # 项目文档
```

## ⚙️ 配置说明

### 前端配置

在 `src/services/chatApi.js` 中配置API地址：

```javascript
const API_CONFIG = {
  baseUrl: 'http://localhost:8000',  // 后端API地址
  timeout: 30000,
}
```

### 后端配置

在 `backend/` 目录下创建 `.env` 文件：

```env
# 火山引擎模型配置（可选，默认使用模拟数据）
VOLCENGINE_API_KEY=your_api_key
VOLCENGINE_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
VOLCENGINE_MODEL=your_model_endpoint

# JWT密钥
SECRET_KEY=your_secret_key

# 其他配置
DEBUG=true
```

### 数据备份

所有数据存储在 `backend/data/` 目录，直接复制该目录即可备份：

```bash
cp -r backend/data backup/data_$(date +%Y%m%d)
```

## 📚 API 文档

### 认证接口

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/auth/register` | 用户注册 |
| POST | `/auth/login` | 用户登录 |
| GET | `/auth/me` | 获取当前用户 |

### 聊天接口

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/chat/agent/{session_id}` | 与智能体聊天 |
| POST | `/chat/friend/{session_id}` | 与好友聊天 |
| POST | `/chat/group/{session_id}` | 群聊 |
| GET | `/chat/sessions` | 获取会话列表 |
| POST | `/chat/session` | 创建/检查会话 |

### 智能体接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/agents` | 获取智能体列表 |
| POST | `/agents` | 创建智能体 |
| PUT | `/agents/{id}` | 更新智能体 |
| DELETE | `/agents/{id}` | 删除智能体 |
| POST | `/agents/{id}/subscribe` | 订阅/取消订阅 |

### 管理接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/admin/users` | 获取所有用户 |
| GET | `/admin/sessions` | 获取所有会话 |
| DELETE | `/admin/sessions/{id}` | 删除会话 |

完整的API文档请访问: http://localhost:8000/docs

## 📝 开发指南

### 添加新的AI角色

在 `backend/data/files/ai_roles.json` 中添加：

```json
{
  "id": "role_custom",
  "name": "自定义角色",
  "avatar": "🎯",
  "color": "#FF6B6B",
  "description": "角色描述",
  "ability": "能力说明",
  "personality": "性格特点"
}
```

### 自定义智能体创建

用户可以在智能体管理页面创建自定义智能体：

1. 点击"创建智能体"
2. 填写名称、头像、能力、性格、描述
3. 选择可见性（Public/Private）
4. 点击创建

### 开发规范

- **前端**: 使用 Vue3 Composition API，遵循 ESLint 规范
- **后端**: 遵循 PEP8 规范，使用类型注解
- **Git**: 使用 Conventional Commits 规范

## 📈 更新日志

### v1.0.0 (2024-04)

- ✨ 初始版本发布
- 🤖 智能体管理系统
- 👥 群组聊天功能
- 💬 多会话管理
- 🔐 用户认证系统
- 🌐 中英双语支持
- 📱 响应式设计
- 🔧 后台管理系统

### 计划功能

- [ ] 深色模式
- [ ] 消息搜索
- [ ] 文件上传
- [ ] 语音消息
- [ ] Docker部署
- [ ] 实时通知
- [ ] 数据导出

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 项目
2. 创建分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目基于 [MIT](LICENSE) 许可证开源。

## 👨‍💻 作者

- 开发者: Your Name
- 邮箱: your.email@example.com

## 🙏 致谢

- [Vue.js](https://vuejs.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Element Plus](https://element-plus.org/)
- [Pinia](https://pinia.vuejs.org/)

---

## 📸 项目截图

### 群组聊天界面
群组聊天支持多个智能体同时参与对话，模拟真实群聊场景。

![群组聊天](./images/截屏2026-04-30%2015.31.25.png)

### 智能体管理
创建和管理自定义智能体，设置能力、性格和可见性。

![智能体管理](./images/截屏2026-04-30%2015.31.35.png)

### 会话列表
查看所有历史会话，支持按类型筛选（单聊/群聊）。

![会话列表](./images/截屏2026-04-30%2015.31.44.png)

### 后台管理
管理员可查看所有用户、会话和系统状态。

![后台管理](./images/截屏2026-04-30%2015.31.57.png)

---

<p align="center">
  🌟 如果这个项目对你有帮助，请给个 Star！
</p>

<p align="center">
  <b>快速接入智能体，单一对话 + 多智能体群聊，文件存储，一键部署！</b>
</p>
