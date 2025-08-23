<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 顶部导航 -->
    <nav class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-semibold text-gray-900">管理员控制台</h1>
          </div>
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-600">
              欢迎，{{ authStore.currentUser?.username }}
            </span>
            <button
              @click="handleLogout"
              class="text-sm text-gray-600 hover:text-gray-900"
            >
              退出登录
            </button>
          </div>
        </div>
      </div>
    </nav>

    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- 统计卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-indigo-500 rounded-md flex items-center justify-center">
                  <span class="text-white text-sm font-medium">标</span>
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">
                    标签文章总数
                  </dt>
                  <dd class="text-lg font-medium text-gray-900">
                    {{ tagArticles.length }}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-green-500 rounded-md flex items-center justify-center">
                  <span class="text-white text-sm font-medium">用</span>
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">
                    普通用户数
                  </dt>
                  <dd class="text-lg font-medium text-gray-900">
                    {{ userCount }}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-yellow-500 rounded-md flex items-center justify-center">
                  <span class="text-white text-sm font-medium">文</span>
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">
                    普通文章数
                  </dt>
                  <dd class="text-lg font-medium text-gray-900">
                    {{ normalArticles.length }}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 标签文章管理 -->
      <div class="bg-white shadow rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <div class="flex justify-between items-center mb-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900">
              标签文章管理
            </h3>
            <button
              @click="showCreateModal = true"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              创建标签文章
            </button>
          </div>

          <!-- 标签文章列表 -->
          <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
            <table class="min-w-full divide-y divide-gray-300">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    标签名称
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    状态
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    创建时间
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    操作
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="article in tagArticles" :key="article.id">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {{ article.title }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="getStatusClass(article.status)" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full">
                      {{ getStatusText(article.status) }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ formatDate(article.created_at) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                    <button
                      @click="editTagArticle(article)"
                      class="text-indigo-600 hover:text-indigo-900"
                    >
                      编辑
                    </button>
                    <button
                      @click="deleteTagArticle(article.id)"
                      class="text-red-600 hover:text-red-900"
                    >
                      删除
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div v-if="tagArticles.length === 0" class="text-center py-12">
            <p class="text-gray-500">暂无标签文章</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 创建/编辑标签文章模态框 -->
    <div v-if="showCreateModal || showEditModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">
            {{ showEditModal ? '编辑标签文章' : '创建标签文章' }}
          </h3>
          
          <form @submit.prevent="handleSubmit" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                标签名称（即文章标题）
              </label>
              <input
                v-model="articleForm.title"
                type="text"
                required
                class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="请输入标签名称"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                文章内容
              </label>
              <textarea
                v-model="articleForm.content"
                rows="8"
                required
                class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="请输入文章内容"
              ></textarea>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                状态
              </label>
              <select
                v-model="articleForm.status"
                class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              >
                <option value="draft">草稿</option>
                <option value="published">已发布</option>
                <option value="archived">已归档</option>
              </select>
            </div>

            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="closeModal"
                class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                取消
              </button>
              <button
                type="submit"
                :disabled="loading"
                class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
              >
                {{ loading ? '保存中...' : '保存' }}
              </button>
            </div>
          </form>
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

// 数据
const tagArticles = ref([])
const normalArticles = ref([])
const userCount = ref(0)

// 模态框状态
const showCreateModal = ref(false)
const showEditModal = ref(false)
const loading = ref(false)

// 表单数据
const articleForm = ref({
  id: null,
  title: '',
  content: '',
  status: 'draft'
})

// 方法
const loadData = async () => {
  try {
    // 加载标签文章
    const tagResult = await contentStore.loadArticles({ is_tag_article: true })
    if (tagResult.success) {
      tagArticles.value = tagResult.data
    }

    // 加载普通文章
    const normalResult = await contentStore.loadArticles({ is_tag_article: false })
    if (normalResult.success) {
      normalArticles.value = normalResult.data
    }

    // 这里可以添加加载用户数量的逻辑
    userCount.value = 10 // 临时数据
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

const handleSubmit = async () => {
  loading.value = true
  
  try {
    const articleData = {
      ...articleForm.value,
      is_tag_article: true
    }

    let result
    if (showEditModal.value) {
      result = await contentStore.updateArticle(articleData)
    } else {
      result = await contentStore.createTagArticle(articleData)
    }

    if (result.success) {
      closeModal()
      await loadData()
    } else {
      alert('操作失败：' + result.error)
    }
  } catch (error) {
    alert('操作失败，请重试')
  } finally {
    loading.value = false
  }
}

const editTagArticle = (article) => {
  articleForm.value = {
    id: article.id,
    title: article.title,
    content: article.content || '',
    status: article.status
  }
  showEditModal.value = true
}

const deleteTagArticle = async (id) => {
  if (!confirm('确定要删除这个标签文章吗？')) {
    return
  }

  try {
    const result = await contentStore.deleteArticle(id)
    if (result.success) {
      await loadData()
    } else {
      alert('删除失败：' + result.error)
    }
  } catch (error) {
    alert('删除失败，请重试')
  }
}

const closeModal = () => {
  showCreateModal.value = false
  showEditModal.value = false
  articleForm.value = {
    id: null,
    title: '',
    content: '',
    status: 'draft'
  }
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/admin/login')
}

const getStatusClass = (status) => {
  switch (status) {
    case 'published':
      return 'bg-green-100 text-green-800'
    case 'draft':
      return 'bg-yellow-100 text-yellow-800'
    case 'archived':
      return 'bg-gray-100 text-gray-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

const getStatusText = (status) => {
  switch (status) {
    case 'published':
      return '已发布'
    case 'draft':
      return '草稿'
    case 'archived':
      return '已归档'
    default:
      return '未知'
  }
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('zh-CN')
}

onMounted(() => {
  loadData()
})
</script>

