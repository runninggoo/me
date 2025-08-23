<!-- src/components/Roadmap/TopicNode.vue -->
<template>
  <div class="topic-node-card" :style="themeStyles">
    <div v-if="data.label" class="title-bar" :style="{ textAlign: data.textAlign || 'left' }">
      {{ data.label }}
    </div>
    <div v-if="data.description" class="content-area">
      {{ data.description }}
    </div>

    <Handle v-for="pos in ['top', 'right', 'bottom', 'left']" :key="pos" :id="pos" :type="data.handles?.[pos]" :position="Position[pos.charAt(0).toUpperCase() + pos.slice(1)]" />
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { Handle, Position } from '@vue-flow/core';
import { ColorThemes } from 'src/data/RoadmapnodeDefinitions';

const props = defineProps({ data: Object });

const theme = computed(() => ColorThemes[props.data.color?.toUpperCase()] || ColorThemes.GRAY);
const themeStyles = computed(() => ({ '--theme-color': theme.value.color }));
</script>

<style scoped>
.topic-node-card {
  background-color: #ffffff;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  min-width: 200px;
  max-width: 300px;
  position: relative;
}
.vue-flow__node-topic.selected .topic-node-card {
  border-color: var(--theme-color);
  box-shadow: 0 0 0 2px var(--theme-color);
}

.title-bar {
  background-color: var(--theme-color);
  color: white;
  padding: 8px 12px;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
  font-weight: 600;
}

.content-area {
  padding: 12px;
  font-size: 14px;
  color: #4b5563;
  line-height: 1.5;
  /* 如果标题栏存在，则添加上边框 */
  border-top: 1px solid #e5e7eb;
}


/* 连接点样式 */
:deep(.vue-flow__handle) {
  width: 8px; height: 8px; background: #9ca3af;
  opacity: 0; transition: opacity 0.2s;
}
.topic-node-card:hover :deep(.vue-flow__handle),
.vue-flow__node-topic.selected :deep(.vue-flow__handle) {
  opacity: 1;
}
</style>