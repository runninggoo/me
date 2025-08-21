// src/components/Mindmap/ContextMenu.vue
<script setup>
import { computed } from 'vue';

const props = defineProps({
  isVisible: Boolean,
  position: Object, // { top, left }
  isNode: Boolean, // to check if the click was on a node or the canvas
});

const emit = defineEmits(['add', 'copy', 'cut', 'paste', 'delete', 'close']);

const menuStyle = computed(() => {
  if (!props.isVisible) return { display: 'none' };
  return {
    top: `${props.position.top}px`,
    left: `${props.position.left}px`,
  };
});
</script>

<template>
  <div v-if="isVisible" class="context-menu" :style="menuStyle">
    <ul>
      <li v-if="isNode" @click="emit('add')">添加子节点</li>
      <li v-if="isNode" @click="emit('copy')">复制节点</li>
      <li v-if="isNode" @click="emit('cut')">剪切节点</li>
      <li @click="emit('paste')">粘贴节点</li>
      <li v-if="isNode" @click="emit('delete')">删除节点</li>
    </ul>
  </div>
</template>

<style scoped>
.context-menu {
  position: absolute;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 5px 0;
  min-width: 120px;
  z-index: 1000;
}

.context-menu ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.context-menu li {
  padding: 8px 15px;
  cursor: pointer;
  font-size: 14px;
}

.context-menu li:hover {
  background-color: #f0f0f0;
}
</style>