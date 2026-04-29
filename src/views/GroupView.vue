<template>
  <div class="group-container">
    <Header />
    
    <div class="group-main">
      <aside class="nav-sidebar">
        <nav class="nav-menu">
          <div 
            :class="['nav-item', { active: currentView === 'chat' }]"
            @click="setCurrentView('chat')"
          >
            <span class="nav-icon">💬</span>
            <span>{{ isEnglish ? 'Chat' : '聊天' }}</span>
            <span v-if="unreadCount > 0" class="unread-badge">{{ unreadCount }}</span>
          </div>
          <div 
            :class="['nav-item', { active: currentView === 'contacts' }]"
            @click="setCurrentView('contacts')"
          >
            <span class="nav-icon">📒</span>
            <span>{{ isEnglish ? 'Contacts' : '通讯录' }}</span>
          </div>
          <div 
            :class="['nav-item', { active: currentView === 'agents' }]"
            @click="setCurrentView('agents')"
          >
            <span class="nav-icon">🤖</span>
            <span>{{ isEnglish ? 'Agents' : '智能体管理' }}</span>
          </div>
          <div 
            :class="['nav-item', { active: currentView === 'settings' }]"
            @click="setCurrentView('settings')"
          >
            <span class="nav-icon">⚙️</span>
            <span>{{ isEnglish ? 'Settings' : '设置' }}</span>
          </div>
        </nav>
      </aside>

      <aside v-if="currentView === 'chat'" class="contact-sidebar">
        <div class="chat-header-bar">
          <h3>{{ isEnglish ? 'Recent Chats' : '最近聊天' }}</h3>
          <span class="unread-total">{{ unreadCount }} {{ isEnglish ? 'unread' : '未读' }}</span>
        </div>

        <div class="search-bar">
          <el-input 
            v-model="searchText" 
            :placeholder="isEnglish ? 'Search friends or groups...' : '搜索好友或群聊...'"
            class="search-input"
          />
        </div>

        <div class="contact-list">
          <div 
            v-for="session in filteredSessions" 
            :key="session.session_id"
            :class="['contact-item', { active: isSessionActive(session) }]"
            @click="selectSession(session)"
          >
            <div class="avatar-wrapper">
              <span class="avatar-text">{{ getSessionAvatar(session) }}</span>
              <span v-if="session.chat_type === 'agent' || session.chat_type === 'friend'" :class="['status-dot', getSessionStatus(session)]"></span>
            </div>
            <div class="contact-info">
              <div class="group-header">
                <span class="contact-name">{{ getSessionName(session) }}</span>
                <span v-if="getSessionUnread(session) > 0" class="unread-badge">{{ getSessionUnread(session) }}</span>
              </div>
              <span class="contact-status">{{ getSessionSubtitle(session) }}</span>
            </div>
          </div>
        </div>
      </aside>

      <main class="main-content">
        <div v-if="currentView === 'chat'" class="chat-area">
          <div v-if="!currentSelectedFriendId && !currentGroupId" class="empty-chat">
            <div class="empty-icon">💬</div>
            <h3>{{ isEnglish ? 'Select a friend or group' : '选择一个好友或群聊' }}</h3>
            <p>{{ isEnglish ? 'Start your conversation' : '开始您的对话之旅' }}</p>
          </div>

          <div v-else class="chat-window">
            <div class="chat-header">
              <div class="chat-info">
                <span class="chat-avatar">{{ currentChatTarget?.avatar }}</span>
                <div class="chat-meta">
                  <h3 class="chat-title">{{ currentChatTarget?.name }}</h3>
                  <span class="chat-subtitle">{{ currentChatSubtitle }}</span>
                </div>
              </div>
              <div class="chat-actions">
                <button class="action-btn">📞</button>
                <button class="action-btn">📹</button>
                <button class="action-btn">⋮</button>
              </div>
            </div>

            <div class="message-list">
              <div 
                v-for="msg in currentMessagesList" 
                :key="msg.id"
                :class="['message-item', { 'is-user': msg.role === 'user' }]"
              >
                <span class="message-avatar">{{ msg.role === 'user' ? '👤' : currentChatTarget?.avatar }}</span>
                <div class="message-content">
                  <span class="message-name" v-if="msg.role !== 'user'">{{ msg.name || currentChatTarget?.name }}</span>
                  <div class="message-bubble">
                    {{ msg.content }}
                  </div>
                  <span class="message-time">{{ msg.timestamp }}</span>
                </div>
              </div>
            </div>

            <div class="input-area">
              <div class="input-wrapper">
                <span class="input-icon">😊</span>
                <input 
                  v-model="inputMessage"
                  :placeholder="isEnglish ? 'Type a message...' : '输入消息...'"
                  class="message-input"
                  @keydown.enter.exact="sendMessage"
                />
              </div>
              <div class="input-actions">
                <button class="input-action-btn">🖼️</button>
                <button class="input-action-btn">📎</button>
                <button class="send-btn" @click="sendMessage">{{ isEnglish ? 'Send' : '发送' }}</button>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="currentView === 'agents'" class="agents-area">
          <AgentManager />
        </div>

        <div v-else-if="currentView === 'contacts'" class="contacts-area">
          <div class="contacts-layout">
            <div class="contacts-left">
              <div class="contacts-tabs">
                <span 
                  :class="['contacts-tab', { active: contactsTab === 'agents' }]"
                  @click="setContactsTab('agents')"
                >
                  🤖 {{ isEnglish ? 'AI Agents' : 'AI智能体' }}
                </span>
                <span 
                  :class="['contacts-tab', { active: contactsTab === 'groups' }]"
                  @click="setContactsTab('groups')"
                >
                  👥 {{ isEnglish ? 'Groups' : '群聊' }}
                </span>
                <span 
                  :class="['contacts-tab', { active: contactsTab === 'users' }]"
                  @click="setContactsTab('users')"
                >
                  👤 {{ isEnglish ? 'Users' : '用户好友' }}
                </span>
              </div>
              
              <button class="create-group-btn" @click="showCreateGroupModal = true">
                ➕ {{ isEnglish ? 'Create Group' : '创建群聊' }}
              </button>
              
              <div class="contacts-search">
                <input 
                  v-model="contactsSearchText"
                  :placeholder="isEnglish ? 'Search...' : '搜索...'"
                  class="search-input"
                />
              </div>
              
              <div class="contacts-list">
                <div 
                  v-for="item in filteredContacts" 
                  :key="item.id"
                  :class="['contacts-list-item', { active: selectedContact?.id === item.id }]"
                  @click="selectContact(item)"
                >
                  <div class="list-avatar">{{ item.avatar }}</div>
                  <div class="list-info">
                    <span class="list-name">{{ item.name }}</span>
                    <span class="list-desc">
                      {{ item.type === 'ai' ? (isEnglish ? 'AI Assistant' : 'AI助手') : 
                         item.type === 'group' ? (item.memberCount + ' ' + (isEnglish ? 'members' : '名成员')) :
                         (item.status === 'online' ? (isEnglish ? 'Online' : '在线') : (isEnglish ? 'Offline' : '离线')) }}
                    </span>
                  </div>
                  <button 
                    class="delete-btn" 
                    @click.stop="deleteConversation(item)"
                    :title="isEnglish ? 'Delete conversation' : '删除会话'"
                  >
                    🗑️
                  </button>
                </div>
                
                <div v-if="filteredContacts.length === 0" class="empty-list">
                  <p>{{ isEnglish ? 'No contacts found' : '没有找到联系人' }}</p>
                </div>
              </div>
            </div>
            
            <div class="contacts-right">
              <div v-if="selectedContact" class="contact-detail">
                <div class="detail-card">
                  <div class="avatar-section">
                    <div class="detail-avatar-wrapper">
                      <div class="detail-avatar">{{ selectedContact.avatar }}</div>
                      <span v-if="selectedContact.type !== 'group'" :class="['status-indicator', selectedContact.status || 'online']"></span>
                    </div>
                    <div class="detail-info">
                      <h2 class="detail-name">{{ selectedContact.name }}</h2>
                      <div class="detail-meta">
                        <span :class="['type-badge', selectedContact.type]">
                          {{ selectedContact.type === 'ai' ? (isEnglish ? 'AI' : 'AI助手') : 
                             selectedContact.type === 'group' ? (isEnglish ? 'Group' : '群聊') : 
                             (isEnglish ? 'User' : '用户') }}
                        </span>
                        <span v-if="selectedContact.type !== 'group'" class="status-text">
                          {{ selectedContact.status === 'online' ? (isEnglish ? 'Online' : '在线') : (isEnglish ? 'Offline' : '离线') }}
                        </span>
                      </div>
                    </div>
                  </div>
                  
                  <div v-if="selectedContact.type === 'ai'" class="detail-section">
                    <div class="section-header">
                      <span class="section-icon">📋</span>
                      <h4>{{ isEnglish ? 'Description' : '描述' }}</h4>
                    </div>
                    <p class="description-text">{{ getAiRoleDesc(selectedContact.roleId) || (isEnglish ? 'No description available' : '暂无描述') }}</p>
                  </div>
                  
                  <div v-if="selectedContact.type === 'ai'" class="detail-section">
                    <div class="section-header">
                      <span class="section-icon">✨</span>
                      <h4>{{ isEnglish ? 'Abilities' : '能力' }}</h4>
                    </div>
                    <div class="abilities-tags">
                      <span class="ability-tag">{{ getAiAbility(selectedContact.roleId) }}</span>
                    </div>
                  </div>
                  
                  <div v-if="selectedContact.type === 'group'" class="detail-section">
                    <div class="section-header">
                      <span class="section-icon">👥</span>
                      <h4>{{ isEnglish ? 'Members' : '成员' }}</h4>
                      <span class="member-count">{{ selectedContact.memberCount }} {{ isEnglish ? 'members' : '名成员' }}</span>
                    </div>
                    <div class="members-grid">
                      <div 
                        v-for="(memberId, index) in selectedContact.members" 
                        :key="index"
                        class="member-card"
                      >
                        <span class="member-avatar">{{ getMemberAvatar(memberId) }}</span>
                        <span class="member-name">{{ getMemberName(memberId) }}</span>
                      </div>
                    </div>
                  </div>
                  
                  <div v-if="selectedContact.type === 'user'" class="detail-section">
                    <div class="section-header">
                      <span class="section-icon">📅</span>
                      <h4>{{ isEnglish ? 'Joined' : '加入时间' }}</h4>
                    </div>
                    <p class="joined-date">{{ selectedContact.createdAt || (isEnglish ? 'Unknown' : '未知') }}</p>
                  </div>
                  
                  <div class="detail-actions">
                    <button class="action-btn primary" @click="startChat(selectedContact)">
                      <span class="btn-icon">💬</span>
                      {{ isEnglish ? 'Start Chat' : '发起聊天' }}
                    </button>
                    <button v-if="selectedContact.type === 'group'" class="action-btn secondary">
                      <span class="btn-icon">👋</span>
                      {{ isEnglish ? 'Invite Members' : '邀请成员' }}
                    </button>
                    <button v-if="selectedContact.type !== 'group'" class="action-btn outline">
                      <span class="btn-icon">🔔</span>
                      {{ isEnglish ? 'Notifications' : '通知设置' }}
                    </button>
                  </div>
                </div>
              </div>
              
              <div v-else class="empty-detail">
                <div class="empty-icon">👤</div>
                <p>{{ isEnglish ? 'Select a contact' : '选择一个联系人' }}</p>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="currentView === 'settings'" class="settings-area">
          <div class="settings-container">
            <h2>{{ isEnglish ? 'Settings' : '设置' }}</h2>
            <div class="settings-section">
              <h3>{{ isEnglish ? 'Profile' : '个人信息' }}</h3>
              <div class="settings-item">
                <label>{{ isEnglish ? 'Username' : '用户名' }}</label>
                <el-input :value="userInfo?.username" disabled />
              </div>
              <div class="settings-item">
                <label>{{ isEnglish ? 'Avatar' : '头像' }}</label>
                <div class="avatar-preview">
                  <img :src="userInfo?.avatar || 'https://i.pravatar.cc/80'" :alt="isEnglish ? 'Avatar' : '头像'" />
                </div>
              </div>
            </div>
            <div class="settings-section">
              <h3>{{ isEnglish ? 'Notifications' : '通知设置' }}</h3>
              <div class="settings-item">
                <label>{{ isEnglish ? 'Message Notifications' : '消息通知' }}</label>
                <el-switch v-model="notifications" />
              </div>
              <div class="settings-item">
                <label>{{ isEnglish ? 'Sound' : '声音提醒' }}</label>
                <el-switch v-model="soundEnabled" />
              </div>
            </div>
            <div v-if="isAdmin" class="settings-section admin-section">
              <h3>{{ isEnglish ? 'Admin Panel' : '后台管理' }}</h3>
              <button class="admin-btn" @click="openAdminPanel">
                <span class="admin-icon">⚙️</span>
                {{ isEnglish ? 'Open Admin Panel' : '进入后台管理' }}
              </button>
            </div>
          </div>
        </div>
      </main>

      <aside v-if="currentView === 'chat'" class="info-panel" :style="{ width: infoPanelWidth + 'px' }">
        <div class="resize-handle" @mousedown="startResize"></div>
        <div v-if="currentSelectedFriendId" class="friend-info">
          <div class="info-header">
            <h3>{{ isEnglish ? 'Friend Info' : '好友信息' }}</h3>
          </div>
          <div class="info-content">
            <div class="info-avatar">{{ currentFriend?.avatar }}</div>
            <h4 class="info-name">{{ currentFriend?.name }}</h4>
            <p class="info-type">{{ currentFriend?.type === 'ai' ? (isEnglish ? 'AI Assistant' : 'AI助手') : (isEnglish ? 'User' : '普通用户') }}</p>
            <p class="info-status" :class="currentFriend?.status">
              {{ currentFriend?.status === 'online' ? (isEnglish ? 'Online' : '在线') : (isEnglish ? 'Offline' : '离线') }}
            </p>
            <div v-if="currentFriend?.type === 'ai'" class="info-desc">
              <p>{{ getAiRoleDesc(currentFriend?.roleId) }}</p>
            </div>
            <div class="info-actions">
              <button class="action-btn send-message-btn" @click="startChatWithFriend(currentFriend)">
                <span class="btn-icon">💬</span>
                <span class="btn-text">{{ isEnglish ? 'Send Message' : '发消息' }}</span>
              </button>
              <button class="action-btn delete-friend-btn" @click="confirmDeleteFriend(currentFriend)">
                <span class="btn-icon">🗑️</span>
                <span class="btn-text">{{ isEnglish ? 'Remove' : '删除' }}</span>
              </button>
            </div>
          </div>
        </div>

        <div v-else-if="currentGroupId" class="group-info">
          <div class="info-header">
            <h3>{{ isEnglish ? 'Group Info' : '群聊信息' }}</h3>
          </div>
          <div class="info-content">
            <div class="info-avatar">{{ currentGroup?.avatar }}</div>
            <h4 class="info-name">{{ currentGroup?.name }}</h4>
            <p class="info-member-count">{{ currentGroup?.memberCount }} {{ isEnglish ? 'members' : '名成员' }}</p>
            
            <div class="member-list">
              <h5>{{ isEnglish ? 'Members' : '群成员' }}</h5>
              <div 
                v-for="(memberId, index) in currentGroup?.members" 
                :key="index"
                class="member-item"
              >
                <span class="member-avatar">{{ getMemberAvatar(memberId) }}</span>
                <span class="member-name">{{ getMemberName(memberId) }}</span>
              </div>
            </div>

            <div class="group-info-actions">
              <button class="action-btn invite-btn">
                <span class="btn-icon">👥</span>
                <span class="btn-text">{{ isEnglish ? 'Invite' : '邀请' }}</span>
              </button>
              <button class="action-btn settings-btn">
                <span class="btn-icon">⚙️</span>
                <span class="btn-text">{{ isEnglish ? 'Settings' : '设置' }}</span>
              </button>
            </div>
          </div>
        </div>

        <div v-else class="empty-info">
          <span class="empty-icon">👤</span>
          <p>{{ isEnglish ? 'Select a chat to view info' : '选择聊天对象查看信息' }}</p>
        </div>
      </aside>
    </div>

    <div v-if="showCreateGroupModal" class="modal-overlay" @click.self="showCreateGroupModal = false">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ isEnglish ? 'Create New Group' : '创建新群聊' }}</h3>
          <button class="modal-close" @click="showCreateGroupModal = false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>{{ isEnglish ? 'Group Name' : '群聊名称' }}</label>
            <input 
              v-model="newGroupName" 
              :placeholder="isEnglish ? 'Enter group name' : '请输入群聊名称'" 
              class="modal-input"
            />
          </div>
          <div class="form-group">
            <label>{{ isEnglish ? 'Group Avatar' : '群聊头像' }}</label>
            <div class="avatar-options">
              <span 
                v-for="avatar in avatarOptions" 
                :key="avatar"
                :class="['avatar-option', { selected: newGroupAvatar === avatar }]"
                @click="newGroupAvatar = avatar"
              >{{ avatar }}</span>
            </div>
          </div>
          <div class="form-group">
            <label>{{ isEnglish ? 'Select Members' : '选择成员' }}</label>
            <div class="member-select">
              <div 
                v-for="friend in availableFriends" 
                :key="friend.id"
                :class="['member-option', { selected: selectedMembers.includes(friend.id) }]"
                @click="toggleMember(friend.id)"
              >
                <span class="member-avatar">{{ friend.avatar }}</span>
                <span class="member-name">{{ friend.name }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="modal-btn cancel" @click="showCreateGroupModal = false">
            {{ isEnglish ? 'Cancel' : '取消' }}
          </button>
          <button 
            class="modal-btn confirm" 
            @click="handleCreateGroup"
            :disabled="!newGroupName.trim() || selectedMembers.length === 0"
          >
            {{ isEnglish ? 'Create' : '创建' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useChatStore } from '../stores/chatStore'
import Header from '../components/Header.vue'
import AgentManager from '../components/AgentManager.vue'
import { chatWithAgent, chatWithFriend, chatInGroup, checkOrCreateSession, createGroup, getUserSessions, getChatHistory, deleteFriend } from '../services/chatApi'

const chatStore = useChatStore()

const { 
  friends, 
  groups, 
  currentSelectedFriendId, 
  currentGroupId, 
  currentFriend, 
  currentGroup, 
  currentFriendMessages, 
  currentGroupMessages,
  currentTab,
  currentView,
  aiRoles
} = storeToRefs(chatStore)

const searchText = ref('')
const inputMessage = ref('')
const notifications = ref(true)
const soundEnabled = ref(true)
const userInfo = ref(null)
const infoPanelWidth = ref(260)
const isEnglish = ref(false)
const contactsTab = ref('agents')
const contactsSearchText = ref('')
const selectedContact = ref(null)
const sessions = ref([])

const isAdmin = computed(() => userInfo.value?.role === 'admin')

const openAdminPanel = () => {
  window.location.href = '/admin'
}

const showCreateGroupModal = ref(false)
const newGroupName = ref('')
const newGroupAvatar = ref('👥')
const selectedMembers = ref([])
const avatarOptions = ['👥', '🤖', '📊', '💬', '👨‍👩‍👧', '🌍', '🏢', '🎯']

const availableFriends = computed(() => {
  return friends.value.filter(f => f.type === 'ai' || f.type === 'user')
})

const toggleMember = (friendId) => {
  const index = selectedMembers.value.indexOf(friendId)
  if (index > -1) {
    selectedMembers.value.splice(index, 1)
  } else {
    selectedMembers.value.push(friendId)
  }
}

const handleCreateGroup = async () => {
  if (!newGroupName.value.trim() || selectedMembers.value.length === 0) return
  
  try {
    const result = await createGroup(newGroupName.value, newGroupAvatar.value, selectedMembers.value)
    
    if (result) {
      const newGroup = {
        id: result.id,
        name: result.name,
        avatar: result.avatar,
        members: result.members,
        memberCount: result.member_count,
        unread: 0,
        createdAt: result.created_at
      }
      chatStore.groups.push(newGroup)
      showCreateGroupModal.value = false
      newGroupName.value = ''
      newGroupAvatar.value = '👥'
      selectedMembers.value = []
      
      if (typeof window !== 'undefined') {
        const ElMessage = await import('element-plus').then(m => m.ElMessage)
        ElMessage.success(isEnglish.value ? 'Group created successfully' : '群聊创建成功')
      }
    }
  } catch (error) {
    console.error('创建群聊失败:', error)
    if (typeof window !== 'undefined') {
      const ElMessage = await import('element-plus').then(m => m.ElMessage)
      ElMessage.error(isEnglish.value ? 'Failed to create group' : '创建群聊失败')
    }
  }
}

const startResize = (e) => {
  e.preventDefault()
  const startX = e.clientX
  const startWidth = infoPanelWidth.value
  
  const onMouseMove = (e) => {
    const deltaX = e.clientX - startX
    let newWidth = startWidth - deltaX
    newWidth = Math.max(200, Math.min(400, newWidth))
    infoPanelWidth.value = newWidth
  }
  
  const onMouseUp = () => {
    document.removeEventListener('mousemove', onMouseMove)
    document.removeEventListener('mouseup', onMouseUp)
  }
  
  document.addEventListener('mousemove', onMouseMove)
  document.addEventListener('mouseup', onMouseUp)
}

onMounted(async () => {
  const userInfoStr = localStorage.getItem('userInfo')
  if (userInfoStr) {
    userInfo.value = JSON.parse(userInfoStr)
  }
  
  const lang = localStorage.getItem('language')
  isEnglish.value = lang === 'en'
  
  await chatStore.initData()
  await loadSessions()
})

const aiFriends = computed(() => {
  return friends.value.filter(f => f.type === 'ai')
})

const userFriends = computed(() => {
  return friends.value.filter(f => f.type === 'user')
})

const unreadCount = computed(() => {
  return groups.value.reduce((sum, group) => sum + (group.unread || 0), 0)
})

const contactsList = computed(() => {
  if (contactsTab.value === 'agents') {
    return aiFriends.value.map(f => ({ ...f, type: 'ai' }))
  } else if (contactsTab.value === 'groups') {
    return groups.value.map(g => ({ ...g, type: 'group' }))
  } else {
    return userFriends.value.map(f => ({ ...f, type: 'user' }))
  }
})

const filteredContacts = computed(() => {
  if (!contactsSearchText.value) return contactsList.value
  const keyword = contactsSearchText.value.toLowerCase()
  return contactsList.value.filter(item => item.name.toLowerCase().includes(keyword))
})

const setContactsTab = (tab) => {
  contactsTab.value = tab
  selectedContact.value = null
}

const selectContact = (contact) => {
  selectedContact.value = contact
}

const startChat = (contact) => {
  if (contact.type === 'group') {
    chatStore.selectGroup(contact.id)
  } else {
    chatStore.selectFriend(contact.id)
  }
  chatStore.setCurrentView('chat')
}

const deleteConversation = (contact) => {
  if (contact.type === 'group') {
    chatStore.clearGroupMessages(contact.id)
  } else {
    chatStore.clearFriendMessages(contact.id)
  }
}

const startChatWithFriend = (friend) => {
  if (friend.type === 'ai') {
    chatStore.selectFriend(friend.id)
  } else {
    chatStore.selectFriend(friend.id)
  }
  chatStore.setCurrentView('chat')
}

const confirmDeleteFriend = async (friend) => {
  try {
    if (typeof window !== 'undefined') {
      const ElMessageBox = await import('element-plus').then(m => m.ElMessageBox)
      const ElMessage = await import('element-plus').then(m => m.ElMessage)
      await ElMessageBox.confirm(
        isEnglish.value
          ? `Are you sure you want to remove ${friend.name} from your friends?`
          : `确定要删除好友 ${friend.name} 吗？`,
        isEnglish.value ? 'Confirm Delete' : '确认删除',
        {
          confirmButtonText: isEnglish.value ? 'Delete' : '删除',
          cancelButtonText: isEnglish.value ? 'Cancel' : '取消',
          type: 'warning'
        }
      )
      await deleteFriend(friend.id)
      ElMessage.success(isEnglish.value ? 'Friend removed' : '已删除好友')
      if (currentSelectedFriendId.value === friend.id) {
        currentSelectedFriendId.value = null
      }
    }
  } catch {
  }
}

const handleContactClick = (friend) => {
  chatStore.selectFriend(friend.id)
  chatStore.setCurrentView('chat')
}

const handleGroupClick = (group) => {
  chatStore.selectGroup(group.id)
  chatStore.setCurrentView('chat')
}

const selectFriend = (friendId) => {
  chatStore.selectFriend(friendId)
}

const selectGroup = (groupId) => {
  chatStore.selectGroup(groupId)
}

const setCurrentTab = (tab) => {
  chatStore.setCurrentTab(tab)
}

const setCurrentView = async (view) => {
  console.log('setCurrentView called with view:', view)
  chatStore.setCurrentView(view)
  if (view === 'contacts') {
    console.log('Loading contacts data...')
    await chatStore.initData(true)
    await loadSessions()
    console.log('Contacts data loaded')
  }
}

const filteredFriends = computed(() => {
  if (!searchText.value) return friends.value
  const keyword = searchText.value.toLowerCase()
  return friends.value.filter(f => f.name.toLowerCase().includes(keyword))
})

const filteredGroups = computed(() => {
  if (!searchText.value) return groups.value
  const keyword = searchText.value.toLowerCase()
  return groups.value.filter(g => g.name.toLowerCase().includes(keyword))
})

const filteredSessions = computed(() => {
  let result = [...sessions.value]
  
  result.sort((a, b) => new Date(b.updated_at || 0) - new Date(a.updated_at || 0))
  
  if (!searchText.value) return result
  const keyword = searchText.value.toLowerCase()
  return result.filter(session => {
    const name = getSessionName(session)
    return name.toLowerCase().includes(keyword)
  })
})

const getSessionAvatar = (session) => {
  const targetId = session.target_id
  if (session.chat_type === 'agent' || session.chat_type === 'friend') {
    const friend = friends.value.find(f => f.id === targetId)
    return friend?.avatar || '👤'
  } else if (session.chat_type === 'group') {
    const group = groups.value.find(g => g.id === targetId)
    return group?.avatar || '👥'
  }
  return '👤'
}

const getSessionName = (session) => {
  const targetId = session.target_id
  if (session.chat_type === 'agent' || session.chat_type === 'friend') {
    const friend = friends.value.find(f => f.id === targetId)
    return friend?.name || targetId
  } else if (session.chat_type === 'group') {
    const group = groups.value.find(g => g.id === targetId)
    return group?.name || targetId
  }
  return targetId
}

const getSessionStatus = (session) => {
  const targetId = session.target_id
  if (session.chat_type === 'agent') {
    return 'online'
  } else if (session.chat_type === 'friend') {
    const friend = friends.value.find(f => f.id === targetId)
    return friend?.status || 'offline'
  }
  return 'online'
}

const getSessionUnread = (session) => {
  if (session.chat_type === 'group') {
    const group = groups.value.find(g => g.id === session.target_id)
    return group?.unread || 0
  }
  return 0
}

const getSessionSubtitle = (session) => {
  if (session.chat_type === 'agent') {
    return 'AI助手'
  } else if (session.chat_type === 'friend') {
    const friend = friends.value.find(f => f.id === session.target_id)
    return friend?.status === 'online' ? '在线' : '离线'
  } else if (session.chat_type === 'group') {
    const group = groups.value.find(g => g.id === session.target_id)
    return `${group?.memberCount || 0} 名成员`
  }
  return ''
}

const isSessionActive = (session) => {
  if (session.chat_type === 'agent' || session.chat_type === 'friend') {
    return currentSelectedFriendId.value === session.target_id
  } else if (session.chat_type === 'group') {
    return currentGroupId.value === session.target_id
  }
  return false
}

const selectSession = async (session) => {
  try {
    const history = await getChatHistory(session.chat_type, session.target_id)
    
    if (session.chat_type === 'agent' || session.chat_type === 'friend') {
      chatStore.selectFriend(session.target_id)
      if (history.messages && history.messages.length > 0) {
        const mappedMessages = history.messages.map(msg => ({
          id: msg.id,
          role: msg.role,
          name: msg.name,
          content: msg.content,
          timestamp: msg.timestamp ? new Date(msg.timestamp).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }) : ''
        }))
        chatStore.setFriendMessages(session.target_id, mappedMessages)
      } else {
        chatStore.setFriendMessages(session.target_id, [])
      }
    } else if (session.chat_type === 'group') {
      chatStore.selectGroup(session.target_id)
      if (history.messages && history.messages.length > 0) {
        const mappedMessages = history.messages.map(msg => ({
          id: msg.id,
          role: msg.role,
          name: msg.name,
          content: msg.content,
          timestamp: msg.timestamp ? new Date(msg.timestamp).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }) : ''
        }))
        chatStore.setGroupMessages(session.target_id, mappedMessages)
      } else {
        chatStore.setGroupMessages(session.target_id, [])
      }
    }
  } catch (error) {
    console.error('加载会话历史失败:', error)
    if (session.chat_type === 'agent' || session.chat_type === 'friend') {
      chatStore.selectFriend(session.target_id)
      chatStore.setFriendMessages(session.target_id, [])
    } else if (session.chat_type === 'group') {
      chatStore.selectGroup(session.target_id)
      chatStore.setGroupMessages(session.target_id, [])
    }
  }
}

