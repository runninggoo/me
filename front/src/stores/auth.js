// src/stores/auth.js
import { defineStore } from 'pinia'
import { authAPI, adminAPI } from '../services/api.js'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('auth_token'),
    isAuthenticated: false,
    isAdmin: false,
    loading: false
  }),

  getters: {
    isLoggedIn: (state) => !!state.token && !!state.user,
    currentUser: (state) => state.user
  },

  actions: {
    // 初始化认证状态
    async initAuth() {
      const token = localStorage.getItem('auth_token')
      const userInfo = localStorage.getItem('user_info')
      
      if (token && userInfo) {
        this.token = token
        this.user = JSON.parse(userInfo)
        this.isAuthenticated = true
        
        // 验证token是否有效
        try {
          const response = await authAPI.getCurrentUser()
          if (response.success) {
            this.user = response.data
            localStorage.setItem('user_info', JSON.stringify(response.data))
          }
        } catch (error) {
          // Token无效，清除认证状态
          this.logout()
        }
      }
    },

    // 用户登录
    async login(credentials) {
      this.loading = true
      try {
        const response = await authAPI.login(credentials)
        if (response.success) {
          this.token = response.data.token
          this.user = response.data.user
          this.isAuthenticated = true
          
          // 保存到本地存储
          localStorage.setItem('auth_token', response.data.token)
          localStorage.setItem('user_info', JSON.stringify(response.data.user))
          
          return { success: true, message: response.message }
        }
        return { success: false, message: response.error }
      } catch (error) {
        return { success: false, message: error.error || '登录失败' }
      } finally {
        this.loading = false
      }
    },

    // 用户注册
    async register(userData) {
      this.loading = true
      try {
        const response = await authAPI.register(userData)
        if (response.success) {
          this.token = response.data.token
          this.user = response.data.user
          this.isAuthenticated = true
          
          // 保存到本地存储
          localStorage.setItem('auth_token', response.data.token)
          localStorage.setItem('user_info', JSON.stringify(response.data.user))
          
          return { success: true, message: response.message }
        }
        return { success: false, message: response.error }
      } catch (error) {
        return { success: false, message: error.error || '注册失败' }
      } finally {
        this.loading = false
      }
    },

    // 用户登出
    logout() {
      this.user = null
      this.token = null
      this.isAuthenticated = false
      
      // 清除本地存储
      localStorage.removeItem('auth_token')
      localStorage.removeItem('user_info')
    },

    // 更新用户信息
    async updateProfile(userData) {
      this.loading = true
      try {
        const response = await authAPI.updateProfile(userData)
        if (response.success) {
          this.user = response.data
          localStorage.setItem('user_info', JSON.stringify(response.data))
          return { success: true, message: response.message }
        }
        return { success: false, message: response.error }
      } catch (error) {
        return { success: false, message: error.error || '更新失败' }
      } finally {
        this.loading = false
      }
    },

    // 管理员登录
    async adminLogin(credentials) {
      this.loading = true
      try {
        const response = await adminAPI.login(credentials)
        if (response.success) {
          this.token = response.data.access_token
          this.user = response.data.user
          this.isAuthenticated = true
          
          // 保存到本地存储
          localStorage.setItem('auth_token', response.data.access_token)
          localStorage.setItem('user_info', JSON.stringify(response.data.user))
          
          return { success: true, message: response.message }
        }
        return { success: false, message: response.error }
      } catch (error) {
        return { success: false, message: error.error || '管理员登录失败' }
      } finally {
        this.loading = false
      }
    },

    // 管理员注册
    async adminRegister(userData) {
      this.loading = true
      try {
        const response = await adminAPI.register(userData)
        if (response.success) {
          this.token = response.data.access_token
          this.user = response.data.user
          this.isAuthenticated = true
          
          // 保存到本地存储
          localStorage.setItem('auth_token', response.data.access_token)
          localStorage.setItem('user_info', JSON.stringify(response.data.user))
          
          return { success: true, message: response.message }
        }
        return { success: false, message: response.error }
      } catch (error) {
        return { success: false, message: error.error || '管理员注册失败' }
      } finally {
        this.loading = false
      }
    }
  }
})

