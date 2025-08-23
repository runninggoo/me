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
          </div>
        </div>
      </div>
    </nav>

    <div class="max-w-3xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <h1 class="text-3xl font-bold text-gray-900">个人资料</h1>
        <p class="mt-2 text-gray-600">管理您的账户信息</p>
      </div>

      <div class="bg-white shadow rounded-lg">
        <form @submit.prevent="handleUpdateProfile" class="space-y-6 p-6">
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700">用户名</label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              disabled
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-gray-50 text-gray-500 cursor-not-allowed"
            />
            <p class="mt-1 text-sm text-gray-500">用户名不可修改</p>
          </div>

          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">邮箱</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          <div>
            <label for="display_name" class="block text-sm font-medium text-gray-700">显示名称</label>
            <input
              id="display_name"
              v-model="form.display_name"
              type="text"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          <div>
            <label for="bio" class="block text-sm font-medium text-gray-700">个人简介</label>
            <textarea
              id="bio"
              v-model="form.bio"
              rows="4"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="介绍一下自己..."
            ></textarea>
          </div>

          <div>
            <label for="avatar_url" class="block text-sm font-medium text-gray-700">头像URL</label>
            <input
              id="avatar_url"
              v-model="form.avatar_url"
              type="url"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="https://example.com/avatar.jpg"
            />
          </div>

          <div v-if="error" class="text-red-600 text-sm">
            {{ error }}
          </div>

          <div v-if="success" class="text-green-600 text-sm">
            {{ success }}
          </div>

          <div class="flex justify-end">
            <button
              type="submit"
              :disabled="loading"
              class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="loading">保存中...</span>
              <span v-else>保存更改</span>
            </button>
          </div>
        </form>
      </div>

      <!-- 账户统计 -->
      <div class="mt-8 bg-white shadow rounded-lg p-6">
        <h2 class="text-lg font-medium text-gray-900 mb-4">账户统计</h2>
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <div class="text-center">
            <div class="text-2xl font-bold text-indigo-600">{{ stats.articles }}</div>
            <div class="text-sm text-gray-600">文章</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-green-600">{{ stats.roadmaps }}</div>
            <div class="text-sm text-gray-600">路线图</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-purple-600">{{ stats.mindmaps }}</div>
            <div class="text-sm text-gray-600">思维导图</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'
import { useContentStore } from '../stores/content.js'

const router = useRouter()
const authStore = useAuthStore()
const contentStore = useContentStore()

const form = ref({
  username: '',
  email: '',
  display_name: '',
  bio: '',
  avatar_url: ''
})

const stats = ref({
  articles: 0,
  roadmaps: 0,
  mindmaps: 0
})

const error = ref('')
const success = ref('')
const loading = ref(false)

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}

const handleUpdateProfile = async () => {
  loading.value = true
  error.value = ''
  success.value = ''

  try {
    const result = await authStore.updateProfile({
      email: form.value.email,
      display_name: form.value.display_name,
      bio: form.value.bio,
      avatar_url: form.value.avatar_url
    })

    if (result.success) {
      success.value = '个人资料更新成功'
      setTimeout(() => {
        success.value = ''
      }, 3000)
    } else {
      error.value = result.message
    }
  } catch (err) {
    error.value = '更新失败，请稍后重试'
  } finally {
    loading.value = false
  }
}

const loadStats = async () => {
  try {
    const userId = authStore.currentUser?.id
    if (userId) {
      await Promise.all([
        contentStore.loadArticles({ user_id: userId, status: '' }),
        contentStore.loadRoadmaps({ user_id: userId, status: '' }),
        contentStore.loadMindmaps({ user_id: userId, status: '' })
      ])

      stats.value = {
        articles: contentStore.articles.length,
        roadmaps: contentStore.roadmaps.length,
        mindmaps: contentStore.mindmaps.length
      }
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

onMounted(() => {
  const user = authStore.currentUser
  if (user) {
    form.value = {
      username: user.username,
      email: user.email || '',
      display_name: user.display_name || '',
      bio: user.bio || '',
      avatar_url: user.avatar_url || ''
    }
  }
  
  loadStats()
})
</script>