const loadSessions = async () => {
  try {
    const result = await getUserSessions()
    sessions.value = result.sessions || []
  } catch (error) {
    console.error('加载会话列表失败:', error)
  }
}

const currentChatTarget = computed(() => {
  return currentFriend.value || currentGroup.value
})

const currentChatSubtitle = computed(() => {
  if (currentFriend.value) {
    return currentFriend.value.type === 'ai' ? 'AI助手' : (currentFriend.value.status === 'online' ? '在线' : '离线')
  }
  if (currentGroup.value) {
    return `${currentGroup.value.memberCount} 名成员`
  }
  return ''
})

const currentMessagesList = computed(() => {
  return currentFriend.value ? currentFriendMessages.value : currentGroupMessages.value
})

const getAiRoleDesc = (roleId) => {
  const role = aiRoles.value.find(r => r.id === roleId)
  return role?.description || ''
}

const getAiAbility = (roleId) => {
  const role = aiRoles.value.find(r => r.id === roleId)
  if (!role) return '通用助手'
  const abilities = {
    'role-1': '股票分析',
    'role-2': '产品经理',
    'role-3': '健康顾问',
    'role-4': '旅行助手'
  }
  return abilities[roleId] || role.name || '通用助手'
}

const getMemberAvatar = (memberId) => {
  const friend = friends.value.find(f => f.id === memberId)
  return friend?.avatar || '👤'
}

