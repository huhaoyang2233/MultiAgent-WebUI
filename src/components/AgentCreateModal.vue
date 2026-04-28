<template>
  <el-dialog 
    title="创建智能体" 
    :visible="visible" 
    width="500px"
    :before-close="handleClose"
  >
    <el-form :model="form" label-width="100px">
      <el-form-item label="智能体名称">
        <el-input 
          v-model="form.name" 
          placeholder="请输入智能体名称"
          class="form-input"
        />
        <span v-if="nameError" class="error-message">{{ nameError }}</span>
      </el-form-item>
      
      <el-form-item label="智能体头像">
        <div class="avatar-selector">
          <span 
            v-for="avatar in avatarOptions" 
            :key="avatar"
            :class="['avatar-option', { selected: form.avatar === avatar }]"
            @click="form.avatar = avatar"
          >
            {{ avatar }}
          </span>
        </div>
      </el-form-item>
      
      <el-form-item label="能力描述">
        <el-input 
          v-model="form.ability" 
          type="textarea" 
          :rows="3"
          placeholder="请描述智能体的能力"
          class="form-input"
        />
      </el-form-item>
      
      <el-form-item label="性格特点">
        <el-input 
          v-model="form.personality" 
          type="textarea" 
          :rows="2"
          placeholder="请描述智能体的性格特点"
          class="form-input"
        />
      </el-form-item>
      
      <el-form-item label="详细介绍">
        <el-input 
          v-model="form.description" 
          type="textarea" 
          :rows="4"
          placeholder="请详细介绍智能体"
          class="form-input"
        />
      </el-form-item>
    </el-form>
    
    <template #footer>
      <el-button @click="handleClose">取消</el-button>
      <el-button type="primary" @click="handleSubmit">创建</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { reactive, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  existingAgents: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['close', 'create'])

const avatarOptions = ['🤖', '💻', '📊', '📈', '🤝', '🎯', '💡', '🚀', '🌟', '🎨']

const form = reactive({
  name: '',
  avatar: '🤖',
  ability: '',
  personality: '',
  description: ''
})

const nameError = ref('')

watch(() => props.visible, (val) => {
  if (val) {
    form.name = ''
    form.avatar = '🤖'
    form.ability = ''
    form.personality = ''
    form.description = ''
    nameError.value = ''
  }
})

const handleClose = () => {
  emit('close')
}

const validateName = () => {
  if (!form.name.trim()) {
    nameError.value = '请输入智能体名称'
    return false
  }
  
  const exists = props.existingAgents.some(agent => 
    agent.name.toLowerCase() === form.name.trim().toLowerCase()
  )
  
  if (exists) {
    nameError.value = '该智能体名称已存在，请输入其他名称'
    return false
  }
  
  nameError.value = ''
  return true
}

const handleSubmit = () => {
  if (!validateName()) {
    return
  }
  
  if (!form.ability.trim()) {
    ElMessage.error('请描述智能体的能力')
    return
  }
  
  emit('create', { ...form })
  handleClose()
}
</script>

<style scoped>
.form-input {
  border-radius: 8px;
}

.error-message {
  color: #f56c6c;
  font-size: 12px;
  margin-top: 4px;
  display: block;
}

.avatar-selector {
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
</style>