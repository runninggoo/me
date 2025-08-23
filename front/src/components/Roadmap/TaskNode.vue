<!-- src/components/Roadmap/TaskNode.vue -->
<template>
  <div :class="['task-node-card', { 'is-done': data.status === 'done' }]" :style="themeStyles">
    <div class="animated-fill"></div>

    <div class="content-area">
      <span class="task-label">{{ data.label }}</span>
    </div>

    <button v-if="data.hasStatus" class="status-toggle" @click.stop="toggleStatus">
      <span v-if="data.status !== 'done'">></span>
      <span v-else><</span>
    </button>
    

    <Handle v-for="pos in ['top', 'right', 'bottom', 'left']" :key="pos" :id="pos" :type="data.handles?.[pos]" :position="Position[pos.charAt(0).toUpperCase() + pos.slice(1)]" />
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { Handle, Position } from '@vue-flow/core';
import { ColorThemes } from 'src/data/RoadmapnodeDefinitions';

const props = defineProps({ data: Object });
const emit = defineEmits(['updateNodeData']);

const theme = computed(() => ColorThemes[props.data.color?.toUpperCase()] || ColorThemes.BLUE);
const themeStyles = computed(() => ({ '--theme-color': theme.value.color }));

const toggleStatus = () => {
  const newStatus = props.data.status === 'done' ? 'todo' : 'done';
  emit('updateNodeData', { status: newStatus });
};
</script>

<style scoped>
.task-node-card {
  --theme-color: #3b82f6;
  position: relative;
  overflow: hidden; 
  
  background-color: #ffffff;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  min-width: 200px;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.vue-flow__node-task.selected .task-node-card {
  border-color: var(--theme-color);
  box-shadow: 0 0 0 2px var(--theme-color);
}

.animated-fill {
  position: absolute; top: 0; left: 0;
  width: 100%; height: 100%;
  background-color: var(--theme-color);
  transform: translateX(-101%);
  transition: transform 0.4s cubic-bezier(0.23, 1, 0.32, 1);
  z-index: 1;
}
.is-done .animated-fill {
  transform: translateX(0);
}

.content-area {
  position: relative;
  z-index: 2;
  padding: 12px;
  padding-right: 40px;
}
.task-label {
  font-size: 14px;
  font-weight: 500;
  color: #4b5563;
  transition: color 0.4s;
}
.is-done .task-label {
  color: white;
}

.status-toggle {
  position: absolute;
  top: 0; right: 0; bottom: 0;
  width: 36px;
  z-index: 2;

  background-color: transparent;
  border: none;
  border-left: 1px solid #e5e7eb;
  color: #6b7280;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  transition: all 0.4s;
}
.status-toggle:hover {
  background-color: rgba(0,0,0,0.03);
}
.is-done .status-toggle {
  color: white;
  border-left-color: rgba(255,255,255,0.3);
}

:deep(.vue-flow__handle) {
  width: 8px; height: 8px; background: #9ca3af;
  opacity: 0; transition: opacity 0.2s;
  z-index: 3;
}
.task-node-card:hover :deep(.vue-flow__handle),
.vue-flow__node-task.selected :deep(.vue-flow__handle) {
  opacity: 1;
}
</style>