const getMemberName = (memberId) => {
  const friend = friends.value.find(f => f.id === memberId)
  return friend?.name || memberId
}

const sendMessage = async () => {
  if (!inputMessage.value.trim()) return
  
  const message = {
    id: Date.now(),
    role: 'user',
    name: '我',
    content: inputMessage.value.trim(),
    timestamp: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  }

  if (currentFriend.value) {
    chatStore.addFriendMessage(currentFriend.value.id, message)
  } else if (currentGroup.value) {
    chatStore.addGroupMessage(currentGroup.value.id, message)
  }

  inputMessage.value = ''

  try {
    if (currentFriend.value) {
      const chatType = currentFriend.value.type === 'ai' ? 'agent' : 'friend'
      await checkOrCreateSession(chatType, currentFriend.value.id)
    } else if (currentGroup.value) {
      await checkOrCreateSession('group', currentGroup.value.id)
    }
    
    let replyMessage
    if (currentFriend.value) {
      if (currentFriend.value.type === 'ai') {
        replyMessage = await chatWithAgent(currentFriend.value.id, message.content)
      } else {
        replyMessage = await chatWithFriend(currentFriend.value.id, message.content)
      }
      chatStore.addFriendMessage(currentFriend.value.id, {
        id: replyMessage.id,
        role: replyMessage.role,
        name: replyMessage.name,
        content: replyMessage.content,
        timestamp: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
      })
    } else if (currentGroup.value) {
      replyMessage = await chatInGroup(currentGroup.value.id, message.content)
      chatStore.addGroupMessage(currentGroup.value.id, {
        id: replyMessage.id,
        role: replyMessage.role,
        name: replyMessage.name,
        content: replyMessage.content,
        timestamp: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
      })
    }
    
    await loadSessions()
  } catch (error) {
    console.error('发送消息失败:', error)
  }
}
</script>

