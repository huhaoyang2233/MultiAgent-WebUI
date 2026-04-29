<template>
  <div class="admin-panel">
    <div class="admin-sidebar">
      <div class="admin-logo">
        <span class="logo-icon">⚙️</span>
        <span class="logo-text">{{ isEnglish ? 'Admin Panel' : '后台管理' }}</span>
      </div>
      <div class="admin-nav">
        <button 
          :class="['nav-item', { active: adminTab === 'users' }]" 
          @click="adminTab = 'users'"
        >
          <span class="nav-icon">👥</span>
          {{ isEnglish ? 'User Management' : '用户管理' }}
        </button>
        <button 
          :class="['nav-item', { active: adminTab === 'agents' }]" 
          @click="adminTab = 'agents'"
        >
          <span class="nav-icon">🤖</span>
          {{ isEnglish ? 'Agent Management' : '智能体管理' }}
        </button>
        <button 
          :class="['nav-item', { active: adminTab === 'sessions' }]" 
          @click="adminTab = 'sessions'"
        >
          <span class="nav-icon">💬</span>
          {{ isEnglish ? 'Session Management' : '会话管理' }}
        </button>
      </div>
      <button class="back-btn" @click="goBack">
          <span>←</span> {{ isEnglish ? 'Back' : '返回' }}
        </button>
    </div>
    
    <div class="admin-content">
      <div v-if="adminTab === 'users'" class="users-panel">
        <div class="panel-header">
          <h2>{{ isEnglish ? 'User Management' : '用户管理' }}</h2>
          <button class="add-btn" @click="showAddUserModal = true">
            <span>+</span> {{ isEnglish ? 'Add User' : '添加用户' }}
          </button>
        </div>
        
        <div class="search-bar">
          <input 
            type="text" 
            v-model="userSearch" 
            :placeholder="isEnglish ? 'Search users...' : '搜索用户...'"
            class="search-input"
          />
        </div>
        
        <div class="user-list">
          <div 
            v-for="user in filteredUsers" 
            :key="user.id"
            :class="['user-card', { active: selectedUser?.id === user.id }]"
            @click="selectUser(user)"
          >
            <div class="user-avatar">
              <img :src="user.avatar" :alt="user.username" />
            </div>
            <div class="user-info">
              <h3>{{ user.username }}</h3>
              <p>{{ user.email }}</p>
              <div :class="['role-badge', user.role]">
                {{ user.role === 'admin' ? (isEnglish ? 'Admin' : '管理员') : (isEnglish ? 'User' : '普通用户') }}
              </div>
            </div>
            <div class="user-actions">
              <button class="action-btn edit" @click.stop="editUser(user)">✏️</button>
              <button 
                class="action-btn delete" 
                @click.stop="confirmDeleteUser(user)"
                :disabled="user.role === 'admin'"
              >🗑️</button>
            </div>
          </div>
        </div>
        
        <div v-if="selectedUser" class="user-detail">
          <h3>{{ isEnglish ? 'User Details' : '用户详情' }}</h3>
          <div class="detail-row">
            <span class="label">{{ isEnglish ? 'ID' : '用户ID' }}</span>
            <span>{{ selectedUser.id }}</span>
          </div>
          <div class="detail-row">
            <span class="label">{{ isEnglish ? 'Username' : '用户名' }}</span>
            <span>{{ selectedUser.username }}</span>
          </div>
          <div class="detail-row">
            <span class="label">{{ isEnglish ? 'Email' : '邮箱' }}</span>
            <span>{{ selectedUser.email }}</span>
          </div>
          <div class="detail-row">
            <span class="label">{{ isEnglish ? 'Role' : '角色' }}</span>
            <span>{{ selectedUser.role === 'admin' ? (isEnglish ? 'Admin' : '管理员') : (isEnglish ? 'User' : '普通用户') }}</span>
          </div>
          <div class="detail-row">
            <span class="label">{{ isEnglish ? 'Created At' : '创建时间' }}</span>
            <span>{{ formatDate(selectedUser.created_at) }}</span>
          </div>
          <button class="view-sessions-btn" @click="viewUserSessions(selectedUser)">
            {{ isEnglish ? 'View Sessions' : '查看会话' }}
          </button>
        </div>
      </div>
      
      <div v-if="adminTab === 'agents'" class="agents-panel">
        <div class="panel-header">
          <h2>{{ isEnglish ? 'Agent Management' : '智能体管理' }}</h2>
        </div>
        
        <div class="search-bar">
          <input 
            type="text" 
            v-model="agentSearch" 
            :placeholder="isEnglish ? 'Search agents...' : '搜索智能体...'"
            class="search-input"
          />
        </div>
        
        <div class="agent-list">
          <div 
            v-for="agent in filteredAgents" 
            :key="agent.id"
            class="agent-card"
          >
            <div class="agent-avatar">{{ agent.avatar }}</div>
            <div class="agent-info">
              <h3>{{ agent.name }}</h3>
              <p>{{ agent.description }}</p>
            </div>
            <div class="agent-stats">
              <span>{{ agent.ability }}</span>
            </div>
            <div class="agent-actions">
              <button class="action-btn edit" @click="editAgent(agent)">✏️</button>
              <button class="action-btn delete" @click="confirmDeleteAgent(agent)">🗑️</button>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="adminTab === 'sessions'" class="sessions-panel">
        <div class="panel-header">
          <h2>{{ isEnglish ? 'Session Management' : '会话管理' }}</h2>
          <select v-model="sessionFilterUser" class="user-filter">
            <option value="">{{ isEnglish ? 'All Users' : '所有用户' }}</option>
            <option v-for="user in allUsers" :key="user.id" :value="user.id">
              {{ user.username }}
            </option>
          </select>
        </div>
        
        <div class="session-list">
          <div v-for="(sessions, userId) in filteredSessions" :key="userId" class="user-sessions">
            <div class="user-header">
              <span>{{ getUserById(userId)?.username || userId }}</span>
              <span class="count">{{ sessions.length }} {{ isEnglish ? 'sessions' : '个会话' }}</span>
            </div>
            <div class="session-items">
              <div 
                v-for="session in sessions" 
                :key="session.session_id"
                class="session-item"
              >
                <span class="session-id">{{ session.session_id }}</span>
                <span class="session-type">{{ session.chat_type }}</span>
                <span class="session-count">{{ session.message_count }} {{ isEnglish ? 'messages' : '条消息' }}</span>
                <button class="action-btn delete" @click="deleteSession(session.session_id)">🗑️</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="showAddUserModal" class="modal-overlay" @click="closeModals">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editingUser ? (isEnglish ? 'Edit User' : '编辑用户') : (isEnglish ? 'Add User' : '添加用户') }}</h3>
          <button class="close-btn" @click="closeModals">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>{{ isEnglish ? 'Username' : '用户名' }}</label>
            <input type="text" v-model="formData.username" class="form-input" />
          </div>
          <div class="form-group">
            <label>{{ isEnglish ? 'Email' : '邮箱' }}</label>
            <input type="email" v-model="formData.email" class="form-input" />
          </div>
          <div class="form-group">
            <label>{{ isEnglish ? 'Password' : '密码' }}</label>
            <input type="password" v-model="formData.password" class="form-input" />
          </div>
          <div class="form-group">
            <label>{{ isEnglish ? 'Role' : '角色' }}</label>
            <select v-model="formData.role" class="form-input">
              <option value="user">{{ isEnglish ? 'User' : '普通用户' }}</option>
              <option value="admin">{{ isEnglish ? 'Admin' : '管理员' }}</option>
            </select>
          </div>
        </div>
        <div class="modal-footer">
          <button class="modal-btn cancel" @click="closeModals">{{ isEnglish ? 'Cancel' : '取消' }}</button>
          <button class="modal-btn confirm" @click="saveUser">{{ isEnglish ? 'Save' : '保存' }}</button>
        </div>
      </div>
    </div>
    
    <div v-if="showConfirmModal" class="modal-overlay" @click="showConfirmModal = false">
      <div class="modal-content confirm-modal" @click.stop>
        <div class="confirm-icon">⚠️</div>
        <h3>{{ confirmTitle }}</h3>
        <p>{{ confirmMessage }}</p>
        <div class="modal-footer">
          <button class="modal-btn cancel" @click="showConfirmModal = false">{{ isEnglish ? 'Cancel' : '取消' }}</button>
          <button class="modal-btn danger" @click="executeConfirmAction">{{ isEnglish ? 'Confirm' : '确认' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useChatStore } from '../stores/chatStore';
import { getUsers, createUser, updateUser, deleteUser, getAllSessions, deleteAdminSession as deleteSessionApi } from '../services/chatApi';
const router = useRouter();
const chatStore = useChatStore();
const isEnglish = computed(() => chatStore.isEnglish);
const adminTab = ref('users');
const allUsers = ref([]);
const customAgents = ref([]);
const userSearch = ref('');
const agentSearch = ref('');
const sessionFilterUser = ref('');
const selectedUser = ref(null);
const showAddUserModal = ref(false);
const editingUser = ref(null);
const formData = ref({
 username: '',
 email: '',
 password: '',
 role: 'user'
});
const showConfirmModal = ref(false);
const confirmTitle = ref('');
const confirmMessage = ref('');
const confirmAction = ref(null);
const filteredUsers = computed(() => {
 if (!userSearch.value)
 return allUsers.value;
 const keyword = userSearch.value.toLowerCase();
 return allUsers.value.filter(user => user.username.toLowerCase().includes(keyword) ||
 user.email.toLowerCase().includes(keyword));
});
const filteredAgents = computed(() => {
 if (!agentSearch.value)
 return customAgents.value;
 const keyword = agentSearch.value.toLowerCase();
 return customAgents.value.filter(agent => agent.name.toLowerCase().includes(keyword) ||
 agent.description.toLowerCase().includes(keyword));
});
const allSessions = ref({});
const filteredSessions = computed(() => {
 if (!sessionFilterUser.value)
 return allSessions.value;
 const result = {};
 if (allSessions.value[sessionFilterUser.value]) {
 result[sessionFilterUser.value] = allSessions.value[sessionFilterUser.value];
 }
 return result;
});
const getUserById = (userId) => {
 return allUsers.value.find(u => u.id === userId);
};
const selectUser = (user) => {
 selectedUser.value = user;
};
const editUser = (user) => {
 editingUser.value = user;
 formData.value = {
 username: user.username,
 email: user.email,
 password: '',
 role: user.role
 };
 showAddUserModal.value = true;
};
const confirmDeleteUser = (user) => {
 confirmTitle.value = isEnglish.value ? 'Delete User' : '删除用户';
 confirmMessage.value = isEnglish.value ? `Are you sure you want to delete ${user.username}?` : `确定要删除用户 ${user.username} 吗？`;
 confirmAction.value = () => deleteUserAction(user.id);
 showConfirmModal.value = true;
};
const deleteUserAction = async (userId) => {
 try {
 await deleteUser(userId);
 allUsers.value = allUsers.value.filter(u => u.id !== userId);
 if (selectedUser.value?.id === userId) {
 selectedUser.value = null;
 }
 showConfirmModal.value = false;
 }
 catch (error) {
 console.error('删除用户失败:', error);
 showConfirmModal.value = false;
 }
};
const closeModals = () => {
 showAddUserModal.value = false;
 editingUser.value = null;
 formData.value = {
 username: '',
 email: '',
 password: '',
 role: 'user'
 };
};
const saveUser = async () => {
 if (!formData.value.username || !formData.value.email)
 return;
 try {
 if (editingUser.value) {
 await updateUser(editingUser.value.id, formData.value);
 const index = allUsers.value.findIndex(u => u.id === editingUser.value.id);
 if (index !== -1) {
 allUsers.value[index] = { ...allUsers.value[index], ...formData.value };
 }
 }
 else {
 const newUser = await createUser(formData.value);
 allUsers.value.push(newUser);
 }
 closeModals();
 }
 catch (error) {
 console.error('保存用户失败:', error);
 }
};
const confirmDeleteAgent = (agent) => {
 confirmTitle.value = isEnglish.value ? 'Delete Agent' : '删除智能体';
 confirmMessage.value = isEnglish.value ? `Are you sure you want to delete ${agent.name}?` : `确定要删除智能体 ${agent.name} 吗？`;
 confirmAction.value = () => deleteAgentAction(agent.id);
 showConfirmModal.value = true;
};
const deleteAgentAction = async (agentId) => {
 showConfirmModal.value = false;
};
const goBack = () => {
 router.push('/group');
};
const viewUserSessions = (user) => {
 adminTab.value = 'sessions';
 sessionFilterUser.value = user.id;
};
const deleteSession = async (sessionId) => {
 try {
 await deleteSessionApi(sessionId);
 await loadSessions();
 }
 catch (error) {
 console.error('删除会话失败:', error);
 }
};
const executeConfirmAction = () => {
 if (confirmAction.value) {
 confirmAction.value();
 }
};
const formatDate = (dateStr) => {
 if (!dateStr)
 return '';
 return new Date(dateStr).toLocaleString('zh-CN');
};
const loadUsers = async () => {
 try {
 const users = await getUsers();
 allUsers.value = users;
 }
 catch (error) {
 console.error('加载用户列表失败:', error);
 }
};
const loadAgents = async () => {
 try {
 const agents = await chatStore.customAgents;
 customAgents.value = agents;
 }
 catch (error) {
 console.error('加载智能体列表失败:', error);
 }
};
const loadSessions = async () => {
 try {
 const sessions = await getAllSessions();
 allSessions.value = sessions;
 }
 catch (error) {
 console.error('加载会话列表失败:', error);
 }
};
onMounted(async () => {
 await loadUsers();
 await loadAgents();
 await loadSessions();
});
</script>

<style scoped>
.admin-panel {
  display: flex;
  height: 100vh;
  background: #f8fafc;
}

.admin-sidebar {
  width: 240px;
  background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.admin-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px;
  margin-bottom: 20px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
}

.logo-icon {
  font-size: 24px;
}

.logo-text {
  font-size: 16px;
  font-weight: 600;
  color: white;
}

.admin-nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 16px;
  border-radius: 10px;
  border: none;
  background: transparent;
  color: #cbd5e1;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.nav-item.active {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: white;
}

