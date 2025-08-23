<!-- src/components/Roadmap/ListNode.vue -->
<template>
  <div class="list-node-card" :style="themeStyles">
    <div class="title-bar">{{ data.label }}</div>
    <ul v-if="data.items?.length" class="list-items">
      <li v-for="(item, index) in data.items" :key="item.id" :class="{ 'is-done': item.status === 'done' }" @click.stop="toggleItemStatus(index)" >
        <span class="checkbox"></span>
        <span>{{ item.label }}</span>
      </li>
    </ul>

    <Handle v-for="pos in ['top', 'right', 'bottom', 'left']" :key="pos" :id="pos" :type="data.handles?.[pos]" :position="Position[pos.charAt(0).toUpperCase() + pos.slice(1)]" />
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { Handle, Position } from '@vue-flow/core';
import { ColorThemes } from 'src/data/RoadmapnodeDefinitions';

const props = defineProps({ data: Object });
const emit = defineEmits(['updateNodeData']);

const theme = computed(() => ColorThemes[props.data.color?.toUpperCase()] || ColorThemes.PURPLE);
const themeStyles = computed(() => ({ '--theme-color': theme.value.color }));

const toggleItemStatus = (index) => {
  const newItems = JSON.parse(JSON.stringify(props.data.items));
  const currentStatus = newItems[index].status;
  
  newItems[index].status = currentStatus === 'done' ? 'todo' : 'done';
  emit('updateNodeData', { items: newItems });
};
</script>

<style scoped>
.list-node-card {
  --theme-color: #8b5cf6;
  background-color: #f9fafb;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  min-width: 220px;
  position: relative;
}
.title-bar { 
  padding: 8px 12px; 
  font-weight: 600; 
  border-bottom: 1px solid #e5e7eb; 
}
.list-items { 
  list-style: none; 
  padding: 12px; 
  margin: 0; 
  display: flex; 
  flex-direction: column; 
  gap: 8px; 
}
li { 
  display: flex; 
  align-items: center; 
  gap: 8px; 
  font-size: 14px;
  cursor: pointer;
}
.checkbox { 
  width: 14px; 
  height: 14px; 
  border: 1.5px solid #d1d5db; 
  border-radius: 3px; 
  position: relative; 
}
li.is-done { 
  color: #9ca3af; 
  text-decoration: line-through; 
}
li.is-done .checkbox { 
  border-color: var(--theme-color); 
  background-color: var(--theme-color); 
}
li.is-done .checkbox::after { 
  content: '✔'; 
  position: absolute; 
  top: 50%; 
  left: 50%; 
  transform: translate(-50%,-55%); 
  font-size: 10px; 
  color: white; 
}

:deep(.vue-flow__handle) {
  width: 8px; 
  height: 8px; 
  background: #9ca3af;
  opacity: 0; 
  transition: opacity 0.2s;
}
.list-node-card:hover :deep(.vue-flow__handle),
.vue-flow__node-list.selected :deep(.vue-flow__handle) {
  opacity: 1;
}
</style>