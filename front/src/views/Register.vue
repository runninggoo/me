<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          创建新账户
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          或者
          <router-link to="/login" class="font-medium text-indigo-600 hover:text-indigo-500">
            登录现有账户
          </router-link>
        </p>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleRegister">
        <div class="space-y-4">
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700">用户名</label>
            <input
              id="username"
              v-model="form.username"
              name="username"
              type="text"
              required
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="请输入用户名"
            />
          </div>
          
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">邮箱</label>
            <input
              id="email"
              v-model="form.email"
              name="email"
              type="email"
              required
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="请输入邮箱地址"
            />
          </div>
          
          <div>
            <label for="display_name" class="block text-sm font-medium text-gray-700">显示名称（可选）</label>
            <input
              id="display_name"
              v-model="form.display_name"
              name="display_name"
              type="text"
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="请输入显示名称"
            />
          </div>
          
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">密码</label>
            <input
              id="password"
              v-model="form.password"
              name="password"
              type="password"
              required
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="请输入密码（至少8位）"
            />
          </div>
          
          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700">确认密码</label>
            <input
              id="confirmPassword"
              v-model="form.confirmPassword"
              name="confirmPassword"
              type="password"
              required
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="请再次输入密码"
            />
          </div>
        </div>

        <div v-if="error" class="text-red-600 text-sm text-center">
          {{ error }}
        </div>

        <div>
          <button
            type="submit"
            :disabled="loading"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading">注册中...</span>
            <span v-else>注册</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  username: '',
  email: '',
  display_name: '',
  password: '',
  confirmPassword: ''
})

const error = ref('')
const loading = ref(false)

const validateForm = () => {
  if (!form.value.username || !form.value.email || !form.value.password) {
    return '请填写所有必填字段'
  }
  
  if (form.value.password.length < 8) {
    return '密码至少需要8位字符'
  }
  
  if (form.value.password !== form.value.confirmPassword) {
    return '两次输入的密码不一致'
  }
  
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(form.value.email)) {
    return '请输入有效的邮箱地址'
  }
  
  return null
}

const handleRegister = async () => {
  const validationError = validateForm()
  if (validationError) {
    error.value = validationError
    return
  }

  loading.value = true
  error.value = ''

  try {
    const registerData = {
      username: form.value.username,
      email: form.value.email,
      password: form.value.password
    }
    
    if (form.value.display_name) {
      registerData.display_name = form.value.display_name
    }

    const result = await authStore.register(registerData)
    if (result.success) {
      router.push('/dashboard')
    } else {
      error.value = result.message
    }
  } catch (err) {
    error.value = '注册失败，请稍后重试'
  } finally {
    loading.value = false
  }
}
</script>