.nav-icon {
  font-size: 18px;
}

.back-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  border-radius: 10px;
  border: none;
  background: rgba(255, 255, 255, 0.1);
  color: #cbd5e1;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  color: white;
}

.admin-content {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.panel-header h2 {
  font-size: 20px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.add-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  border-radius: 12px;
  border: none;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.search-bar {
  margin-bottom: 20px;
}

.search-input {
  width: 100%;
  padding: 12px 16px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  background: white;
  font-size: 14px;
  outline: none;
  transition: all 0.3s ease;
}

.search-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.user-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.user-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px;
  border-radius: 14px;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.user-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.user-card.active {
  border-color: #3b82f6;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, rgba(96, 165, 250, 0.05) 100%);
}

.user-avatar img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
}

.user-info {
  flex: 1;
}

.user-info h3 {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 4px;
}

.user-info p {
  font-size: 13px;
  color: #64748b;
  margin: 0 0 6px;
}

.role-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 500;
}

.role-badge.admin {
  background: rgba(249, 115, 22, 0.1);
  color: #f97316;
}

.role-badge.user {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.user-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  border: none;
  background: #f1f5f9;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  background: #e2e8f0;
}

.action-btn.delete:hover {
  background: #fee2e2;
}

.action-btn.delete:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.user-detail {
  background: white;
  border-radius: 14px;
  padding: 24px;
}

