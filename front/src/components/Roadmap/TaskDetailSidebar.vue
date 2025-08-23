<template>
  <aside class="task-sidebar">
    <div class="task-sidebar-content">
      <button class="close-btn" @click="$emit('close')">></button>
      <h2>{{ node.data.label }}</h2>
      <p v-if="node.data.url">
        <a :href="node.data.url" target="_blank" rel="noopener">{{ node.data.url }}</a>
      </p>
      <p v-else>暂无链接</p>
    </div>
  </aside>
</template>

<script setup>
defineProps({ node: Object })
defineEmits(['close'])
</script>

<style scoped>
.task-sidebar {
  position: fixed;
  top: 0;
  right: 0;
  width: 60%;
  height: 100%;
  background: #fff;
  border-left: 1px solid #e2e8f0;
  box-shadow: -4px 0 16px rgba(0,0,0,.05);
  z-index: 10;
  display: flex;
  flex-direction: column;
  padding: 2rem;
}
.close-btn {
  font-size: 24px;
  margin-top: auto;
  align-self: flex-start;

  background-color: transparent;
  border: none;
  cursor: pointer;

  padding: 4px 8px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.close-btn:hover {
  background-color: rgba(0, 0, 0, 0.08);
}
</style>