<style scoped>
.group-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f0f6ff;
}

.group-main {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.nav-sidebar {
  width: 90px;
  background: linear-gradient(180deg, #1e3a8a 0%, #1d4ed8 100%);
  display: flex;
  flex-direction: column;
  padding: 20px 0;
}

.nav-menu {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 16px 8px;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.3s ease;
  margin: 0 8px;
}

.nav-icon {
  font-size: 20px;
  margin-bottom: 4px;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.nav-item.active {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.unread-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  background: #ef4444;
  color: white;
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 16px;
  text-align: center;
}

.nav-item {
  position: relative;
}

.nav-item span {
  font-size: 11px;
  margin-top: 4px;
}

.contact-sidebar {
  width: 260px;
  background: white;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #e0e7ff;
}

.chat-header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #e0e7ff;
}

.chat-header-bar h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.unread-total {
  font-size: 13px;
  color: #ef4444;
  font-weight: 500;
}

.tab-header {
  display: flex;
  padding: 16px;
  gap: 8px;
  border-bottom: 1px solid #e0e7ff;
}

.tab-icon {
  font-size: 16px;
}

.tab {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  color: #64748b;
  transition: all 0.3s ease;
}

.tab:hover {
  background: #f0f6ff;
}

.tab.active {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: white;
}

.search-bar {
  padding: 12px;
}

.search-input {
  border-radius: 20px;
  background: #f0f6ff;
  border: 1px solid #e0e7ff;
}

.contact-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.contact-item:hover {
  background: #f0f6ff;
}

.contact-item.active {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(96, 165, 250, 0.1) 100%);
}

.avatar-wrapper {
  position: relative;
}

.avatar-text {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.status-dot {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid white;
}

.status-dot.online {
  background: #10b981;
}

.status-dot.offline {
  background: #9ca3af;
}

.contact-info {
  flex: 1;
  min-width: 0;
}

.group-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.contact-name {
  font-size: 15px;
  font-weight: 500;
  color: #1e293b;
}

.unread-badge {
  background: #ef4444;
  color: white;
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 18px;
  text-align: center;
}

.contact-status {
  font-size: 12px;
  color: #64748b;
  margin-top: 4px;
}

.main-content {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.empty-chat {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #64748b;
}

.empty-icon {
  margin-bottom: 20px;
}

.empty-chat h3 {
  font-size: 18px;
  font-weight: 500;
  color: #334155;
  margin: 0 0 8px;
}

.empty-chat p {
  font-size: 14px;
  color: #94a3b8;
  margin: 0;
}

.chat-window {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
}

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid #e0e7ff;
  background: #f8fafc;
}

.chat-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.chat-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
}

.chat-meta {
  display: flex;
  flex-direction: column;
}

.chat-title {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.chat-subtitle {
  font-size: 13px;
  color: #64748b;
}

.chat-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  background: #f1f5f9;
  color: #64748b;
}

.action-btn:hover {
  background: #e2e8f0;
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f8fafc;
}

.message-item {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.message-item.is-user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.message-content {
  max-width: 60%;
}

.message-name {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 4px;
  display: block;
}

.message-bubble {
  background: white;
  padding: 12px 16px;
  border-radius: 18px;
  font-size: 14px;
  line-height: 1.5;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.message-item.is-user .message-bubble {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: white;
}

.message-time {
  font-size: 12px;
  color: #94a3b8;
  margin-top: 4px;
  display: block;
}

.message-item.is-user .message-content {
  text-align: right;
}

.input-area {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  border-top: 1px solid #e0e7ff;
  background: white;
}

.input-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  background: #f0f6ff;
  border-radius: 24px;
  padding: 0 16px;
}

.input-icon {
  font-size: 20px;
  margin-right: 12px;
}

.message-input {
  flex: 1;
  border: none;
  background: transparent;
  padding: 12px 0;
  font-size: 14px;
  outline: none;
}

.message-input::placeholder {
  color: #94a3b8;
}

.input-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.input-action-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: #f1f5f9;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.input-action-btn:hover {
  background: #e2e8f0;
}

.action-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: #f1f5f9;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  background: #e2e8f0;
}

