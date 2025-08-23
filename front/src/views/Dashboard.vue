<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 导航栏 -->
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <router-link to="/" class="text-xl font-bold text-gray-900">个人博客系统</router-link>
          </div>
          <div class="flex items-center space-x-4">
            <span class="text-gray-700">欢迎，{{ authStore.currentUser?.display_name || authStore.currentUser?.username }}</span>
            <router-link
              to="/profile"
              class="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
            >
              个人资料
            </router-link>
            <button
              @click="handleLogout"
              class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium"
            >
              退出登录
            </button>
          </div>
        </div>
      </div>
    </nav>

    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- 页面标题 -->
      <div class="px-4 py-6 sm:px-0">
        <h1 class="text-3xl font-bold text-gray-900">仪表板</h1>
        <p class="mt-2 text-gray-600">管理您的文章、路线图和思维导图</p>
      </div>

      <!-- 快速操作 -->
      <div class="px-4 sm:px-0 mb-8">
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <router-link
            to="/article/new"
            class="bg-white overflow-hidden shadow rounded-lg hover:shadow-md transition-shadow"
          >
            <div class="p-6 text-center">
              <svg class="mx-auto h-12 w-12 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              <h3 class="mt-4 text-lg font-medium text-gray-900">创建文章</h3>
              <p class="mt-2 text-sm text-gray-600">使用富文本编辑器创建新文章</p>
            </div>
          </router-link>

          <router-link
            to="/roadmap/new"
            class="bg-white overflow-hidden shadow rounded-lg hover:shadow-md transition-shadow"
          >
            <div class="p-6 text-center">
              <svg class="mx-auto h-12 w-12 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              <h3 class="mt-4 text-lg font-medium text-gray-900">创建路线图</h3>
              <p class="mt-2 text-sm text-gray-600">设计交互式学习路线图</p>
            </div>
          </router-link>

          <router-link
            to="/mindmap/new"
            class="bg-white overflow-hidden shadow rounded-lg hover:shadow-md transition-shadow"
          >
            <div class="p-6 text-center">
              <svg class="mx-auto h-12 w-12 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              <h3 class="mt-4 text-lg font-medium text-gray-900">创建思维导图</h3>
              <p class="mt-2 text-sm text-gray-600">整理思路和知识结构</p>
            </div>
          </router-link>
        </div>
      </div>

      <!-- 内容管理标签页 -->
      <div class="px-4 sm:px-0">
        <div class="bg-white shadow rounded-lg">
          <!-- 标签页导航 -->
          <div class="border-b border-gray-200">
            <nav class="-mb-px flex space-x-8 px-6">
              <button
                v-for="tab in tabs"
                :key="tab.key"
                @click="activeTab = tab.key"
                :class="[
                  activeTab === tab.key
                    ? 'border-indigo-500 text-indigo-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                  'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm'
                ]"
              >
                {{ tab.name }}
                <span
                  v-if="getTabCount(tab.key) > 0"
                  :class="[
                    activeTab === tab.key ? 'bg-indigo-100 text-indigo-600' : 'bg-gray-100 text-gray-900',
                    'ml-2 py-0.5 px-2.5 rounded-full text-xs font-medium'
                  ]"
                >
                  {{ getTabCount(tab.key) }}
                </span>
              </button>
            </nav>
          </div>

          <!-- 标签页内容 -->
          <div class="p-6">
            <!-- 文章列表 -->
            <div v-if="activeTab === 'articles'">
              <div v-if="loading" class="text-center py-8">
                <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
                <p class="mt-2 text-gray-600">加载中...</p>
              </div>
              <div v-else-if="contentStore.articles.length === 0" class="text-center py-8">
                <p class="text-gray-600">还没有文章，<router-link to="/article/new" class="text-indigo-600 hover:text-indigo-500">创建第一篇文章</router-link></p>
              </div>
              <div v-else class="space-y-4">
                <div
                  v-for="article in contentStore.articles"
                  :key="article.id"
                  class="border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow"
                >
                  <div class="flex items-center justify-between">
                    <div class="flex-1">
                      <h3 class="text-lg font-medium text-gray-900">{{ article.title }}</h3>
                      <p class="mt-1 text-sm text-gray-600">{{ article.excerpt || '暂无摘要' }}</p>
                      <div class="mt-2 flex items-center space-x-4 text-sm text-gray-500">
                        <span :class="getStatusClass(article.status)">{{ getStatusText(article.status) }}</span>
                        <span>{{ formatDate(article.updated_at) }}</span>
                        <span>浏览量：{{ article.view_count || 0 }}</span>
                      </div>
                    </div>
                    <div class="flex items-center space-x-2">
                      <router-link
                        :to="`/article/${article.id}/edit`"
                        class="text-indigo-600 hover:text-indigo-500 text-sm font-medium"
                      >
                        编辑
                      </router-link>
                      <button
                        @click="deleteContent('article', article.id)"
                        class="text-red-600 hover:text-red-500 text-sm font-medium"
                      >
                        删除
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 路线图列表 -->
            <div v-if="activeTab === 'roadmaps'">
              <div v-if="loading" class="text-center py-8">
                <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
                <p class="mt-2 text-gray-600">加载中...</p>
              </div>
              <div v-else-if="contentStore.roadmaps.length === 0" class="text-center py-8">
                <p class="text-gray-600">还没有路线图，<router-link to="/roadmap/new" class="text-indigo-600 hover:text-indigo-500">创建第一个路线图</router-link></p>
              </div>
              <div v-else class="space-y-4">
                <div
                  v-for="roadmap in contentStore.roadmaps"
                  :key="roadmap.id"
                  class="border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow"
                >
                  <div class="flex items-center justify-between">
                    <div class="flex-1">
                      <h3 class="text-lg font-medium text-gray-900">{{ roadmap.title }}</h3>
                      <p class="mt-1 text-sm text-gray-600">{{ roadmap.description || '暂无描述' }}</p>
                      <div class="mt-2 flex items-center space-x-4 text-sm text-gray-500">
                        <span :class="getStatusClass(roadmap.status)">{{ getStatusText(roadmap.status) }}</span>
                        <span>{{ formatDate(roadmap.updated_at) }}</span>
                        <span>浏览量：{{ roadmap.view_count || 0 }}</span>
                      </div>
                    </div>
                    <div class="flex items-center space-x-2">
                      <router-link
                        :to="`/roadmap/${roadmap.id}/edit`"
                        class="text-indigo-600 hover:text-indigo-500 text-sm font-medium"
                      >
                        编辑
                      </router-link>
                      <button
                        @click="deleteContent('roadmap', roadmap.id)"
                        class="text-red-600 hover:text-red-500 text-sm font-medium"
                      >
                        删除
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 思维导图列表 -->
            <div v-if="activeTab === 'mindmaps'">
              <div v-if="loading" class="text-center py-8">
                <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
                <p class="mt-2 text-gray-600">加载中...</p>
              </div>
              <div v-else-if="contentStore.mindmaps.length === 0" class="text-center py-8">
                <p class="text-gray-600">还没有思维导图，<router-link to="/mindmap/new" class="text-indigo-600 hover:text-indigo-500">创建第一个思维导图</router-link></p>
              </div>
              <div v-else class="space-y-4">
                <div
                  v-for="mindmap in contentStore.mindmaps"
                  :key="mindmap.id"
                  class="border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow"
                >
                  <div class="flex items-center justify-between">
                    <div class="flex-1">
                      <h3 class="text-lg font-medium text-gray-900">{{ mindmap.title }}</h3>
                      <p class="mt-1 text-sm text-gray-600">{{ mindmap.description || '暂无描述' }}</p>
                      <div class="mt-2 flex items-center space-x-4 text-sm text-gray-500">
                        <span :class="getStatusClass(mindmap.status)">{{ getStatusText(mindmap.status) }}</span>
                        <span>{{ formatDate(mindmap.updated_at) }}</span>
                        <span>浏览量：{{ mindmap.view_count || 0 }}</span>
                      </div>
                    </div>
                    <div class="flex items-center space-x-2">
                      <router-link
                        :to="`/mindmap/${mindmap.id}/edit`"
                        class="text-indigo-600 hover:text-indigo-500 text-sm font-medium"
                      >
                        编辑
                      </router-link>
                      <button
                        @click="deleteContent('mindmap', mindmap.id)"
                        class="text-red-600 hover:text-red-500 text-sm font-medium"
                      >
                        删除
                      </button>
                    </div>
                  </div>
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
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'
import { useContentStore } from '../stores/content.js'

