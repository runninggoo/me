<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from './stores/auth.js'

const authStore = useAuthStore()

onMounted(() => {
  // 初始化认证状态
  authStore.initAuth()
})
</script>

<style>
/* 全局样式 */
html, body {
  margin: 0;
  height: 100%;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: #f0f2f5;
  color: #333;
}

#app {
  min-height: 100vh;
}

* {
  box-sizing: border-box;
}

/* Tailwind CSS 基础样式 */
.bg-gray-50 { background-color: #f9fafb; }
.bg-white { background-color: #ffffff; }
.bg-indigo-600 { background-color: #4f46e5; }
.bg-indigo-700 { background-color: #4338ca; }
.bg-red-600 { background-color: #dc2626; }
.bg-red-700 { background-color: #b91c1c; }

.text-gray-900 { color: #111827; }
.text-gray-700 { color: #374151; }
.text-gray-600 { color: #4b5563; }
.text-gray-500 { color: #6b7280; }
.text-white { color: #ffffff; }
.text-indigo-600 { color: #4f46e5; }
.text-indigo-500 { color: #6366f1; }
.text-red-600 { color: #dc2626; }
.text-red-500 { color: #ef4444; }

.border { border-width: 1px; }
.border-gray-300 { border-color: #d1d5db; }
.border-gray-200 { border-color: #e5e7eb; }
.border-transparent { border-color: transparent; }

.rounded { border-radius: 0.25rem; }
.rounded-md { border-radius: 0.375rem; }
.rounded-lg { border-radius: 0.5rem; }
.rounded-full { border-radius: 9999px; }

.shadow { box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06); }
.shadow-sm { box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); }
.shadow-md { box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); }

.px-3 { padding-left: 0.75rem; padding-right: 0.75rem; }
.px-4 { padding-left: 1rem; padding-right: 1rem; }
.px-6 { padding-left: 1.5rem; padding-right: 1.5rem; }
.py-2 { padding-top: 0.5rem; padding-bottom: 0.5rem; }
.py-3 { padding-top: 0.75rem; padding-bottom: 0.75rem; }
.py-4 { padding-top: 1rem; padding-bottom: 1rem; }
.py-6 { padding-top: 1.5rem; padding-bottom: 1.5rem; }
.py-8 { padding-top: 2rem; padding-bottom: 2rem; }
.py-12 { padding-top: 3rem; padding-bottom: 3rem; }

.m-0 { margin: 0; }
.mt-2 { margin-top: 0.5rem; }
.mt-4 { margin-top: 1rem; }
.mt-6 { margin-top: 1.5rem; }
.mt-8 { margin-top: 2rem; }
.mt-16 { margin-top: 4rem; }
.mb-8 { margin-bottom: 2rem; }
.ml-2 { margin-left: 0.5rem; }
.ml-4 { margin-left: 1rem; }

.w-full { width: 100%; }
.h-16 { height: 4rem; }
.h-8 { height: 2rem; }
.w-8 { width: 2rem; }
.h-12 { height: 3rem; }
.w-12 { width: 3rem; }

.flex { display: flex; }
.inline-flex { display: inline-flex; }
.grid { display: grid; }
.hidden { display: none; }

.items-center { align-items: center; }
.justify-center { justify-content: center; }
.justify-between { justify-content: space-between; }

.space-x-4 > * + * { margin-left: 1rem; }
.space-x-8 > * + * { margin-left: 2rem; }
.space-y-4 > * + * { margin-top: 1rem; }
.space-y-6 > * + * { margin-top: 1.5rem; }
.space-y-8 > * + * { margin-top: 2rem; }

.text-sm { font-size: 0.875rem; line-height: 1.25rem; }
.text-base { font-size: 1rem; line-height: 1.5rem; }
.text-lg { font-size: 1.125rem; line-height: 1.75rem; }
.text-xl { font-size: 1.25rem; line-height: 1.75rem; }
.text-2xl { font-size: 1.5rem; line-height: 2rem; }
.text-3xl { font-size: 1.875rem; line-height: 2.25rem; }
.text-4xl { font-size: 2.25rem; line-height: 2.5rem; }

.font-medium { font-weight: 500; }
.font-bold { font-weight: 700; }
.font-extrabold { font-weight: 800; }

.text-center { text-align: center; }

.min-h-screen { min-height: 100vh; }

.max-w-md { max-width: 28rem; }
.max-w-7xl { max-width: 80rem; }

.mx-auto { margin-left: auto; margin-right: auto; }

.grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
.grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }

.gap-4 { gap: 1rem; }
.gap-6 { gap: 1.5rem; }
.gap-8 { gap: 2rem; }

.overflow-hidden { overflow: hidden; }

.transition-shadow { transition-property: box-shadow; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 150ms; }

.hover\:shadow-md:hover { box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); }
.hover\:bg-indigo-700:hover { background-color: #4338ca; }
.hover\:bg-red-700:hover { background-color: #b91c1c; }
.hover\:text-gray-900:hover { color: #111827; }
.hover\:text-indigo-500:hover { color: #6366f1; }

.focus\:outline-none:focus { outline: 2px solid transparent; outline-offset: 2px; }
.focus\:ring-2:focus { box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.5); }
.focus\:ring-offset-2:focus { box-shadow: 0 0 0 2px #fff, 0 0 0 4px rgba(59, 130, 246, 0.5); }
.focus\:ring-indigo-500:focus { box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.5); }
.focus\:border-indigo-500:focus { border-color: #6366f1; }

.disabled\:opacity-50:disabled { opacity: 0.5; }
.disabled\:cursor-not-allowed:disabled { cursor: not-allowed; }

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 响应式样式 */
@media (min-width: 640px) {
  .sm\:px-6 { padding-left: 1.5rem; padding-right: 1.5rem; }
  .sm\:text-sm { font-size: 0.875rem; line-height: 1.25rem; }
  .sm\:text-4xl { font-size: 2.25rem; line-height: 2.5rem; }
  .sm\:grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .sm\:grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .sm\:px-0 { padding-left: 0; padding-right: 0; }
}

@media (min-width: 1024px) {
  .lg\:px-8 { padding-left: 2rem; padding-right: 2rem; }
  .lg\:grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
}

/* 表单样式 */
input, textarea, select {
  appearance: none;
  background-color: #ffffff;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  line-height: 1.25rem;
  color: #111827;
}

input:focus, textarea:focus, select:focus {
  outline: 2px solid transparent;
  outline-offset: 2px;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

button {
  cursor: pointer;
  border: none;
  border-radius: 0.375rem;
  font-weight: 500;
  transition: all 0.15s ease-in-out;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 链接样式 */
a {
  color: #4f46e5;
  text-decoration: none;
}

a:hover {
  color: #6366f1;
  text-decoration: underline;
}
</style>