.send-btn {
  padding: 10px 20px;
  border-radius: 20px;
  border: none;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  border: none;
}

.agents-area {
  flex: 1;
  background: #f8fafc;
  overflow-y: auto;
}

.contacts-area {
  flex: 1;
  background: #f8fafc;
}

.contacts-layout {
  display: flex;
  height: 100%;
}

.contacts-left {
  width: 320px;
  background: white;
  border-right: 1px solid #e0e7ff;
  display: flex;
  flex-direction: column;
}

.contacts-tabs {
  display: flex;
  padding: 8px;
  gap: 4px;
  border-bottom: 1px solid #e0e7ff;
}

.contacts-tab {
  flex: 1;
  padding: 10px 8px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  color: #64748b;
  cursor: pointer;
  text-align: center;
  transition: all 0.3s ease;
}

.contacts-tab:hover {
  background: #f0f6ff;
}

.contacts-tab.active {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: white;
}

.contacts-search {
  padding: 12px;
}

.contacts-search .search-input {
  width: 100%;
  padding: 10px 16px;
  border-radius: 20px;
  border: 1px solid #e0e7ff;
  background: #f0f6ff;
  font-size: 13px;
  outline: none;
  transition: all 0.3s ease;
}

.contacts-search .search-input:focus {
  border-color: #3b82f6;
  background: white;
}

