<template>
  <div 
    :class="['text-node-wrapper', `variant-${data.variant || 'title'}`]"
    :style="{ width: data.width ? `${data.width}px` : 'auto', textAlign: data.textAlign || 'left'}"
  >
    {{ data.label }}
  </div>
</template>

<script setup>
defineProps({
  data: Object,
});
</script>

<style scoped>
.text-node-wrapper {
  resize: horizontal;
  overflow: hidden;
  white-space: pre-wrap;
  word-break: break-word;
  padding: 4px;
}
.text-node-wrapper::-webkit-resizer {
  display: none;
}
.vue-flow__node-text.selected .text-node-wrapper {
  outline: 1px dashed #3b82f6;
  outline-offset: 2px;
}

.variant-title {
  font-size: 24px;
  font-weight: 700;
  color: #111827;
}

.variant-paragraph {
  font-size: 14px;
  color: #374151;
  line-height: 1.6;
}
</style>