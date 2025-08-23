// src/stores/content.js
import { defineStore } from 'pinia'
import { articleAPI, roadmapAPI, mindmapAPI, tagAPI } from '../services/api.js'

export const useContentStore = defineStore('content', {
  state: () => ({
    // 当前编辑的内容
    currentArticle: null,
    currentRoadmap: null,
    currentMindmap: null,
    
    // 内容列表
    articles: [],
    roadmaps: [],
    mindmaps: [],
    tags: [],
    
    // 加载状态
    loading: false,
    saving: false,
    
    // 分页信息
    articlePagination: null,
    roadmapPagination: null,
    mindmapPagination: null
  }),

  getters: {
    // 获取当前用户的标签
    userTags: (state) => state.tags,
    
    // 检查是否有未保存的更改
    hasUnsavedChanges: (state) => {
      return !!(state.currentArticle?.isDirty || 
                state.currentRoadmap?.isDirty || 
                state.currentMindmap?.isDirty)
    }
  },

  actions: {
    // 文章相关操作
    async loadArticles(params = {}) {
      this.loading = true
      try {
        const response = await articleAPI.getArticles(params)
        if (response.success) {
          this.articles = response.data.articles
          this.articlePagination = response.data.pagination
        }
        return response
      } catch (error) {
        console.error('加载文章列表失败:', error)
        return { success: false, error: error.error || '加载失败' }
      } finally {
        this.loading = false
      }
    },

    async loadArticle(id) {
      this.loading = true
      try {
        const response = await articleAPI.getArticle(id)
        if (response.success) {
          this.currentArticle = { ...response.data, isDirty: false }
        }
        return response
      } catch (error) {
        console.error('加载文章失败:', error)
        return { success: false, error: error.error || '加载失败' }
      } finally {
        this.loading = false
      }
    },

    async saveArticle(articleData) {
      this.saving = true
      try {
        let response
        if (articleData.id) {
          response = await articleAPI.updateArticle(articleData.id, articleData)
        } else {
          response = await articleAPI.createArticle(articleData)
        }
        
        if (response.success) {
          this.currentArticle = { ...response.data, isDirty: false }
          // 更新列表中的文章
          const index = this.articles.findIndex(a => a.id === response.data.id)
          if (index >= 0) {
            this.articles[index] = response.data
          } else {
            this.articles.unshift(response.data)
          }
        }
        return response
      } catch (error) {
        console.error('保存文章失败:', error)
        return { success: false, error: error.error || '保存失败' }
      } finally {
        this.saving = false
      }
    },

    async deleteArticle(id) {
      try {
        const response = await articleAPI.deleteArticle(id)
        if (response.success) {
          this.articles = this.articles.filter(a => a.id !== id)
          if (this.currentArticle?.id === id) {
            this.currentArticle = null
          }
        }
        return response
      } catch (error) {
        console.error('删除文章失败:', error)
        return { success: false, error: error.error || '删除失败' }
      }
    },

    // 路线图相关操作
    async loadRoadmaps(params = {}) {
      this.loading = true
      try {
        const response = await roadmapAPI.getRoadmaps(params)
        if (response.success) {
          this.roadmaps = response.data.roadmaps
          this.roadmapPagination = response.data.pagination
        }
        return response
      } catch (error) {
        console.error('加载路线图列表失败:', error)
        return { success: false, error: error.error || '加载失败' }
      } finally {
        this.loading = false
      }
    },

    async loadRoadmap(id) {
      this.loading = true
      try {
        const response = await roadmapAPI.getRoadmap(id)
        if (response.success) {
          this.currentRoadmap = { ...response.data, isDirty: false }
        }
        return response
      } catch (error) {
        console.error('加载路线图失败:', error)
        return { success: false, error: error.error || '加载失败' }
      } finally {
        this.loading = false
      }
    },

    async saveRoadmap(roadmapData) {
      this.saving = true
      try {
        let response
        if (roadmapData.id) {
          response = await roadmapAPI.updateRoadmap(roadmapData.id, roadmapData)
        } else {
          response = await roadmapAPI.createRoadmap(roadmapData)
        }
        
        if (response.success) {
          this.currentRoadmap = { ...response.data, isDirty: false }
          const index = this.roadmaps.findIndex(r => r.id === response.data.id)
          if (index >= 0) {
            this.roadmaps[index] = response.data
          } else {
            this.roadmaps.unshift(response.data)
          }
        }
        return response
      } catch (error) {
        console.error('保存路线图失败:', error)
        return { success: false, error: error.error || '保存失败' }
      } finally {
        this.saving = false
      }
    },

    // 思维导图相关操作
    async loadMindmaps(params = {}) {
      this.loading = true
      try {
        const response = await mindmapAPI.getMindmaps(params)
        if (response.success) {
          this.mindmaps = response.data.mindmaps
          this.mindmapPagination = response.data.pagination
        }
        return response
      } catch (error) {
        console.error('加载思维导图列表失败:', error)
        return { success: false, error: error.error || '加载失败' }
      } finally {
        this.loading = false
      }
    },

    async loadMindmap(id) {
      this.loading = true
      try {
        const response = await mindmapAPI.getMindmap(id)
        if (response.success) {
          this.currentMindmap = { ...response.data, isDirty: false }
        }
        return response
      } catch (error) {
        console.error('加载思维导图失败:', error)
        return { success: false, error: error.error || '加载失败' }
      } finally {
        this.loading = false
      }
    },

    async saveMindmap(mindmapData) {
      this.saving = true
      try {
        let response
        if (mindmapData.id) {
          response = await mindmapAPI.updateMindmap(mindmapData.id, mindmapData)
        } else {
          response = await mindmapAPI.createMindmap(mindmapData)
        }
        
        if (response.success) {
          this.currentMindmap = { ...response.data, isDirty: false }
          const index = this.mindmaps.findIndex(m => m.id === response.data.id)
          if (index >= 0) {
            this.mindmaps[index] = response.data
          } else {
            this.mindmaps.unshift(response.data)
          }
        }
        return response
      } catch (error) {
        console.error('保存思维导图失败:', error)
        return { success: false, error: error.error || '保存失败' }
      } finally {
        this.saving = false
      }
    },

    // 标签相关操作
    async loadTags(userId) {
      try {
        const response = await tagAPI.getTags({ user_id: userId })
        if (response.success) {
          this.tags = response.data
        }
        return response
      } catch (error) {
        console.error('加载标签失败:', error)
        return { success: false, error: error.error || '加载失败' }
      }
    },

    async createTag(tagData) {
      try {
        const response = await tagAPI.createTag(tagData)
        if (response.success) {
          this.tags.push(response.data)
        }
        return response
      } catch (error) {
        console.error('创建标签失败:', error)
        return { success: false, error: error.error || '创建失败' }
      }
    },

    // 标记内容为已修改
    markArticleDirty() {
      if (this.currentArticle) {
        this.currentArticle.isDirty = true
      }
    },

    markRoadmapDirty() {
      if (this.currentRoadmap) {
        this.currentRoadmap.isDirty = true
      }
    },

    markMindmapDirty() {
      if (this.currentMindmap) {
        this.currentMindmap.isDirty = true
      }
    },

    // 创建新内容
    createNewArticle() {
      this.currentArticle = {
        id: null,
        title: '',
        content: {},
        excerpt: '',
        status: 'draft',
        tags: [],
        isDirty: false
      }
    },

    createNewRoadmap() {
      this.currentRoadmap = {
        id: null,
        title: '',
        description: '',
        content: {},
        status: 'draft',
        tags: [],
        isDirty: false
      }
    },

    createNewMindmap() {
      this.currentMindmap = {
        id: null,
        title: '',
        description: '',
        content: {},
        status: 'draft',
        tags: [],
        isDirty: false
      }
    },

    // 清除当前内容
    clearCurrentContent() {
      this.currentArticle = null
      this.currentRoadmap = null
      this.currentMindmap = null
    }
  }
})