.contacts-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.contacts-list-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.contacts-list-item:hover {
  background: #f0f6ff;
}

.contacts-list-item.active {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
}

.list-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.list-info {
  flex: 1;
  min-width: 0;
}

.list-name {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.list-desc {
  display: block;
  font-size: 12px;
  color: #64748b;
  margin-top: 2px;
}

.delete-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: transparent;
  font-size: 14px;
  cursor: pointer;
  opacity: 0;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.contacts-list-item:hover .delete-btn {
  opacity: 1;
}

.delete-btn:hover {
  background: #fee2e2;
}

.empty-list {
  text-align: center;
  padding: 40px 20px;
  color: #94a3b8;
}

.empty-list p {
  margin: 0;
  font-size: 14px;
}

.contacts-right {
  flex: 1;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  background: linear-gradient(180deg, #f0f6ff 0%, #f8fafc 100%);
  padding: 40px;
  overflow-y: auto;
}

.contact-detail {
  width: 100%;
  max-width: 420px;
}

.detail-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 24px rgba(59, 130, 246, 0.08);
  overflow: hidden;
}

.avatar-section {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  padding: 32px;
  display: flex;
  align-items: center;
  gap: 20px;
}

.detail-avatar-wrapper {
  position: relative;
}

.detail-avatar {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  border: 4px solid rgba(255, 255, 255, 0.3);
}

.status-indicator {
  position: absolute;
  bottom: 4px;
  right: 4px;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border: 3px solid white;
}

.status-indicator.online {
  background: #10b981;
}

.status-indicator.offline {
  background: #9ca3af;
}

.detail-info {
  flex: 1;
}

.detail-name {
  font-size: 24px;
  font-weight: 700;
  color: white;
  margin: 0 0 8px;
}

.detail-meta {
  display: flex;
  align-items: center;
  gap: 10px;
}

.type-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.type-badge.ai {
  background: rgba(168, 85, 247, 0.3);
}

.type-badge.group {
  background: rgba(249, 115, 22, 0.3);
}

.type-badge.user {
  background: rgba(16, 185, 129, 0.3);
}

.status-text {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.8);
}

