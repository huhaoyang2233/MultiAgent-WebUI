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
        <button 
          :class="['nav-item', { active: adminTab === 'contacts' }]" 
          @click="adminTab = 'contacts'"
        >
          <span class="nav-icon">👫</span>
          {{ isEnglish ? 'Contacts Management' : '好友管理' }}
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
              <button class="action-btn view-friends" @click.stop="viewUserContacts(user)">👫</button>
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
          <div class="detail-actions">
            <button class="view-sessions-btn" @click="viewUserSessions(selectedUser)">
              {{ isEnglish ? 'View Sessions' : '查看会话' }}
            </button>
            <button class="view-contacts-btn" @click="viewUserContacts(selectedUser)">
              {{ isEnglish ? 'View Friends & Groups' : '查看好友和群组' }}
            </button>
          </div>
        </div>
      </div>
      
      <div v-if="adminTab === 'agents'" class="agents-panel">
        <div class="panel-header">
          <h2>{{ isEnglish ? 'Agent Management' : '智能体广场' }}</h2>
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
              <div class="agent-name-row">
                <h3>{{ agent.name }}</h3>
                <span :class="['visibility-badge', agent.public ? 'public' : 'private']">
                  {{ agent.public ? (isEnglish ? 'Public' : '公开') : (isEnglish ? 'Private' : '私有') }}
                </span>
              </div>
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
        
        <div class="search-bar">
          <input 
            type="text" 
            v-model="sessionSearch" 
            :placeholder="isEnglish ? 'Search sessions...' : '搜索会话...'"
            class="search-input"
          />
        </div>
        
        <div class="session-table-container">
          <table class="session-table">
            <thead>
              <tr>
                <th>{{ isEnglish ? 'User' : '用户' }}</th>
                <th>{{ isEnglish ? 'Session ID' : '会话ID' }}</th>
                <th>{{ isEnglish ? 'Type' : '类型' }}</th>
                <th>{{ isEnglish ? 'Messages' : '消息数' }}</th>
                <th>{{ isEnglish ? 'Actions' : '操作' }}</th>
              </tr>
            </thead>
            <tbody>
              <template v-for="(sessions, userId) in filteredSessions" :key="userId">
                <tr v-for="session in sessions" :key="session.session_id" class="session-row">
                  <td>{{ getUserById(userId)?.username || userId }}</td>
                  <td class="session-id-cell">{{ session.session_id }}</td>
                  <td>
                    <span :class="['type-badge', session.chat_type]">
                      {{ getChatTypeName(session.chat_type) }}
                    </span>
                  </td>
                  <td>{{ session.message_count }}</td>
                  <td>
                    <button class="action-btn view-history" @click="viewSessionHistory(session.session_id)">📋</button>
                    <button class="action-btn delete" @click="deleteSession(session.session_id)">🗑️</button>
                  </td>
                </tr>
              </template>
              <tr v-if="Object.keys(filteredSessions).length === 0">
                <td colspan="5" class="no-data">{{ isEnglish ? 'No sessions found' : '没有找到会话' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <div v-if="adminTab === 'contacts'" class="contacts-panel">
        <div class="panel-header">
          <h2>{{ isEnglish ? 'Friends & Groups Management' : '好友与群组管理' }}</h2>
          <div class="search-bar inline">
            <input 
              type="text" 
              v-model="contactSearch" 
              :placeholder="isEnglish ? 'Search contacts...' : '搜索联系人...'"
              class="search-input"
            />
          </div>
          <select v-model="contactFilterUser" class="user-filter">
            <option value="">{{ isEnglish ? 'All Users' : '所有用户' }}</option>
            <option v-for="user in allUsers" :key="user.id" :value="user.id">
              {{ user.username }}
            </option>
          </select>
        </div>
        
        <div class="contacts-tabs">
          <button :class="['tab-btn', { active: contactTab === 'friends' }]" @click="contactTab = 'friends'">
            {{ isEnglish ? 'Friends' : '好友' }}
          </button>
          <button :class="['tab-btn', { active: contactTab === 'groups' }]" @click="contactTab = 'groups'">
            {{ isEnglish ? 'Groups' : '群组' }}
          </button>
        </div>
        
        <div v-if="contactTab === 'friends'" class="friends-list">
          <div v-for="(friends, userId) in filteredFriends" :key="userId" class="user-contacts">
            <div class="user-contacts-header">
              {{ getUserById(userId)?.username || userId }} {{ isEnglish ? "'s Friends" : '的好友' }}
              <span class="count">({{ friends.length }})</span>
            </div>
            <div class="contact-cards">
              <div v-for="friend in friends" :key="friend.id" class="contact-card">
                <div class="contact-avatar">{{ friend.avatar }}</div>
                <div class="contact-info">
                  <h4>{{ friend.name }}</h4>
                  <p>{{ friend.type === 'ai' ? (isEnglish ? 'AI Agent' : 'AI智能体') : (isEnglish ? 'User' : '用户') }}</p>
                </div>
                <span :class="['status-dot', friend.status]"></span>
              </div>
            </div>
          </div>
          <div v-if="Object.keys(filteredFriends).length === 0" class="no-data">
            {{ isEnglish ? 'No friends found' : '没有找到好友' }}
          </div>
        </div>
        
        <div v-if="contactTab === 'groups'" class="groups-list">
          <div v-for="(groups, userId) in filteredGroups" :key="userId" class="user-contacts">
            <div class="user-contacts-header">
              {{ getUserById(userId)?.username || userId }} {{ isEnglish ? "'s Groups" : '的群组' }}
              <span class="count">({{ groups.length }})</span>
            </div>
            <div class="contact-cards">
              <div v-for="group in groups" :key="group.id" class="contact-card">
                <div class="contact-avatar">{{ group.avatar }}</div>
                <div class="contact-info">
                  <h4>{{ group.name }}</h4>
                  <p>{{ isEnglish ? `${group.members?.length || 0} members` : `${group.members?.length || 0} 名成员` }}</p>
                </div>
                <span :class="['status-dot', 'online']"></span>
              </div>
            </div>
          </div>
          <div v-if="Object.keys(filteredGroups).length === 0" class="no-data">
            {{ isEnglish ? 'No groups found' : '没有找到群组' }}
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
    
    <div v-if="showAgentModal" class="modal-overlay" @click="closeAgentModal">
      <div class="modal-content agent-modal" @click.stop>
        <div class="modal-header">
          <h3>{{ editingAgent ? (isEnglish ? 'Edit Agent' : '编辑智能体') : (isEnglish ? 'Add Agent' : '添加智能体') }}</h3>
          <button class="close-btn" @click="closeAgentModal">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>{{ isEnglish ? 'Name' : '名称' }}</label>
            <input type="text" v-model="agentForm.name" class="form-input" />
          </div>
          <div class="form-group">
            <label>{{ isEnglish ? 'Avatar' : '头像' }}</label>
            <input type="text" v-model="agentForm.avatar" class="form-input" placeholder="🤖" />
          </div>
          <div class="form-group">
            <label>{{ isEnglish ? 'Ability' : '能力' }}</label>
            <input type="text" v-model="agentForm.ability" class="form-input" />
          </div>
          <div class="form-group">
            <label>{{ isEnglish ? 'Personality' : '性格' }}</label>
            <textarea v-model="agentForm.personality" class="form-textarea"></textarea>
          </div>
          <div class="form-group">
            <label>{{ isEnglish ? 'Description' : '描述' }}</label>
            <textarea v-model="agentForm.description" class="form-textarea"></textarea>
          </div>
          <div class="form-group">
            <label>{{ isEnglish ? 'Visibility' : '可见性' }}</label>
            <div class="visibility-options">
              <label :class="['visibility-option', { selected: agentForm.public }]">
                <input type="radio" v-model="agentForm.public" :value="true" />
                <span>🌐 {{ isEnglish ? 'Public' : '公开' }}</span>
              </label>
              <label :class="['visibility-option', { selected: !agentForm.public }]">
                <input type="radio" v-model="agentForm.public" :value="false" />
                <span>🔒 {{ isEnglish ? 'Private' : '私有' }}</span>
              </label>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="modal-btn cancel" @click="closeAgentModal">{{ isEnglish ? 'Cancel' : '取消' }}</button>
          <button class="modal-btn confirm" @click="saveAgent">{{ isEnglish ? 'Save' : '保存' }}</button>
        </div>
      </div>
    </div>
    
    <div v-if="showSessionHistoryModal" class="modal-overlay" @click="closeSessionHistoryModal">
      <div class="modal-content session-history-modal" @click.stop>
        <div class="modal-header">
          <h3>{{ isEnglish ? 'Session History' : '会话历史' }}</h3>
          <button class="close-btn" @click="closeSessionHistoryModal">×</button>
        </div>
        <div class="modal-body history-body">
          <div v-if="sessionHistoryMessages.length === 0" class="no-history">
            {{ isEnglish ? 'No messages in this session' : '该会话暂无消息' }}
          </div>
          <div v-else class="message-list">
            <div 
              v-for="message in sessionHistoryMessages" 
              :key="message.id"
              :class="['message-item', message.role]"
            >
              <div class="message-avatar">{{ message.role === 'user' ? '👤' : '🤖' }}</div>
              <div class="message-content">
                <div class="message-name">{{ message.name }}</div>
                <div class="message-text">{{ message.content }}</div>
                <div class="message-time">{{ formatDate(message.timestamp) }}</div>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="modal-btn confirm" @click="closeSessionHistoryModal">{{ isEnglish ? 'Close' : '关闭' }}</button>
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

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useChatStore } from '../stores/chatStore';
import { 
  getUsers, 
  createUser, 
  updateUser, 
  deleteUser, 
  getAllSessions, 
  deleteAdminSession as deleteSessionApi,
  getUserFriends,
  getUserGroups,
  getSessionHistory,
  updateCustomAgent,
  deleteCustomAgent,
  createCustomAgent,
  getCustomAgents
} from '../services/chatApi';

const router = useRouter();
const chatStore = useChatStore();
const isEnglish = computed(() => chatStore.isEnglish);

const adminTab = ref('users');
const contactTab = ref('friends');

const allUsers = ref([]);
const customAgents = ref([]);
const allSessions = ref({});
const allFriends = ref({});
const allGroups = ref({});

const userSearch = ref('');
const agentSearch = ref('');
const sessionSearch = ref('');
const contactSearch = ref('');
const sessionFilterUser = ref('');
const contactFilterUser = ref('');

const selectedUser = ref(null);

const showAddUserModal = ref(false);
const showAgentModal = ref(false);
const showSessionHistoryModal = ref(false);
const showConfirmModal = ref(false);

const editingUser = ref(null);
const editingAgent = ref(null);

const formData = ref({
  username: '',
  email: '',
  password: '',
  role: 'user'
});

const agentForm = ref({
  name: '',
  avatar: '🤖',
  ability: '',
  personality: '',
  description: '',
  public: true
});

const sessionHistoryMessages = ref([]);
const currentSessionId = ref('');

const confirmTitle = ref('');
const confirmMessage = ref('');
const confirmAction = ref(null);

const filteredUsers = computed(() => {
  if (!userSearch.value) return allUsers.value;
  const keyword = userSearch.value.toLowerCase();
  return allUsers.value.filter(user => 
    user.username.toLowerCase().includes(keyword) ||
    user.email.toLowerCase().includes(keyword)
  );
});

const filteredAgents = computed(() => {
  if (!agentSearch.value) return customAgents.value;
  const keyword = agentSearch.value.toLowerCase();
  return customAgents.value.filter(agent => 
    agent.name.toLowerCase().includes(keyword) ||
    agent.description.toLowerCase().includes(keyword)
  );
});

const filteredSessions = computed(() => {
  let result = { ...allSessions.value };
  
  if (sessionFilterUser.value) {
    const filtered = {};
    if (result[sessionFilterUser.value]) {
      filtered[sessionFilterUser.value] = result[sessionFilterUser.value];
    }
    result = filtered;
  }
  
  if (sessionSearch.value) {
    const keyword = sessionSearch.value.toLowerCase();
    const filtered = {};
    for (const [userId, sessions] of Object.entries(result)) {
      const userSessions = sessions.filter(session => 
        session.session_id.toLowerCase().includes(keyword)
      );
      if (userSessions.length > 0) {
        filtered[userId] = userSessions;
      }
    }
    result = filtered;
  }
  
  return result;
});

const filteredFriends = computed(() => {
  let result = { ...allFriends.value };
  
  if (contactFilterUser.value) {
    const filtered = {};
    if (result[contactFilterUser.value]) {
      filtered[contactFilterUser.value] = result[contactFilterUser.value];
    }
    result = filtered;
  }
  
  if (contactSearch.value) {
    const keyword = contactSearch.value.toLowerCase();
    const filtered = {};
    for (const [userId, friends] of Object.entries(result)) {
      const userFriends = friends.filter(friend => 
        friend.name.toLowerCase().includes(keyword)
      );
      if (userFriends.length > 0) {
        filtered[userId] = userFriends;
      }
    }
    result = filtered;
  }
  
  return result;
});

const filteredGroups = computed(() => {
  let result = { ...allGroups.value };
  
  if (contactFilterUser.value) {
    const filtered = {};
    if (result[contactFilterUser.value]) {
      filtered[contactFilterUser.value] = result[contactFilterUser.value];
    }
    result = filtered;
  }
  
  if (contactSearch.value) {
    const keyword = contactSearch.value.toLowerCase();
    const filtered = {};
    for (const [userId, groups] of Object.entries(result)) {
      const userGroups = groups.filter(group => 
        group.name.toLowerCase().includes(keyword)
      );
      if (userGroups.length > 0) {
        filtered[userId] = userGroups;
      }
    }
    result = filtered;
  }
  
  return result;
});

const getUserById = (userId) => {
  return allUsers.value.find(u => u.id === userId);
};

const getChatTypeName = (type) => {
  const types = {
    'agent': isEnglish.value ? 'Agent' : '智能体',
    'friend': isEnglish.value ? 'Friend' : '好友',
    'group': isEnglish.value ? 'Group' : '群组',
    'unknown': isEnglish.value ? 'Unknown' : '未知'
  };
  return types[type] || type;
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
  } catch (error) {
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
  if (!formData.value.username || !formData.value.email) return;
  try {
    if (editingUser.value) {
      await updateUser(editingUser.value.id, formData.value);
      const index = allUsers.value.findIndex(u => u.id === editingUser.value.id);
      if (index !== -1) {
        allUsers.value[index] = { ...allUsers.value[index], ...formData.value };
      }
    } else {
      const newUser = await createUser(formData.value);
      allUsers.value.push(newUser);
    }
    closeModals();
  } catch (error) {
    console.error('保存用户失败:', error);
  }
};

const editAgent = (agent) => {
  editingAgent.value = agent;
  agentForm.value = {
    name: agent.name,
    avatar: agent.avatar,
    ability: agent.ability,
    personality: agent.personality,
    description: agent.description,
    public: agent.public !== undefined ? agent.public : true
  };
  showAgentModal.value = true;
};

const closeAgentModal = () => {
  showAgentModal.value = false;
  editingAgent.value = null;
  agentForm.value = {
    name: '',
    avatar: '🤖',
    ability: '',
    personality: '',
    description: '',
    public: true
  };
};

const saveAgent = async () => {
  if (!agentForm.value.name) return;
  try {
    if (editingAgent.value) {
      const result = await updateCustomAgent(editingAgent.value.id, agentForm.value);
      if (result.success) {
        const index = customAgents.value.findIndex(a => a.id === editingAgent.value.id);
        if (index !== -1) {
          customAgents.value[index] = { ...customAgents.value[index], ...result.data };
        }
      }
    } else {
      const result = await createCustomAgent(agentForm.value);
      if (result.success) {
        customAgents.value.push(result.data);
      }
    }
    closeAgentModal();
  } catch (error) {
    console.error('保存智能体失败:', error);
  }
};

const confirmDeleteAgent = (agent) => {
  confirmTitle.value = isEnglish.value ? 'Delete Agent' : '删除智能体';
  confirmMessage.value = isEnglish.value ? `Are you sure you want to delete ${agent.name}?` : `确定要删除智能体 ${agent.name} 吗？`;
  confirmAction.value = () => deleteAgentAction(agent.id);
  showConfirmModal.value = true;
};

const deleteAgentAction = async (agentId) => {
  try {
    const result = await deleteCustomAgent(agentId);
    if (result.success) {
      customAgents.value = customAgents.value.filter(a => a.id !== agentId);
    }
    showConfirmModal.value = false;
  } catch (error) {
    console.error('删除智能体失败:', error);
    showConfirmModal.value = false;
  }
};

const viewUserSessions = (user) => {
  adminTab.value = 'sessions';
  sessionFilterUser.value = user.id;
};

const viewUserContacts = async (user) => {
  adminTab.value = 'contacts';
  contactFilterUser.value = user.id;
};

const viewSessionHistory = async (sessionId) => {
  currentSessionId.value = sessionId;
  const chat = await getSessionHistory(sessionId);
  sessionHistoryMessages.value = chat?.messages || [];
  showSessionHistoryModal.value = true;
};

const closeSessionHistoryModal = () => {
  showSessionHistoryModal.value = false;
  sessionHistoryMessages.value = [];
  currentSessionId.value = '';
};

const deleteSession = async (sessionId) => {
  try {
    await deleteSessionApi(sessionId);
    await loadSessions();
  } catch (error) {
    console.error('删除会话失败:', error);
  }
};

const goBack = () => {
  router.push('/group');
};

const executeConfirmAction = () => {
  if (confirmAction.value) {
    confirmAction.value();
  }
};

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  return new Date(dateStr).toLocaleString('zh-CN');
};

