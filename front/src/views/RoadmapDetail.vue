<template>
  <div class="min-h-screen bg-gray-50">
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

<SimplePaywallModal 
  v-if="showPaywall && !hasPaid" 
  @pay="handlePayment" 
  @close="handleClosePaywall" 
/>

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

      <article v-else-if="roadmap" class="bg-white shadow rounded-lg overflow-hidden">
        <div class="px-6 py-8 border-b border-gray-200">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center text-sm text-gray-500">
              <span>{{ formatDate(roadmap.created_at) }}</span>
              <span class="mx-2">•</span>
              <span v-if="roadmap.author">作者：{{ roadmap.author.display_name || roadmap.author.username }}</span>
            </div>
            <div v-if="canEdit" class="flex space-x-2">
              <router-link 
                :to="`/roadmap/${roadmap.id}/edit`"
                class="px-3 py-1 text-sm bg-indigo-600 text-white rounded hover:bg-indigo-700"
              >
                编辑
              </router-link>
            </div>
          </div>
          <h1 class="text-3xl font-bold text-gray-900 mb-4">{{ roadmap.title }}</h1>
          <div v-if="roadmap.description" class="text-lg text-gray-600 mb-4">
            {{ roadmap.description }}
          </div>
          <div v-if="roadmap.tags && roadmap.tags.length > 0" class="flex flex-wrap gap-2">
            <span 
              v-for="tag in roadmap.tags" 
              :key="tag.id"
              class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800"
            >
              {{ tag.name }}
            </span>
          </div>
        </div>

        <div class="px-6 py-8">
  <div v-if="roadmap.content && (hasPaid || !isOtherUserContent)" style="height: 70vh;">
    <RoadmapViewer v-model="roadmap.content" />
  </div>
  <div v-else-if="!hasPaid && isOtherUserContent" class="text-center py-12">
    <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-gray-100">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
      </svg>
    </div>
    <h3 class="mt-2 text-lg font-medium text-gray-900">内容已锁定</h3>
    <p class="mt-1 text-sm text-gray-500">支付1元后即可查看完整内容</p>
    <button
      @click="showPaywall = true"
      class="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
    >
      立即支付
    </button>
  </div>
  <div v-else class="text-gray-500 italic">
    暂无内容
  </div>
</div>
      </article>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'
import { useContentStore } from '../stores/content.js'
import RoadmapViewer from '../components/Roadmap/RoadmapViewer.vue' 
import SimplePaywallModal from '../components/SimplePaywallModal.vue'

const showPaywall = ref(false)
const hasPaid = ref(false)

const route = useRoute()
const authStore = useAuthStore()
const contentStore = useContentStore()

const loading = ref(true)
const error = ref('')
const roadmap = ref(null)

const canEdit = computed(() => {
  return authStore.isAuthenticated && 
         roadmap.value && 
         roadmap.value.user_id === authStore.user?.id
})

const isOtherUserContent = computed(() => {
  return authStore.isAuthenticated && 
         roadmap.value && 
         roadmap.value.user_id !== authStore.user?.id
})

const handlePayment = () => {
  hasPaid.value = true
  showPaywall.value = false
}

const handleClosePaywall = () => {
  showPaywall.value = false
}

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

const loadRoadmap = async () => {
  const roadmapId = parseInt(route.params.id)
  if (!roadmapId) {
    error.value = '无效的路线图ID'
    loading.value = false
    return
  }

  try {
    const result = await contentStore.loadRoadmap(roadmapId)
    if (result.success) {
  roadmap.value = result.data
  if (isOtherUserContent.value) {
    showPaywall.value = true
  }
} else {
      error.value = result.error || '路线图不存在'
    }
  } catch (err) {
    error.value = '加载路线图失败'
    console.error('加载路线图失败:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadRoadmap()
})
</script>

<style scoped>

</style>