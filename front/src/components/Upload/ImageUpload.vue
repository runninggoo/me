<template>
  <div class="image-upload">
    <!-- 上传区域 -->
    <div
      @click="triggerFileInput"
      @dragover.prevent
      @drop.prevent="handleDrop"
      :class="[
        'upload-area',
        { 'drag-over': isDragOver, 'uploading': uploading }
      ]"
    >
      <input
        ref="fileInput"
        type="file"
        accept="image/*"
        multiple
        @change="handleFileSelect"
        class="hidden"
      />
      
      <div v-if="!uploading" class="upload-content">
        <svg class="upload-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
        </svg>
        <p class="upload-text">点击或拖拽图片到此处上传</p>
        <p class="upload-hint">支持 PNG、JPG、JPEG、GIF、WebP 格式</p>
      </div>
      
      <div v-else class="uploading-content">
        <div class="spinner"></div>
        <p>上传中... {{ uploadProgress }}%</p>
      </div>
    </div>

    <!-- 上传进度 -->
    <div v-if="uploading" class="progress-bar">
      <div class="progress-fill" :style="{ width: uploadProgress + '%' }"></div>
    </div>

    <!-- 错误信息 -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <!-- 已上传的图片列表 -->
    <div v-if="uploadedImages.length > 0" class="uploaded-images">
      <h4>已上传的图片</h4>
      <div class="image-grid">
        <div
          v-for="image in uploadedImages"
          :key="image.id"
          class="image-item"
        >
          <img :src="image.file_url" :alt="image.filename" class="image-preview" />
          <div class="image-overlay">
            <button
              @click="copyImageUrl(image.file_url)"
              class="action-btn copy-btn"
              title="复制链接"
            >
              <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
            </button>
            <button
              @click="insertImage(image.file_url)"
              class="action-btn insert-btn"
              title="插入编辑器"
            >
              <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
            </button>
            <button
              @click="deleteImage(image.id)"
              class="action-btn delete-btn"
              title="删除"
            >
              <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
          <div class="image-info">
            <p class="image-name">{{ image.filename }}</p>
            <p class="image-size">{{ formatFileSize(image.file_size) }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { uploadAPI } from '../../services/api.js'

const emit = defineEmits(['image-inserted'])

// 响应式数据
const fileInput = ref(null)
const isDragOver = ref(false)
const uploading = ref(false)
const uploadProgress = ref(0)
const error = ref('')
const uploadedImages = ref([])

// 方法
const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = (event) => {
  const files = Array.from(event.target.files)
  uploadFiles(files)
}

const handleDrop = (event) => {
  isDragOver.value = false
  const files = Array.from(event.dataTransfer.files).filter(file => 
    file.type.startsWith('image/')
  )
  if (files.length > 0) {
    uploadFiles(files)
  }
}

const uploadFiles = async (files) => {
  if (files.length === 0) return

  uploading.value = true
  uploadProgress.value = 0
  error.value = ''

  try {
    for (let i = 0; i < files.length; i++) {
      const file = files[i]
      
      // 检查文件大小（限制为5MB）
      if (file.size > 5 * 1024 * 1024) {
        error.value = `文件 ${file.name} 超过5MB限制`
        continue
      }

      const formData = new FormData()
      formData.append('file', file)

      const response = await uploadAPI.uploadImage(formData, (progress) => {
        uploadProgress.value = Math.round((i / files.length + progress / files.length) * 100)
      })

      if (response.success) {
        uploadedImages.value.unshift(response.data)
      } else {
        error.value = response.error || '上传失败'
      }
    }
  } catch (err) {
    error.value = '上传失败：' + (err.message || '网络错误')
  } finally {
    uploading.value = false
    uploadProgress.value = 0
    // 清空文件输入
    if (fileInput.value) {
      fileInput.value.value = ''
    }
  }
}

const copyImageUrl = async (url) => {
  try {
    const fullUrl = url.startsWith('http') ? url : `${window.location.origin}${url}`
    await navigator.clipboard.writeText(fullUrl)
    // 可以添加一个提示消息
    console.log('图片链接已复制到剪贴板')
  } catch (err) {
    console.error('复制失败:', err)
  }
}

const insertImage = (url) => {
  emit('image-inserted', url)
}

const deleteImage = async (imageId) => {
  if (!confirm('确定要删除这张图片吗？')) return

  try {
    const response = await uploadAPI.deleteUpload(imageId)
    if (response.success) {
      uploadedImages.value = uploadedImages.value.filter(img => img.id !== imageId)
    } else {
      error.value = response.error || '删除失败'
    }
  } catch (err) {
    error.value = '删除失败：' + (err.message || '网络错误')
  }
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const loadUploadedImages = async () => {
  try {
    const response = await uploadAPI.getUploads({ page: 1, limit: 20 })
    if (response.success) {
      uploadedImages.value = response.data.uploads || []
    }
  } catch (err) {
    console.error('加载图片列表失败:', err)
  }
}

// 拖拽事件处理
const handleDragOver = () => {
  isDragOver.value = true
}

const handleDragLeave = () => {
  isDragOver.value = false
}

onMounted(() => {
  loadUploadedImages()
})
</script>

<style scoped>
.image-upload {
  width: 100%;
}

.upload-area {
  border: 2px dashed #d1d5db;
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: #f9fafb;
}

.upload-area:hover,
.upload-area.drag-over {
  border-color: #6366f1;
  background-color: #f0f9ff;
}

.upload-area.uploading {
  cursor: not-allowed;
  opacity: 0.7;
}

.hidden {
  display: none;
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.upload-icon {
  width: 3rem;
  height: 3rem;
  color: #6b7280;
}

.upload-text {
  font-size: 1.1rem;
  font-weight: 500;
  color: #374151;
  margin: 0;
}

.upload-hint {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0;
}

.uploading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.spinner {
  width: 2rem;
  height: 2rem;
  border: 3px solid #e5e7eb;
  border-top: 3px solid #6366f1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.progress-bar {
  width: 100%;
  height: 4px;
  background-color: #e5e7eb;
  border-radius: 2px;
  margin-top: 1rem;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: #6366f1;
  transition: width 0.3s ease;
}

.error-message {
  color: #dc2626;
  font-size: 0.875rem;
  margin-top: 0.5rem;
  padding: 0.5rem;
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 4px;
}

.uploaded-images {
  margin-top: 2rem;
}

.uploaded-images h4 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 1rem;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.image-item {
  position: relative;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
  background-color: white;
}

.image-preview {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.image-item:hover .image-overlay {
  opacity: 1;
}

.action-btn {
  width: 2rem;
  height: 2rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.action-btn svg {
  width: 1rem;
  height: 1rem;
}

.copy-btn {
  background-color: #3b82f6;
  color: white;
}

.copy-btn:hover {
  background-color: #2563eb;
}

.insert-btn {
  background-color: #10b981;
  color: white;
}

.insert-btn:hover {
  background-color: #059669;
}

.delete-btn {
  background-color: #ef4444;
  color: white;
}

.delete-btn:hover {
  background-color: #dc2626;
}

.image-info {
  padding: 0.5rem;
}

.image-name {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.image-size {
  font-size: 0.75rem;
  color: #6b7280;
  margin: 0.25rem 0 0 0;
}
</style>