const loadUsers = async () => {
  try {
    const users = await getUsers();
    allUsers.value = users;
  } catch (error) {
    console.error('加载用户列表失败:', error);
  }
};

const loadAgents = async () => {
  try {
    const agents = await getCustomAgents();
    customAgents.value = agents || [];
  } catch (error) {
    console.error('加载智能体列表失败:', error);
  }
};

const loadSessions = async () => {
  try {
    const sessions = await getAllSessions();
    allSessions.value = sessions;
  } catch (error) {
    console.error('加载会话列表失败:', error);
  }
};

const loadContacts = async () => {
  try {
    const friends = {};
    const groups = {};
    
    for (const user of allUsers.value) {
      friends[user.id] = await getUserFriends(user.id);
      groups[user.id] = await getUserGroups(user.id);
    }
    
    allFriends.value = friends;
    allGroups.value = groups;
  } catch (error) {
    console.error('加载联系人列表失败:', error);
  }
};

onMounted(async () => {
  await loadUsers();
  await loadAgents();
  await loadSessions();
  await loadContacts();
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
  flex-wrap: wrap;
  gap: 12px;
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

.search-bar.inline {
  margin-bottom: 0;
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
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
  max-width: 100%;
  overflow-x: hidden;
}

.user-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px;
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
  min-width: 0;
  overflow: hidden;
}

.user-info h3 {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-info p {
  font-size: 13px;
  color: #64748b;
  margin: 0 0 6px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
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

.action-btn.view-friends:hover {
  background: #dbeafe;
}

.action-btn.view-history:hover {
  background: #dcfce7;
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

.detail-actions {
  display: flex;
  gap: 12px;
  margin-top: 20px;
}

.view-sessions-btn, .view-contacts-btn {
  flex: 1;
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

.view-sessions-btn:hover, .view-contacts-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.view-contacts-btn {
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
}

.view-contacts-btn:hover {
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
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

.agent-name-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.visibility-badge {
  padding: 2px 8px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 500;
}

.visibility-badge.public {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.visibility-badge.private {
  background: rgba(249, 115, 22, 0.1);
  color: #f97316;
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

.session-table-container {
  overflow-x: auto;
}

.session-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.session-table thead {
  background: linear-gradient(135deg, #f0f6ff 0%, #e0e7ff 100%);
}

.session-table th, .session-table td {
  padding: 14px 16px;
  text-align: left;
  border-bottom: 1px solid #f1f5f9;
}

.session-table th {
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.session-table tbody tr:hover {
  background: #f8fafc;
}

.session-id-cell {
  font-family: monospace;
  font-size: 12px;
  color: #334155;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.type-badge {
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
}

.type-badge.agent {
  background: rgba(168, 85, 247, 0.1);
  color: #7c3aed;
}

.type-badge.friend {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}

.type-badge.group {
  background: rgba(249, 115, 22, 0.1);
  color: #f97316;
}

.type-badge.unknown {
  background: rgba(100, 116, 139, 0.1);
  color: #64748b;
}

.no-data {
  text-align: center;
  padding: 40px;
  color: #94a3b8;
  font-size: 14px;
}

.contacts-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.contacts-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
}

.tab-btn {
  padding: 10px 20px;
  border-radius: 10px;
  border: none;
  background: white;
  font-size: 14px;
  font-weight: 500;
  color: #64748b;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tab-btn:hover {
  background: #f1f5f9;
}

.tab-btn.active {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: white;
}

.friends-list, .groups-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.user-contacts {
  background: white;
  border-radius: 14px;
  overflow: hidden;
}

.user-contacts-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(135deg, #f0f6ff 0%, #e0e7ff 100%);
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
}

.user-contacts-header .count {
  font-size: 13px;
  color: #64748b;
  font-weight: normal;
}

.contact-cards {
  padding: 12px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
}

.contact-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 10px;
  background: #f8fafc;
}

.contact-avatar {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.contact-info h4 {
  font-size: 13px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 2px;
}

.contact-info p {
  font-size: 12px;
  color: #64748b;
  margin: 0;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-left: auto;
}

.status-dot.online {
  background: #10b981;
}

.status-dot.offline {
  background: #94a3b8;
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

.agent-modal {
  max-width: 560px;
}

.session-history-modal {
  max-width: 600px;
  max-height: 80vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
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

.history-body {
  flex: 1;
  overflow-y: auto;
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

.form-textarea {
  width: 100%;
  padding: 12px;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  font-size: 14px;
  outline: none;
  transition: all 0.3s ease;
  min-height: 80px;
  resize: vertical;
}

.form-textarea:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.visibility-options {
  display: flex;
  gap: 12px;
}

.visibility-option {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  border-radius: 10px;
  border: 2px solid #e2e8f0;
  cursor: pointer;
  transition: all 0.3s ease;
}

.visibility-option.selected {
  border-color: #3b82f6;
  background: rgba(59, 130, 246, 0.05);
}

.visibility-option input {
  display: none;
}

.visibility-option span {
  font-size: 14px;
  color: #334155;
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

.message-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message-item {
  display: flex;
  gap: 12px;
}

.message-item.user {
  flex-direction: row-reverse;
}

.message-item.user .message-content {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: white;
}

.message-item.user .message-name,
.message-item.user .message-time {
  color: rgba(255, 255, 255, 0.8);
}

.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  flex-shrink: 0;
}

.message-content {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 16px;
  background: #f1f5f9;
}

.message-name {
  font-size: 12px;
  font-weight: 500;
  color: #64748b;
  margin-bottom: 4px;
}

.message-text {
  font-size: 14px;
  color: #1e293b;
  line-height: 1.5;
}

.message-item.user .message-text {
  color: white;
}

.message-time {
  font-size: 11px;
  color: #94a3b8;
  margin-top: 4px;
  text-align: right;
}

.no-history {
  text-align: center;
  padding: 40px;
  color: #94a3b8;
  font-size: 14px;
}
</style>