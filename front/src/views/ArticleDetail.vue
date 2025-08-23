<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 导航栏 -->
    <nav class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <router-link to="/" class="text-xl font-bold text-gray-900">
              个人博客系统
            </router-link>
          </div>
          <div class="flex items-center space-x-4">
            <router-link 
              to="/" 
              class="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
            >
              首页
            </router-link>
            <router-link 
              v-if="authStore.isAuthenticated" 
              to="/dashboard" 
              class="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
            >
              仪表板
            </router-link>
            <router-link 
              v-if="!authStore.isAuthenticated" 
              to="/login" 
              class="bg-indigo-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-indigo-700"
            >
              登录
            </router-link>
            <button 
              v-if="authStore.isAuthenticated" 
              @click="authStore.logout" 
              class="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
            >
              退出登录
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主内容 -->
    <main class="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
        <p class="mt-2 text-gray-600">加载中...</p>
      </div>

      <div v-else-if="error" class="text-center py-12">
        <p class="text-red-600">{{ error }}</p>
        <router-link 
          to="/" 
          class="mt-4 inline-block bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700"
        >
          返回首页
        </router-link>
      </div>

      <article v-else-if="article" class="bg-white shadow rounded-lg overflow-hidden">
        <!-- 文章头部 -->
        <div class="px-6 py-8 border-b border-gray-200">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center text-sm text-gray-500">
              <span>{{ formatDate(article.created_at) }}</span>
              <span class="mx-2">•</span>
              <span>{{ article.view_count }} 次浏览</span>
              <span v-if="article.author" class="mx-2">•</span>
              <span v-if="article.author">作者：{{ article.author.display_name || article.author.username }}</span>
            </div>
            <div v-if="canEdit" class="flex space-x-2">
              <router-link 
                :to="`/article/${article.id}/edit`"
                class="px-3 py-1 text-sm bg-indigo-600 text-white rounded hover:bg-indigo-700"
              >
                编辑
              </router-link>
            </div>
          </div>
          
          <h1 class="text-3xl font-bold text-gray-900 mb-4">{{ article.title }}</h1>
          
          <div v-if="article.excerpt" class="text-lg text-gray-600 mb-4">
            {{ article.excerpt }}
          </div>

          <!-- 标签 -->
          <div v-if="article.tags && article.tags.length > 0" class="flex flex-wrap gap-2">
            <span 
              v-for="tag in article.tags" 
              :key="tag.id"
              class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800"
            >
              {{ tag.name }}
            </span>
          </div>
        </div>

        <!-- 文章内容 -->
        <div class="px-6 py-8">
          <div v-if="article.content" class="prose prose-lg max-w-none">
            <TipTapViewer v-model="article.content" />
          </div>
          <div v-else class="text-gray-500 italic">
            暂无内容
          </div>
        </div>

        <!-- 关联内容 -->
        <div v-if="hasRelatedContent" class="px-6 py-6 bg-gray-50 border-t border-gray-200">
          <h3 class="text-lg font-medium text-gray-900 mb-4">相关内容</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-if="article.roadmap_id" class="bg-white p-4 rounded-lg border">
              <h4 class="font-medium text-gray-900 mb-2">关联路线图</h4>
              <router-link 
                :to="`/roadmap/${article.roadmap_id}`"
                class="text-indigo-600 hover:text-indigo-800"
              >
                查看路线图
              </router-link>
            </div>
            <div v-if="article.mindmap_id" class="bg-white p-4 rounded-lg border">
              <h4 class="font-medium text-gray-900 mb-2">关联思维导图</h4>
              <router-link 
                :to="`/mindmap/${article.mindmap_id}`"
                class="text-indigo-600 hover:text-indigo-800"
              >
                查看思维导图
              </router-link>
            </div>
          </div>
        </div>
      </article>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'
import { useContentStore } from '../stores/content.js'
import TipTapViewer from '../components/Article/TipTapViewer.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const contentStore = useContentStore()

const loading = ref(true)
const error = ref('')
const article = ref(null)

const canEdit = computed(() => {
  return authStore.isAuthenticated && 
         article.value && 
         article.value.user_id === authStore.user?.id
})

const hasRelatedContent = computed(() => {
  return article.value && (article.value.roadmap_id || article.value.mindmap_id)
})

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const loadArticle = async () => {
  const articleId = parseInt(route.params.id)
  if (!articleId) {
    error.value = '无效的文章ID'
    loading.value = false
    return
  }

  try {
    const result = await contentStore.loadArticle(articleId)
    if (result.success) {
      article.value = result.data
    } else {
      error.value = result.error || '文章不存在'
    }
  } catch (err) {
    error.value = '加载文章失败'
    console.error('加载文章失败:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadArticle()
})
</script>

<style scoped>
.prose {
  color: #374151;
  line-height: 1.75;
}

.prose h1, .prose h2, .prose h3, .prose h4, .prose h5, .prose h6 {
  color: #111827;
  font-weight: 600;
  line-height: 1.25;
}

.prose h1 { font-size: 2.25rem; margin-top: 0; margin-bottom: 0.8888889em; }
.prose h2 { font-size: 1.875rem; margin-top: 2em; margin-bottom: 1em; }
.prose h3 { font-size: 1.5rem; margin-top: 1.6em; margin-bottom: 0.6em; }

.prose p {
  margin-top: 1.25em;
  margin-bottom: 1.25em;
}

.prose blockquote {
  font-weight: 500;
  font-style: italic;
  color: #374151;
  border-left-width: 0.25rem;
  border-left-color: #d1d5db;
  quotes: "\201C""\201D""\2018""\2019";
  margin-top: 1.6em;
  margin-bottom: 1.6em;
  padding-left: 1em;
}

.prose ul, .prose ol {
  margin-top: 1.25em;
  margin-bottom: 1.25em;
  padding-left: 1.625em;
}

.prose li {
  margin-top: 0.5em;
  margin-bottom: 0.5em;
}

.prose pre {
  color: #374151;
  background-color: #f3f4f6;
  overflow-x: auto;
  font-weight: 400;
  font-size: 0.875em;
  line-height: 1.7142857;
  margin-top: 1.7142857em;
  margin-bottom: 1.7142857em;
  border-radius: 0.375rem;
  padding-top: 0.8571429em;
  padding-right: 1.1428571em;
  padding-bottom: 0.8571429em;
  padding-left: 1.1428571em;
}

.prose code {
  color: #111827;
  font-weight: 600;
  font-size: 0.875em;
}

.prose a {
  color: #3b82f6;
  text-decoration: underline;
  font-weight: 500;
}

.prose a:hover {
  color: #1d4ed8;
}
</style>

