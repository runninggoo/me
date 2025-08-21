<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <h3>转移节点归属权</h3>
      <p class="modal-description">请选择一个新的父节点，或选择“主画布”以取消归属。</p>
      <div class="tree-container">
        <ul>
          <li @click="selectParent(null)" :class="{ selected: selectedParentId === null }" class="root-canvas">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect></svg>
            <span>主画布 (无归属)</span>
          </li>
          <NodeTreeItem
            v-for="node in nodesTree"
            :key="node.id"
            :node="node"
            :selected-id="selectedParentId"
            @select="selectParent"
          />
        </ul>
      </div>
      <div class="selection-info">
        当前选择: <strong>{{ selectedNodeName }}</strong>
      </div>
      <div class="modal-actions">
        <button @click="closeModal" class="btn-secondary">取消</button>
        <button @click="confirm" class="btn-primary">确定</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import NodeTreeItem from './NodeTreeItem.vue';

const props = defineProps({
  modelValue: Boolean,
  nodesTree: {
    type: Array,
    required: true,
  },
});

const emit = defineEmits(['update:modelValue', 'confirm']);

const selectedParentId = ref(null);

function selectParent(node) {
  selectedParentId.value = node ? node.id : null;
}

function findNodeName(nodes, id) {
  if (id === null) return '主画布';
  for (const node of nodes) {
    if (node.id === id) return node.data.label || node.id;
    if (node.children && node.children.length) {
      const found = findNodeName(node.children, id);
      if (found) return found;
    }
  }
  return '未知';
}

const selectedNodeName = computed(() => {
  return findNodeName(props.nodesTree, selectedParentId.value);
});

function closeModal() {
  emit('update:modelValue', false);
}

function confirm() {
  emit('confirm', selectedParentId.value);
  // The call to closeModal() is removed from here
  // as the parent component will handle closing upon successful confirmation.
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}
.modal-content {
  background: white;
  padding: 24px;
  border-radius: 8px;
  min-width: 420px;
  max-width: 90vw;
  box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
}
.modal-content h3 {
  margin-top: 0;
  color: #111827;
}
.modal-description {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 16px;
}
.tree-container {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #e5e7eb;
  padding: 10px;
  margin: 15px 0;
  border-radius: 6px;
}
.tree-container ul {
  padding-left: 0;
  list-style-type: none;
  margin: 0;
}
.root-canvas {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 8px;
  cursor: pointer;
  border-radius: 4px;
  color: #374151;
  font-size: 14px;
}
.root-canvas:hover {
  background-color: #f9fafb;
}
.tree-container .selected {
  background-color: #dbeafe;
  font-weight: 600;
  color: #1e40af;
}
.selection-info {
  margin-top: 10px;
  font-size: 14px;
  color: #4b5563;
}
.selection-info strong {
    color: #1f2937;
}
.modal-actions {
  margin-top: 24px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
.modal-actions button {
  padding: 8px 16px;
  border-radius: 6px;
  border: 1px solid transparent;
  font-weight: 500;
  cursor: pointer;
}
.btn-primary {
  background-color: #3b82f6;
  color: white;
}
.btn-primary:hover {
  background-color: #2563eb;
}
.btn-secondary {
  background-color: #fff;
  border-color: #d1d5db;
  color: #374151;
}
.btn-secondary:hover {
  background-color: #f9fafb;
}
</style>