.detail-section {
  padding: 20px 24px;
  border-bottom: 1px solid #f1f5f9;
}

.detail-section:last-of-type {
  border-bottom: none;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.section-header h4 {
  font-size: 14px;
  font-weight: 600;
  color: #334155;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-icon {
  font-size: 16px;
}

.member-count {
  font-size: 12px;
  color: #94a3b8;
}

.description-text {
  font-size: 14px;
  color: #475569;
  line-height: 1.6;
  margin: 0;
}

.abilities-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.ability-tag {
  padding: 6px 14px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 500;
  background: linear-gradient(135deg, rgba(168, 85, 247, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
  color: #7c3aed;
}

.members-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.member-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 12px;
  border-radius: 12px;
  background: #f8fafc;
  transition: all 0.3s ease;
}

.member-card:hover {
  background: #f0f6ff;
}

.member-card .member-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.member-card .member-name {
  font-size: 12px;
  color: #475569;
  text-align: center;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.joined-date {
  font-size: 13px;
  color: #64748b;
  margin: 0;
}

.detail-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  padding: 20px 24px;
}

.action-btn {
  flex: 1;
  min-width: 140px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 16px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.action-btn.primary {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: white;
}

.action-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.35);
}

.action-btn.secondary {
  background: linear-gradient(135deg, #f97316 0%, #fb923c 100%);
  color: white;
}

.action-btn.secondary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(249, 115, 22, 0.35);
}

.action-btn.outline {
  background: transparent;
  border: 1.5px solid #e2e8f0;
  color: #64748b;
}

.action-btn.outline:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.btn-icon {
  font-size: 16px;
}



.empty-detail {
  text-align: center;
  color: #94a3b8;
}

.empty-detail .empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-detail p {
  font-size: 16px;
  margin: 0;
}

.settings-area {
  flex: 1;
  background: #f8fafc;
  padding: 32px;
}

.settings-container {
  max-width: 600px;
  margin: 0 auto;
}

.settings-container h2 {
  font-size: 24px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 24px;
}

.settings-section {
  background: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 20px;
}

.settings-section h3 {
  font-size: 16px;
  font-weight: 600;
  color: #334155;
  margin: 0 0 20px;
}

.settings-section.admin-section {
  background: linear-gradient(135deg, rgba(249, 115, 22, 0.05) 0%, rgba(245, 158, 11, 0.05) 100%);
  border: 1px solid rgba(249, 115, 22, 0.2);
}

.admin-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 14px 24px;
  border-radius: 12px;
  border: none;
  background: linear-gradient(135deg, #f97316 0%, #fb923c 100%);
  color: white;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.admin-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(249, 115, 22, 0.35);
}

.admin-icon {
  font-size: 18px;
}

.settings-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
  border-bottom: 1px solid #f1f5f9;
}