.user-detail h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 20px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #f1f5f9;
}

.detail-row:last-of-type {
  border-bottom: none;
}

.detail-row .label {
  font-size: 14px;
  color: #64748b;
  font-weight: 500;
}

.detail-row span:last-child {
  font-size: 14px;
  color: #1e293b;
}

.view-sessions-btn {
  margin-top: 20px;
  padding: 12px 24px;
  border-radius: 12px;
  border: none;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-sessions-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.agent-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 16px;
}

.agent-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px;
  border-radius: 14px;
  background: white;
}

.agent-avatar {
  width: 60px;
  height: 60px;
  border-radius: 16px;
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
}

.agent-info h3 {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.agent-info p {
  font-size: 13px;
  color: #64748b;
  margin: 4px 0 0;
  line-height: 1.5;
}

.agent-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.agent-stats span {
  padding: 4px 10px;
  border-radius: 10px;
  background: rgba(168, 85, 247, 0.1);
  color: #7c3aed;
  font-size: 12px;
}

.agent-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.sessions-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.user-filter {
  padding: 10px 16px;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  background: white;
  font-size: 14px;
  outline: none;
}

.user-sessions {
  background: white;
  border-radius: 14px;
  overflow: hidden;
}

.user-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(135deg, #f0f6ff 0%, #e0e7ff 100%);
}

.user-header span:first-child {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
}

.count {
  font-size: 13px;
  color: #64748b;
}

.session-items {
  padding: 12px;
}

.session-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px;
  border-radius: 10px;
  margin-bottom: 8px;
  background: #f8fafc;
}

