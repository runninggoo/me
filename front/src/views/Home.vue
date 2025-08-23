<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 导航栏 -->
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-bold text-gray-900">个人博客系统</h1>
          </div>
          <div class="flex items-center space-x-4">
            <template v-if="authStore.isLoggedIn">
              <router-link
                to="/dashboard"
                class="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
              >
                仪表板
              </router-link>
              <button
                @click="handleLogout"
                class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                退出登录
              </button>
            </template>
            <template v-else>
              <router-link
                to="/login"
                class="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
              >
                登录
              </router-link>
              <router-link
                to="/register"
                class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                注册
              </router-link>
            </template>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主要内容 -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- 欢迎区域 -->
      <div class="px-4 py-6 sm:px-0">
        <div class="text-center">
          <h2 class="text-3xl font-extrabold text-gray-900 sm:text-4xl">
            欢迎来到个人博客系统
          </h2>
          <p class="mt-4 text-lg text-gray-600">
            创建和分享您的文章、路线图和思维导图
          </p>
          <div class="mt-8">
            <router-link
              v-if="!authStore.isLoggedIn"
              to="/register"
              class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
            >
              开始使用
            </router-link>
            <router-link
              v-else
              to="/dashboard"
              class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
            >
              进入仪表板
            </router-link>
          </div>
        </div>
      </div>

      <!-- 功能介绍 -->
      <div class="mt-16">
        <div class="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <div class="ml-4">
                  <h3 class="text-lg font-medium text-gray-900">富文本编辑</h3>
                </div>
              </div>
              <div class="mt-4">
                <p class="text-sm text-gray-600">
                  使用强大的TipTap编辑器创建和编辑文章，支持Markdown、数学公式、代码高亮等功能。
                </p>
              </div>
            </div>
          </div>

          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
                  </svg>
                </div>
                <div class="ml-4">
                  <h3 class="text-lg font-medium text-gray-900">路线图设计</h3>
                </div>
              </div>
              <div class="mt-4">
                <p class="text-sm text-gray-600">
                  使用Vue Flow创建交互式路线图，规划学习路径和项目进度。
                </p>
              </div>
            </div>
          </div>

          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <div class="ml-4">
                  <h3 class="text-lg font-medium text-gray-900">思维导图</h3>
                </div>
              </div>
              <div class="mt-4">
                <p class="text-sm text-gray-600">
                  创建思维导图来整理思路，可视化知识结构和概念关系。
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 最新内容 -->
      <div class="mt-16" v-if="recentContent.length > 0">
        <h3 class="text-2xl font-bold text-gray-900 mb-8">最新内容</h3>
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <router-link
            v-for="item in recentContent"
            :key="`${item.type}-${item.id}`"
            :to="getItemLink(item)"
            class="bg-white overflow-hidden shadow rounded-lg hover:shadow-md transition-shadow block"
          >
            <div class="p-6">
              <div class="flex items-center justify-between">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                      :class="getTypeClass(item.type)">
                  {{ getTypeName(item.type) }}
                </span>
                <span class="text-sm text-gray-500">
                  {{ formatDate(item.created_at) }}
                </span>
              </div>
              <h4 class="mt-4 text-lg font-medium text-gray-900 hover:text-indigo-600">{{ item.title }}</h4>
              <p class="mt-2 text-sm text-gray-600 line-clamp-3">
                {{ item.excerpt || item.description || '暂无描述' }}
              </p>
              <div class="mt-4">
                <span class="text-sm text-gray-500">
                  作者：{{ item.author?.display_name || item.author?.username }}
                </span>
              </div>
            </div>
          </router-link>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'
import { articleAPI, roadmapAPI, mindmapAPI } from '../services/api.js'

const router = useRouter()
const authStore = useAuthStore()

const recentContent = ref([])
const loading = ref(false)

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}

const loadRecentContent = async () => {
  loading.value = true
  try {
    // 并行加载最新的文章、路线图和思维导图
    const [articlesRes, roadmapsRes, mindmapsRes] = await Promise.all([
      articleAPI.getArticles({ status: 'published', limit: 3 }),
      roadmapAPI.getRoadmaps({ status: 'published', limit: 3 }),
      mindmapAPI.getMindmaps({ status: 'published', limit: 3 })
    ])

    const allContent = []
    
    if (articlesRes.success) {
      allContent.push(...articlesRes.data.articles.map(item => ({ ...item, type: 'article' })))
    }
    
    if (roadmapsRes.success) {
      allContent.push(...roadmapsRes.data.roadmaps.map(item => ({ ...item, type: 'roadmap' })))
    }
    
    if (mindmapsRes.success) {
      allContent.push(...mindmapsRes.data.mindmaps.map(item => ({ ...item, type: 'mindmap' })))
    }

    // 按创建时间排序，取最新的9个
    recentContent.value = allContent
      .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
      .slice(0, 9)
      
  } catch (error) {
    console.error('加载最新内容失败:', error)
  } finally {
    loading.value = false
  }
}

const getItemLink = (item) => {
  switch (item.type) {
    case 'article':
      return `/article/${item.id}`
    case 'roadmap':
      return `/roadmap/${item.id}`
    case 'mindmap':
      return `/mindmap/${item.id}`
    default:
      return '#'
  }
}

const getTypeName = (type) => {
  const typeNames = {
    article: '文章',
    roadmap: '路线图',
    mindmap: '思维导图'
  }
  return typeNames[type] || type
}

const getTypeClass = (type) => {
  const typeClasses = {
    article: 'bg-blue-100 text-blue-800',
    roadmap: 'bg-green-100 text-green-800',
    mindmap: 'bg-purple-100 text-purple-800'
  }
  return typeClasses[type] || 'bg-gray-100 text-gray-800'
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

onMounted(() => {
  loadRecentContent()
})
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