.settings-item:last-child {
  border-bottom: none;
}

.settings-item label {
  font-size: 14px;
  color: #475569;
}

.avatar-preview img {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  border: 3px solid #e0e7ff;
}

.info-panel {
  min-width: 200px;
  max-width: 400px;
  background: white;
  border-left: 1px solid #e0e7ff;
  overflow-y: auto;
  position: relative;
  flex-shrink: 0;
}

.resize-handle {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 6px;
  cursor: col-resize;
  background: transparent;
  z-index: 10;
}

.resize-handle:hover,
.resize-handle:active {
  background: #c0c4cc;
}

.resize-handle::before {
  content: '';
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 20px;
  height: 40px;
  background: #e0e7ff;
  border-radius: 10px;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.resize-handle:hover::before {
  opacity: 1;
}

.info-header {
  padding: 16px 20px;
  border-bottom: 1px solid #e0e7ff;
}

.info-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
}

.info-content {
  padding: 16px;
  text-align: center;
  box-sizing: border-box;
  overflow: hidden;
}

.info-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36px;
  margin: 0 auto 16px;
}

.info-name {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 8px;
}

.info-type, .info-status, .info-member-count {
  font-size: 13px;
  color: #64748b;
  margin: 0 0 8px;
}

.info-status.online {
  color: #10b981;
}

.info-desc {
  background: #f0f6ff;
  border-radius: 8px;
  padding: 12px;
  margin: 16px 0;
  text-align: left;
}

.info-desc p {
  font-size: 13px;
  color: #475569;
  margin: 0;
  line-height: 1.6;
}

.info-actions {
  display: flex;
  gap: 8px;
  margin-top: 16px;
  width: 100%;
  padding: 0;
}

.info-actions .action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 8px 8px;
  border-radius: 8px;
  border: none;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s ease;
  max-width: calc(50% - 4px);
  min-width: 0;
  word-break: keep-all;
}

.info-actions .send-message-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.25);
}

.info-actions .send-message-btn:hover {
  background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.35);
  transform: translateY(-1px);
}

.info-actions .send-message-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 6px rgba(59, 130, 246, 0.25);
}

.info-actions .delete-friend-btn {
  background: linear-gradient(135deg, #f87171 0%, #ef4444 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.25);
}

.info-actions .delete-friend-btn:hover {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.35);
  transform: translateY(-1px);
}

.info-actions .delete-friend-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 6px rgba(239, 68, 68, 0.25);
}

.info-actions .btn-icon {
  font-size: 14px;
}

.info-actions .btn-text {
  white-space: nowrap;
}

.group-info-actions {
  display: flex;
  gap: 8px;
  margin-top: 16px;
  width: 100%;
  padding: 0;
}

.group-info-actions .action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 8px 8px;
  border-radius: 8px;
  border: 1px solid #e0e7ff;
  background: white;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s ease;
  max-width: calc(50% - 4px);
  min-width: 0;
  word-break: keep-all;
}

.group-info-actions .invite-btn {
  color: #3b82f6;
}

.group-info-actions .invite-btn:hover {
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  border-color: #3b82f6;
}

.group-info-actions .settings-btn {
  color: #64748b;
}

.group-info-actions .settings-btn:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.group-info-actions .btn-icon {
  font-size: 14px;
}

.group-info-actions .btn-text {
  white-space: nowrap;
}

.member-list {
  margin-top: 16px;
  text-align: left;
}

.member-list h5 {
  font-size: 14px;
  font-weight: 600;
  color: #334155;
  margin: 0 0 12px;
}

.member-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 0;
}

.member-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}

.member-name {
  font-size: 14px;
  color: #334155;
}

.empty-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: #94a3b8;
}

.empty-info p {
  margin-top: 12px;
  font-size: 14px;
}

.create-group-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 16px;
  font-size: 13px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 0 12px 12px;
  transition: all 0.3s ease;
}

.create-group-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
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
  max-width: 500px;
  max-height: 80vh;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid #f1f5f9;
}

.modal-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #64748b;
  padding: 4px;
}

.modal-close:hover {
  color: #1e293b;
}

.modal-body {
  padding: 24px;
  max-height: 50vh;
  overflow-y: auto;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #334155;
  margin-bottom: 8px;
}

.modal-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.modal-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.avatar-options {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.avatar-option {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.avatar-option:hover {
  transform: scale(1.1);
}

.avatar-option.selected {
  border-color: #3b82f6;
  background: #dbeafe;
}

.member-select {
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
}

.member-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  border-bottom: 1px solid #f1f5f9;
}

.member-option:last-child {
  border-bottom: none;
}

.member-option:hover {
  background: #f8fafc;
}

.member-option.selected {
  background: #dbeafe;
}

.member-option .member-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #e0e7ff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}

.member-option .member-name {
  font-size: 14px;
  color: #334155;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px 24px;
  border-top: 1px solid #f1f5f9;
}

.modal-btn {
  padding: 10px 24px;
  border-radius: 8px;
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

.modal-btn.confirm:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.modal-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>