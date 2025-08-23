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
              {{ isEditing ? '编辑文章' : '创建文章' }}
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
              @click="publishArticle"
              :disabled="contentStore.saving || !canPublish"
              class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md hover:bg-indigo-700 disabled:opacity-50"
            >
              {{ currentArticle?.status === 'published' ? '更新发布' : '发布文章' }}
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
            <!-- 文章标题 -->
            <div class="p-6 border-b border-gray-200">
              <input
                v-model="articleTitle"
                @input="markDirty"
                type="text"
                placeholder="请输入文章标题..."
                class="w-full text-2xl font-bold border-none outline-none resize-none placeholder-gray-400"
              />
            </div>
            
            <!-- 文章摘要 -->
            <div class="p-6 border-b border-gray-200">
              <textarea
                v-model="articleExcerpt"
                @input="markDirty"
                placeholder="请输入文章摘要（可选）..."
                rows="2"
                class="w-full border-none outline-none resize-none placeholder-gray-400"
              ></textarea>
            </div>

            <!-- TipTap 编辑器 -->
            <div class="p-6">
              <TipTapEditor
                v-if="editorReady"
                v-model="articleContent"
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
                    v-model="articleStatus"
                    @change="markDirty"
                    class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
                  >
                    <option value="draft">草稿</option>
                    <option value="published">已发布</option>
                    <option value="archived">已归档</option>
                  </select>
                </div>

                <div>
                  <label class="flex items-center">
                    <input
                      v-model="isTagArticle"
                      @change="markDirty"
                      type="checkbox"
                      class="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                    />
                    <span class="ml-2 text-sm text-gray-700">标签文章</span>
                  </label>
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
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800"
                  >
                    {{ tag.name }}
                    <button
                      @click="removeTag(tag.id)"
                      class="ml-1 text-indigo-600 hover:text-indigo-500"
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

            <!-- 关联内容 -->
            <div class="bg-white shadow rounded-lg p-6">
              <h3 class="text-lg font-medium text-gray-900 mb-4">关联内容</h3>
              
              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">关联路线图</label>
                  <select
                    v-model="linkedRoadmapId"
                    @change="markDirty"
                    class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
                  >
                    <option value="">无关联</option>
                    <option
                      v-for="roadmap in contentStore.roadmaps"
                      :key="roadmap.id"
                      :value="roadmap.id"
                    >
                      {{ roadmap.title }}
                    </option>
                  </select>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">关联思维导图</label>
                  <select
                    v-model="linkedMindmapId"
                    @change="markDirty"
                    class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
                  >
                    <option value="">无关联</option>
                    <option
                      v-for="mindmap in contentStore.mindmaps"
                      :key="mindmap.id"
                      :value="mindmap.id"
                    >
                      {{ mindmap.title }}
                    </option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'
import { useContentStore } from '../stores/content.js'
import TipTapEditor from '../components/Article/TipTapEditor.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const contentStore = useContentStore()

// 编辑器状态
const editorReady = ref(false)
const lastSaved = ref('')

// 文章数据
const articleTitle = ref('')
const articleExcerpt = ref('')
const articleContent = ref({})
const articleStatus = ref('draft')
const isTagArticle = ref(false)
const linkedRoadmapId = ref('')
const linkedMindmapId = ref('')

// 标签管理
const selectedTags = ref([])
const selectedTagId = ref('')

// 计算属性
const isEditing = computed(() => !!route.params.id)
const currentArticle = computed(() => contentStore.currentArticle)

const canPublish = computed(() => {
  return articleTitle.value.trim() && 
         articleContent.value && 
         Object.keys(articleContent.value).length > 0
})

const availableTags = computed(() => {
  return contentStore.tags.filter(tag => 
    !selectedTags.value.some(selected => selected.id === tag.id)
  )
})

// 方法
const markDirty = () => {
  contentStore.markArticleDirty()
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
  await saveArticle('draft')
}

const publishArticle = async () => {
  await saveArticle('published')
}

const saveArticle = async (status = null) => {
  if (!articleTitle.value.trim()) {
    alert('请输入文章标题')
    return
  }

  // 获取编辑器内容
  let contentToSave = articleContent.value
  
  // 确保内容是有效的格式
  if (!contentToSave || (typeof contentToSave === 'object' && Object.keys(contentToSave).length === 0)) {
    contentToSave = {
      type: 'doc',
      content: []
    }
  }

  const articleData = {
    title: articleTitle.value,
    content: contentToSave,
    excerpt: articleExcerpt.value,
    status: status || articleStatus.value,
    is_tag_article: isTagArticle.value,
    roadmap_id: linkedRoadmapId.value || null,
    mindmap_id: linkedMindmapId.value || null,
    tags: selectedTags.value.map(tag => tag.id)
  }

  if (isEditing.value) {
    articleData.id = parseInt(route.params.id)
  }

  const result = await contentStore.saveArticle(articleData)
  
  if (result.success) {
    lastSaved.value = new Date().toLocaleTimeString()
    
    // 如果是新建文章，跳转到编辑页面
    if (!isEditing.value && result.data.id) {
      router.replace(`/article/${result.data.id}/edit`)
    }
  } else {
    alert('保存失败：' + result.error)
  }
}

const loadArticle = async () => {
  if (isEditing.value) {
    const result = await contentStore.loadArticle(parseInt(route.params.id))
    if (result.success) {
      const article = result.data
      articleTitle.value = article.title
      articleExcerpt.value = article.excerpt || ''
      articleContent.value = article.content || {}
      articleStatus.value = article.status
      isTagArticle.value = article.is_tag_article
      linkedRoadmapId.value = article.roadmap_id || ''
      linkedMindmapId.value = article.mindmap_id || ''
      selectedTags.value = article.tags || []
    } else {
      alert('加载文章失败：' + result.error)
      router.push('/dashboard')
    }
  } else {
    // 新建文章
    contentStore.createNewArticle()
  }
  
  editorReady.value = true
}

const loadRelatedData = async () => {
  const userId = authStore.currentUser?.id
  if (userId) {
    await Promise.all([
      contentStore.loadTags(userId),
      contentStore.loadRoadmaps({ user_id: userId, status: '' }),
      contentStore.loadMindmaps({ user_id: userId, status: '' })
    ])
  }
}

// 页面离开前检查未保存的更改
const checkUnsavedChanges = () => {
  if (contentStore.hasUnsavedChanges) {
    return '您有未保存的更改，确定要离开吗？'
  }
}

onMounted(async () => {
  await loadRelatedData()
  await loadArticle()
})

onBeforeUnmount(() => {
  window.removeEventListener('beforeunload', checkUnsavedChanges)
})

// 监听路由变化
watch(() => route.params.id, async (newId, oldId) => {
  if (newId !== oldId) {
    editorReady.value = false
    await loadArticle()
  }
})

// 页面刷新前提醒
window.addEventListener('beforeunload', checkUnsavedChanges)
</script>

