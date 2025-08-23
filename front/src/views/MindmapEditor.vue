<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 顶部工具栏 -->
    <div class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center space-x-4">
            <router-link
              to="/dashboard"
              class="text-gray-600 hover:text-gray-900"
            >
              ← 返回仪表板
            </router-link>
            <div class="border-l border-gray-300 h-6"></div>
            <h1 class="text-lg font-medium text-gray-900">
              {{ isEditing ? '编辑思维导图' : '创建思维导图' }}
            </h1>
          </div>
          
          <div class="flex items-center space-x-3">
            <span v-if="contentStore.saving" class="text-sm text-gray-600">
              保存中...
            </span>
            <span v-else-if="lastSaved" class="text-sm text-gray-600">
              已保存于 {{ lastSaved }}
            </span>
            
            <button
              @click="saveDraft"
              :disabled="contentStore.saving"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50"
            >
              保存草稿
            </button>
            
            <button
              @click="publishMindmap"
              :disabled="contentStore.saving || !canPublish"
              class="px-4 py-2 text-sm font-medium text-white bg-purple-600 border border-transparent rounded-md hover:bg-purple-700 disabled:opacity-50"
            >
              {{ currentMindmap?.status === 'published' ? '更新发布' : '发布思维导图' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <!-- 主编辑区域 -->
        <div class="lg:col-span-3">
          <div class="bg-white shadow rounded-lg">
            <!-- 思维导图标题 -->
            <div class="p-6 border-b border-gray-200">
              <input
                v-model="mindmapTitle"
                @input="markDirty"
                type="text"
                placeholder="请输入思维导图标题..."
                class="w-full text-2xl font-bold border-none outline-none resize-none placeholder-gray-400"
              />
            </div>
            
            <!-- 思维导图描述 -->
            <div class="p-6 border-b border-gray-200">
              <textarea
                v-model="mindmapDescription"
                @input="markDirty"
                placeholder="请输入思维导图描述（可选）..."
                rows="2"
                class="w-full border-none outline-none resize-none placeholder-gray-400"
              ></textarea>
            </div>

            <!-- 思维导图编辑器 -->
            <div class="p-6" style="height: 600px;">
              <MindmapEditor
                v-if="editorReady"
                v-model="mindmapContent"
              />
            </div>
          </div>
        </div>

        <!-- 侧边栏 -->
        <div class="lg:col-span-1">
          <div class="space-y-6">
            <!-- 发布设置 -->
            <div class="bg-white shadow rounded-lg p-6">
              <h3 class="text-lg font-medium text-gray-900 mb-4">发布设置</h3>
              
              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">状态</label>
                  <select
                    v-model="mindmapStatus"
                    @change="markDirty"
                    class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
                  >
                    <option value="draft">草稿</option>
                    <option value="published">已发布</option>
                    <option value="archived">已归档</option>
                  </select>
                </div>
              </div>
            </div>

            <!-- 标签管理 -->
            <div class="bg-white shadow rounded-lg p-6">
              <h3 class="text-lg font-medium text-gray-900 mb-4">标签</h3>
              
              <div class="space-y-3">
                <div v-if="selectedTags.length > 0" class="flex flex-wrap gap-2">
                  <span
                    v-for="tag in selectedTags"
                    :key="tag.id"
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800"
                  >
                    {{ tag.name }}
                    <button
                      @click="removeTag(tag.id)"
                      class="ml-1 text-purple-600 hover:text-purple-500"
                    >
                      ×
                    </button>
                  </span>
                </div>
                
                <select
                  v-model="selectedTagId"
                  @change="addTag"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
                >
                  <option value="">选择标签...</option>
                  <option
                    v-for="tag in availableTags"
                    :key="tag.id"
                    :value="tag.id"
                  >
                    {{ tag.name }}
                  </option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'
import { useContentStore } from '../stores/content.js'
import MindmapEditor from '../components/Mindmap/MindmapEditor.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const contentStore = useContentStore()

// 编辑器状态
const editorReady = ref(false)
const lastSaved = ref('')

// 思维导图数据
const mindmapTitle = ref('')
const mindmapDescription = ref('')
const mindmapContent = ref({})
const mindmapStatus = ref('draft')

// 标签管理
const selectedTags = ref([])
const selectedTagId = ref('')

// 计算属性
const isEditing = computed(() => !!route.params.id)
const currentMindmap = computed(() => contentStore.currentMindmap)

const canPublish = computed(() => {
  return mindmapTitle.value.trim() && 
         mindmapContent.value && 
         Object.keys(mindmapContent.value).length > 0
})

const availableTags = computed(() => {
  return contentStore.tags.filter(tag => 
    !selectedTags.value.some(selected => selected.id === tag.id)
  )
})

// 方法
const markDirty = () => {
  contentStore.markMindmapDirty()
}

const addTag = () => {
  if (selectedTagId.value) {
    const tag = contentStore.tags.find(t => t.id === parseInt(selectedTagId.value))
    if (tag && !selectedTags.value.some(t => t.id === tag.id)) {
      selectedTags.value.push(tag)
      selectedTagId.value = ''
      markDirty()
    }
  }
}

const removeTag = (tagId) => {
  selectedTags.value = selectedTags.value.filter(tag => tag.id !== tagId)
  markDirty()
}

const saveDraft = async () => {
  await saveMindmap('draft')
}

const publishMindmap = async () => {
  await saveMindmap('published')
}

const saveMindmap = async (status = null) => {
  if (!mindmapTitle.value.trim()) {
    alert('请输入思维导图标题')
    return
  }

  const mindmapData = {
    title: mindmapTitle.value,
    description: mindmapDescription.value,
    content: mindmapContent.value,
    status: status || mindmapStatus.value,
    tags: selectedTags.value.map(tag => tag.id)
  }

  if (isEditing.value) {
    mindmapData.id = parseInt(route.params.id)
  }

  const result = await contentStore.saveMindmap(mindmapData)
  
  if (result.success) {
    lastSaved.value = new Date().toLocaleTimeString()
    
    // 如果是新建思维导图，跳转到编辑页面
    if (!isEditing.value && result.data.id) {
      router.replace(`/mindmap/${result.data.id}/edit`)
    }
  } else {
    alert('保存失败：' + result.error)
  }
}

const loadMindmap = async () => {
  if (isEditing.value) {
    const result = await contentStore.loadMindmap(parseInt(route.params.id))
    if (result.success) {
      const mindmap = result.data
      mindmapTitle.value = mindmap.title
      mindmapDescription.value = mindmap.description || ''
      mindmapContent.value = mindmap.content || {}
      mindmapStatus.value = mindmap.status
      selectedTags.value = mindmap.tags || []
    } else {
      alert('加载思维导图失败：' + result.error)
      router.push('/dashboard')
    }
  } else {
    // 新建思维导图
    contentStore.createNewMindmap()
  }
  
  editorReady.value = true
}

const loadRelatedData = async () => {
  const userId = authStore.currentUser?.id
  if (userId) {
    await contentStore.loadTags(userId)
  }
}

onMounted(async () => {
  await loadRelatedData()
  await loadMindmap()
})

// 监听路由变化
watch(() => route.params.id, async (newId, oldId) => {
  if (newId !== oldId) {
    editorReady.value = false
    await loadMindmap()
  }
})
</script>