const router = useRouter()
const authStore = useAuthStore()
const contentStore = useContentStore()

const activeTab = ref('articles')
const loading = ref(false)

const tabs = [
  { key: 'articles', name: '文章' },
  { key: 'roadmaps', name: '路线图' },
  { key: 'mindmaps', name: '思维导图' }
]

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}

const getTabCount = (tabKey) => {
  switch (tabKey) {
    case 'articles':
      return contentStore.articles.length
    case 'roadmaps':
      return contentStore.roadmaps.length
    case 'mindmaps':
      return contentStore.mindmaps.length
    default:
      return 0
  }
}

const getStatusText = (status) => {
  const statusMap = {
    draft: '草稿',
    published: '已发布',
    archived: '已归档'
  }
  return statusMap[status] || status
}

const getStatusClass = (status) => {
  const statusClasses = {
    draft: 'text-yellow-600 bg-yellow-100 px-2 py-1 rounded-full text-xs',
    published: 'text-green-600 bg-green-100 px-2 py-1 rounded-full text-xs',
    archived: 'text-gray-600 bg-gray-100 px-2 py-1 rounded-full text-xs'
  }
  return statusClasses[status] || 'text-gray-600 bg-gray-100 px-2 py-1 rounded-full text-xs'
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

const deleteContent = async (type, id) => {
  if (!confirm('确定要删除这个内容吗？此操作不可撤销。')) {
    return
  }

  try {
    let result
    switch (type) {
      case 'article':
        result = await contentStore.deleteArticle(id)
        break
      case 'roadmap':
        // TODO: 实现路线图删除
        break
      case 'mindmap':
        // TODO: 实现思维导图删除
        break
    }

    if (result && result.success) {
      // 删除成功，内容已从store中移除
    } else {
      alert('删除失败：' + (result?.error || '未知错误'))
    }
  } catch (error) {
    alert('删除失败：' + error.message)
  }
}

const loadContent = async () => {
  loading.value = true
  try {
    const userId = authStore.currentUser?.id
    if (userId) {
      await Promise.all([
        contentStore.loadArticles({ user_id: userId, status: '' }), // 加载所有状态的文章
        contentStore.loadRoadmaps({ user_id: userId, status: '' }),
        contentStore.loadMindmaps({ user_id: userId, status: '' }),
        contentStore.loadTags(userId)
      ])
    }
  } catch (error) {
    console.error('加载内容失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadContent()
})
</script>

