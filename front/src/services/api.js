// src/services/api.js
import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:5001/api',  // 修改为完整的后端API地址
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器 - 添加JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 处理错误
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    if (error.response?.status === 401) {
      // Token过期或无效，清除本地存储并跳转到登录页
      localStorage.removeItem('auth_token')
      localStorage.removeItem('user_info')
      // 这里可以添加路由跳转逻辑
    }
    return Promise.reject(error.response?.data || error.message)
  }
)

// 认证相关API
export const authAPI = {
  // 用户注册
  register(userData) {
    return api.post('/auth/register', userData)
  },
  
  // 用户登录
  login(credentials) {
    return api.post('/auth/login', credentials)
  },
  
  // 获取当前用户信息
  getCurrentUser() {
    return api.get('/auth/me')
  },
  
  // 更新用户信息
  updateProfile(userData) {
    return api.put('/auth/profile', userData)
  }
}

// 文章相关API
export const articleAPI = {
  // 获取文章列表
  getArticles(params = {}) {
    return api.get('/articles', { params })
  },
  
  // 获取文章详情
  getArticle(id) {
    return api.get(`/articles/${id}`)
  },
  
  // 创建文章
  createArticle(articleData) {
    return api.post('/articles', articleData)
  },
  
  // 更新文章
  updateArticle(id, articleData) {
    return api.put(`/articles/${id}`, articleData)
  },
  
  // 删除文章
  deleteArticle(id) {
    return api.delete(`/articles/${id}`)
  },
  
  // 发布文章
  publishArticle(id) {
    return api.post(`/articles/${id}/publish`)
  }
}

// 路线图相关API
export const roadmapAPI = {
  // 获取路线图列表
  getRoadmaps(params = {}) {
    return api.get('/roadmaps', { params })
  },
  
  // 获取路线图详情
  getRoadmap(id) {
    return api.get(`/roadmaps/${id}`)
  },
  
  // 创建路线图
  createRoadmap(roadmapData) {
    return api.post('/roadmaps', roadmapData)
  },
  
  // 更新路线图
  updateRoadmap(id, roadmapData) {
    return api.put(`/roadmaps/${id}`, roadmapData)
  },
  
  // 删除路线图
  deleteRoadmap(id) {
    return api.delete(`/roadmaps/${id}`)
  }
}

// 思维导图相关API
export const mindmapAPI = {
  // 获取思维导图列表
  getMindmaps(params = {}) {
    return api.get('/mindmaps', { params })
  },
  
  // 获取思维导图详情
  getMindmap(id) {
    return api.get(`/mindmaps/${id}`)
  },
  
  // 创建思维导图
  createMindmap(mindmapData) {
    return api.post('/mindmaps', mindmapData)
  },
  
  // 更新思维导图
  updateMindmap(id, mindmapData) {
    return api.put(`/mindmaps/${id}`, mindmapData)
  },
  
  // 删除思维导图
  deleteMindmap(id) {
    return api.delete(`/mindmaps/${id}`)
  }
}

// 标签相关API
export const tagAPI = {
  // 获取标签列表
  getTags(params = {}) {
    return api.get('/tags', { params })
  },
  
  // 获取标签详情
  getTag(id) {
    return api.get(`/tags/${id}`)
  },
  
  // 创建标签
  createTag(tagData) {
    return api.post('/tags', tagData)
  },
  
  // 更新标签
  updateTag(id, tagData) {
    return api.put(`/tags/${id}`, tagData)
  },
  
  // 删除标签
  deleteTag(id) {
    return api.delete(`/tags/${id}`)
  },
  
  // 获取标签关系图
  getTagGraph(userId) {
    return api.get('/tags/graph', { params: { user_id: userId } })
  },
  
  // 验证标签关系
  validateRelation(relationData) {
    return api.post('/tags/validate-relation', relationData)
  },
  
  // 创建标签关系
  createRelation(relationData) {
    return api.post('/tags/relations', relationData)
  },
  
  // 删除标签关系
  deleteRelation(id) {
    return api.delete(`/tags/relations/${id}`)
  }
}

// 文件上传相关API
export const uploadAPI = {
  // 上传图片
  uploadImage(file) {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/upload/image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
  
  // 获取上传文件列表
  getUploads(params = {}) {
    return api.get('/upload', { params })
  },
  
  // 删除上传文件
  deleteUpload(id) {
    return api.delete(`/upload/${id}`)
  }
}

// 管理员相关API
export const adminAPI = {
  // 管理员注册
  register(userData) {
    return api.post('/admin/register', userData)
  },
  
  // 管理员登录
  login(credentials) {
    return api.post('/admin/login', credentials)
  },
  
  // 获取标签列表
  getTags(params = {}) {
    return api.get('/admin/tags', { params })
  },
  
  // 创建标签文章
  createTag(tagData) {
    return api.post('/admin/tags', tagData)
  },
  
  // 更新标签文章
  updateTag(id, tagData) {
    return api.put(`/admin/tags/${id}`, tagData)
  },
  
  // 删除标签文章
  deleteTag(id) {
    return api.delete(`/admin/tags/${id}`)
  }
}

export default api