.session-item:last-child {
  margin-bottom: 0;
}

.session-id {
  font-size: 13px;
  color: #334155;
  font-family: monospace;
}

.session-type {
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}

.session-count {
  font-size: 13px;
  color: #64748b;
  margin-left: auto;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 16px;
  width: 90%;
  max-width: 480px;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #f1f5f9;
}

.modal-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.close-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: #f1f5f9;
  font-size: 20px;
  color: #64748b;
  cursor: pointer;
}

.close-btn:hover {
  background: #e2e8f0;
}

.modal-body {
  padding: 24px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #334155;
  margin-bottom: 8px;
}

.form-input {
  width: 100%;
  padding: 12px;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  font-size: 14px;
  outline: none;
  transition: all 0.3s ease;
}

.form-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.modal-footer {
  display: flex;
  gap: 12px;
  padding: 20px 24px;
  border-top: 1px solid #f1f5f9;
}

.modal-btn {
  flex: 1;
  padding: 12px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.modal-btn.cancel {
  background: #f1f5f9;
  color: #64748b;
}

.modal-btn.cancel:hover {
  background: #e2e8f0;
}

.modal-btn.confirm {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: white;
}

.modal-btn.confirm:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.modal-btn.danger {
  background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);
  color: white;
}

.confirm-modal {
  text-align: center;
  padding: 32px;
}

.confirm-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.confirm-modal h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 8px;
}

.confirm-modal p {
  font-size: 14px;
  color: #64748b;
  margin: 0;
}
</style>