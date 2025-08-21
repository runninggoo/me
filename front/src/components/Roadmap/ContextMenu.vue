<template>
  <div
    v-if="visible"
    class="context-menu"
    :style="{ top: position.y + 'px', left: position.x + 'px' }"
    @click.stop
  >
    <ul>
      <li @click="$emit('select-option', 'copy')">复制节点</li>
      <li @click="$emit('select-option', 'delete')">删除节点</li>
      <li @click="$emit('select-option', 'transfer')">转移归属权</li>
    </ul>
  </div>
</template>

<script setup>
defineProps({
  visible: Boolean,
  position: {
    type: Object,
    default: () => ({ x: 0, y: 0 }),
  },
});
defineEmits(['select-option']);
</script>

<style scoped>
.context-menu {
  position: fixed;
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  z-index: 1000;
  padding: 0;
  min-width: 150px;
}
.context-menu ul {
  list-style: none;
  padding: 5px 0;
  margin: 0;
}
.context-menu li {
  padding: 8px 15px;
  cursor: pointer;
  font-size: 14px;
  color: #334155;
}
.context-menu li:hover {
  background-color: #f1f5f9;
}
</style>