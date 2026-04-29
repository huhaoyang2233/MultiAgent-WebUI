<template>
  <div class="agent-manager">
    <div class="manager-header">
      <h2>{{ isEnglish ? 'Agent Management' : '智能体管理' }}</h2>
      <button class="create-btn" @click="openCreateModal">
        <span class="btn-icon">+</span>
        <span>{{ isEnglish ? 'Create Agent' : '创建智能体' }}</span>
      </button>
    </div>

    <div class="agent-grid" v-if="customAgents.length > 0">
      <div 
        v-for="agent in customAgents" 
        :key="agent.id" 
        class="agent-card"
      >
        <div class="card-header">
          <div class="agent-avatar">{{ agent.avatar }}</div>
          <div class="agent-info">
            <h3 class="agent-name">{{ agent.name }}</h3>
            <span :class="['status-tag', agent.subscribed ? 'subscribed' : 'unsubscribed']">
              {{ agent.subscribed ? (isEnglish ? 'Subscribed' : '已订阅') : (isEnglish ? 'Unsubscribed' : '未订阅') }}
            </span>
          </div>
        </div>

        <div class="card-body">
          <div class="detail-row">
            <span class="detail-label">{{ isEnglish ? 'Ability' : '能力' }}</span>
            <p class="detail-value">{{ agent.ability }}</p>
          </div>
          <div class="detail-row">
            <span class="detail-label">{{ isEnglish ? 'Personality' : '性格' }}</span>
            <p class="detail-value">{{ agent.personality }}</p>
          </div>
          <div class="detail-row">
            <span class="detail-label">{{ isEnglish ? 'Description' : '介绍' }}</span>
            <p class="detail-value">{{ agent.description }}</p>
          </div>
        </div>

        <div class="card-footer">
          <span class="create-time">{{ isEnglish ? 'Created at' : '创建于' }} {{ formatDate(agent.createdAt) }}</span>
          <div class="card-actions">
            <button 
              v-if="!agent.subscribed"
              class="action-btn primary"
              @click="handleSubscribe(agent.id)"
            >
              {{ isEnglish ? 'Subscribe' : '订阅' }}
            </button>
            <button 
              v-else
              class="action-btn default"
              @click="handleSubscribe(agent.id)"
            >
              {{ isEnglish ? 'Unsubscribe' : '取消订阅' }}
            </button>
            <button 
              v-if="agent.subscribed"
              class="action-btn success"
              @click="handleChat(agent)"
            >
              {{ isEnglish ? 'Chat' : '聊天' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <div class="empty-icon">🤖</div>
      <p>{{ isEnglish ? 'No custom agents yet' : '暂无自定义智能体' }}</p>
      <button class="create-btn" @click="openCreateModal">
        {{ isEnglish ? 'Create Your First Agent' : '创建第一个智能体' }}
      </button>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ isEnglish ? 'Create New Agent' : '创建智能体' }}</h3>
          <button class="close-btn" @click="closeModal">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>{{ isEnglish ? 'Agent Name' : '智能体名称' }}</label>
            <input 
              v-model="form.name" 
              :placeholder="isEnglish ? 'Enter agent name' : '请输入智能体名称'"
              class="form-input"
              @blur="validateName"
            />
            <span v-if="nameError" class="error-text">{{ nameError }}</span>
          </div>
          
          <div class="form-group">
            <label>{{ isEnglish ? 'Avatar' : '智能体头像' }}</label>
            <div class="avatar-options">
              <span 
                v-for="avatar in avatarOptions" 
                :key="avatar"
                :class="['avatar-option', { selected: form.avatar === avatar }]"
                @click="form.avatar = avatar"
              >
                {{ avatar }}
              </span>
            </div>
          </div>
          
          <div class="form-group">
            <label>{{ isEnglish ? 'Ability' : '能力描述' }}</label>
            <textarea 
              v-model="form.ability" 
              :placeholder="isEnglish ? 'Describe agent abilities' : '请描述智能体的能力'"
              class="form-textarea"
            ></textarea>
          </div>
          
          <div class="form-group">
            <label>{{ isEnglish ? 'Personality' : '性格特点' }}</label>
            <textarea 
              v-model="form.personality" 
              :placeholder="isEnglish ? 'Describe agent personality' : '请描述智能体的性格特点'"
              class="form-textarea"
            ></textarea>
          </div>
          
          <div class="form-group">
            <label>{{ isEnglish ? 'Description' : '详细介绍' }}</label>
            <textarea 
              v-model="form.description" 
              :placeholder="isEnglish ? 'Detailed introduction' : '请详细介绍智能体'"
              class="form-textarea"
            ></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="modal-btn cancel" @click="closeModal">{{ isEnglish ? 'Cancel' : '取消' }}</button>
          <button class="modal-btn confirm" @click="handleSubmit">{{ isEnglish ? 'Create' : '创建' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { storeToRefs } from 'pinia';
import { useChatStore } from '../stores/chatStore';
import { getCustomAgents, createCustomAgent } from '../services/chatApi';

const chatStore = useChatStore();
const { customAgents } = storeToRefs(chatStore);
const isEnglish = computed(() => chatStore.isEnglish);
const showModal = ref(false);
const nameError = ref('');
const avatarOptions = ['🤖', '💻', '📊', '📈', '🤝', '🎯', '💡', '🚀', '🌟', '🎨'];
const form = reactive({
 name: '',
 avatar: '🤖',
 ability: '',
 personality: '',
 description: ''
});

onMounted(async () => {
  const agents = await getCustomAgents();
  agents.forEach(agent => {
    const exists = customAgents.value.some(a => a.id === agent.id);
    if (!exists) {
      chatStore.addCustomAgent(agent);
    }
  });
});

const openCreateModal = () => {
 showModal.value = true;
 resetForm();
};
const closeModal = () => {
 showModal.value = false;
 nameError.value = '';
};
const resetForm = () => {
 form.name = '';
 form.avatar = '🤖';
 form.ability = '';
 form.personality = '';
 form.description = '';
};
const validateName = () => {
 if (!form.name.trim()) {
 nameError.value = isEnglish.value ? 'Please enter agent name' : '请输入智能体名称';
 return false;
 }
 const exists = customAgents.value.some(agent => agent.name.toLowerCase() === form.name.trim().toLowerCase());
 if (exists) {
 nameError.value = isEnglish.value ? 'Agent name already exists' : '该智能体名称已存在';
 return false;
 }
 nameError.value = '';
 return true;
};
const handleSubmit = async () => {
 if (!validateName())
 return;
 if (!form.ability.trim()) {
 alert(isEnglish.value ? 'Please describe agent abilities' : '请描述智能体的能力');
 return;
 }
 const result = await createCustomAgent({ ...form });
 if (result.success) {
   chatStore.addCustomAgent(result.data);
   closeModal();
   alert(isEnglish.value ? 'Agent created successfully' : '智能体创建成功');
 } else {
   alert(result.message || (isEnglish.value ? 'Failed to create agent' : '创建失败'));
 }
};
const handleSubscribe = async (agentId) => {
 await chatStore.toggleSubscribeAgent(agentId);
};
const handleChat = (agent) => {
 const friend = chatStore.friends.find(f => f.name === agent.name);
 if (friend) {
 chatStore.selectFriend(friend.id);
 chatStore.setCurrentView('chat');
 }
};
const formatDate = (dateStr) => {
 if (!dateStr)
 return '';
 const date = new Date(dateStr);
 return date.toLocaleDateString('zh-CN');
};
</script>

<style scoped>
.agent-manager {
  padding: 24px;
  height: 100%;
  overflow-y: auto;
}

.manager-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.manager-header h2 {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.create-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  border-radius: 8px;
  border: none;
  background: linear-gradient(135deg, #409EFF 0%, #67C23A 100%);
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.create-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.btn-icon {
  font-size: 18px;
  font-weight: bold;
}

.agent-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.agent-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.agent-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(64, 158, 255, 0.15);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 20px;
  background: linear-gradient(135deg, #409EFF 0%, #67C23A 100%);
}

.agent-avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
}

.agent-info {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.agent-name {
  font-size: 18px;
  font-weight: 600;
  color: white;
  margin: 0;
}

.status-tag {
  font-size: 12px;
  padding: 3px 10px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  width: fit-content;
}

.status-tag.subscribed {
  background: rgba(103, 194, 58, 0.8);
}

.status-tag.unsubscribed {
  background: rgba(255, 153, 0, 0.8);
}

.card-body {
  padding: 16px 20px;
}

.detail-row {
  margin-bottom: 12px;
}

.detail-row:last-child {
  margin-bottom: 0;
}

.detail-label {
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
  display: block;
}

.detail-value {
  font-size: 14px;
  color: #606266;
  margin: 0;
  line-height: 1.5;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 20px;
  background: #fafafa;
  border-top: 1px solid #f0f0f0;
}

.create-time {
  font-size: 12px;
  color: #909399;
}

.card-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  padding: 6px 14px;
  border-radius: 6px;
  border: none;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn.primary {
  background: linear-gradient(135deg, #409EFF 0%, #67C23A 100%);
  color: white;
}

.action-btn.default {
  background: #f5f7fa;
  color: #606266;
}

.action-btn.success {
  background: #67C23A;
  color: white;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-state p {
  font-size: 16px;
  color: #909399;
  margin: 0 0 20px;
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
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #f0f0f0;
}

.modal-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.close-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: #f5f7fa;
  font-size: 20px;
  color: #909399;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  background: #e4e7ed;
}

.modal-body {
  padding: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #606266;
  margin-bottom: 8px;
}

.form-input {
  width: 100%;
  padding: 10px 14px;
  border-radius: 8px;
  border: 1px solid #dcdfe6;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.form-input:focus {
  border-color: #409EFF;
}

.error-text {
  display: block;
  font-size: 12px;
  color: #f56c6c;
  margin-top: 4px;
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
  background: linear-gradient(135deg, #409EFF 0%, #67C23A 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 3px solid transparent;
}

.avatar-option:hover {
  transform: scale(1.1);
  border-color: #409EFF;
}

.avatar-option.selected {
  border-color: #409EFF;
  box-shadow: 0 0 0 4px rgba(64, 158, 255, 0.2);
}

.form-textarea {
  width: 100%;
  padding: 10px 14px;
  border-radius: 8px;
  border: 1px solid #dcdfe6;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s ease;
  resize: vertical;
  min-height: 80px;
  box-sizing: border-box;
}

.form-textarea:focus {
  border-color: #409EFF;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid #f0f0f0;
}

.modal-btn {
  padding: 10px 24px;
  border-radius: 8px;
  border: none;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.modal-btn.cancel {
  background: #f5f7fa;
  color: #606266;
}

.modal-btn.cancel:hover {
  background: #e4e7ed;
}

.modal-btn.confirm {
  background: linear-gradient(135deg, #409EFF 0%, #67C23A 100%);
  color: white;
}

.modal-btn.confirm:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}
</style>