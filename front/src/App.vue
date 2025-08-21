<!-- src/App.vue -->
<template>
  <div class="app-container">
    <!-- 顶部导航栏 -->
    <nav class="top-nav">
      <button v-for="tab in tabs" :key="tab.key" :class="{ active: activeTab === tab.key }"
        @click="activeTab = tab.key">
        {{ tab.label }}
      </button>
    </nav>

    <!-- 三个编辑器视图，按当前 tab 显示一个 -->
    <main class="app-main">
      <!-- 1. Roadmap -->
      <RoadmapEditor v-if="activeTab === 'roadmap'" v-model="roadmapjson" />

      <!-- 2. Article -->
      <TiptapEditor v-if="activeTab === 'article'" v-model="articleJson"/>

      <!-- 3. Mindmap -->
      <MindMapEditor v-if="activeTab === 'mindmap'" v-model="mindmapJson" />

    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { initialRoadmap,initialArticle,initialMindmap } from 'src/data/initial-elements.js'
import RoadmapEditor from 'src/components/Roadmap/RoadmapEditor.vue'
import TiptapEditor from 'src/components/Article/TiptapEditor.vue'
import MindMapEditor from 'src/components/Mindmap/MindMapEditor.vue'

/* -------------------- 顶部 Tab 切换 -------------------- */
const tabs = [
  { key: 'roadmap', label: 'Roadmap' },
  { key: 'article', label: 'Article' },
  { key: 'mindmap', label: 'MindMap' }
]
const activeTab = ref('roadmap')

/* Roadmap 数据源 */
const roadmapjson = ref(initialRoadmap)

/* Article 数据源 */
const articleJson = ref(initialArticle)

/* Mindmap 数据源 */
const mindmapJson = ref(initialMindmap)

</script>

<style>
html,
body {
  margin: 0;
  height: 100%;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: #f0f2f5;
  color: #333;
}

#app {
  height: 100vh;
}
</style>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f0f2f5;
}

/* 顶部导航栏样式 */
.top-nav {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 16px;
  background: #f0f0f0;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  z-index: 10;
}

.top-nav button {
  padding: 6px 14px;
  border: none;
  border-radius: 4px;
  background: transparent;
  cursor: pointer;
  font-size: 14px;
  color: #555;
  transition: background 0.2s;
}

.top-nav button:hover {
  background: #f2f2f2;
}

.top-nav button.active {
  background: #e6f4ff;
  color: #1677ff;
  font-weight: 600;
}

.app-main {
  flex: 1;
  position: relative;
}
</style>