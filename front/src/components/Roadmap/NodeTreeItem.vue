<template>
  <li>
    <div @click.stop="$emit('select', node)" :class="{ selected: selectedId === node.id }">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="3" width="18" height="18" rx="2" ry="2" fill="rgba(100, 116, 139, 0.2)"></rect>
      </svg>
      <span>{{ node.data.label || node.id }}</span>
    </div>
    <ul v-if="node.children && node.children.length">
      <NodeTreeItem 
        v-for="child in node.children" 
        :key="child.id" 
        :node="child"
        :selected-id="selectedId"
        @select="(n) => $emit('select', n)"
      />
    </ul>
  </li>
</template>

<script setup>
defineProps({
  node: {
    type: Object,
    required: true,
  },
  selectedId: String,
});

defineEmits(['select']);
</script>

<style scoped>
ul {
  padding-left: 20px;
  list-style-type: none;
  margin: 0;
  border-left: 1px solid #e5e7eb;
  margin-left: 8px;
}
li {
  margin: 2px 0;
}
div {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 8px;
  cursor: pointer;
  border-radius: 4px;
  color: #374151;
  font-size: 14px;
}
div:hover {
  background-color: #f9fafb;
}
.selected {
  background-color: #dbeafe;
  font-weight: 600;
  color: #1e40af;
}
</style>