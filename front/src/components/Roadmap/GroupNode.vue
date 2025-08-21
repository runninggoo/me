<template>
  <div class="group-node-wrapper">
    <div :style="containerStyle" :class="['group-node-body', { selected: node.selected }]">
      <div class="group-node-label" :style="labelStyle">
      {{ data.label }}
    </div>
      <div class="group-node-content"></div>
      <NodeResizer
        v-if="node.selected" 
        :min-width="150"
        :min-height="100"
        :color="resizeColor"
        @resize-end="onResizeEnd"
      />
      <Handle
        v-for="pos in ['top', 'right', 'bottom', 'left']"
        :id="pos"
        :key="pos"
        :type="data.handles?.[pos]"
        :position="Position[pos.charAt(0).toUpperCase() + pos.slice(1)]"
      />
    </div>
  </div>
</template>

<script setup>
/* SCRIPT部分完全不变 */
import { computed } from 'vue';
import { Handle, Position, useNode } from '@vue-flow/core';
import { NodeResizer } from '@vue-flow/node-resizer';
import '@vue-flow/node-resizer/dist/style.css';
import { ColorThemes } from 'src/data/RoadmapnodeDefinitions';

const { node } = useNode();
const data = computed(() => node.data || {});
const emit = defineEmits(['resize']);

function onResizeEnd(params) {
  emit('resize', { id: node.id, width: params.width, height: params.height });
}

const theme = computed(() => ColorThemes[data.value.color?.toUpperCase()] || { color: '#cbd5e1' });

const containerStyle = computed(() => ({
  '--theme-color': theme.value.color,
  borderColor: 'var(--theme-color)',
}));

const labelStyle = computed(() => ({
  // 标题颜色可以与主题色关联，但背景是透明的
  color: theme.value.color,
}));

const resizeColor = computed(() => theme.value.color);
</script>

<style scoped>
/* 整体wrapper，确保布局正确 */
.group-node-wrapper {
  /* Vue Flow 会控制此容器的大小 */
  width: 100%;
  height: 100%;
  /* 使用flex布局来分离标题和主体 */
  display: flex;
  flex-direction: column;
}

.group-node-label {
  font-size: 1rem;
  font-weight: 600;
  text-align: left;
  flex-shrink: 0; /* 防止标题被压缩 */
  cursor: grab;
  user-select: none;
  padding: 10px 10px;
}

.group-node-body {
  position: relative; /* 为内部的 Resizer 和 Handle 提供定位上下文 */
  width: 100%;
  flex-grow: 1;
  background: rgba(248, 250, 252, 0.7);
  border: 1px solid;
  border-radius: 6px;
  box-sizing: border-box;
  backdrop-filter: blur(2px);
  transition: border-color 200ms ease-in-out, box-shadow 200ms ease-in-out;
}

.group-node-body.selected {
  box-shadow: 0 0 0 2px var(--theme-color);
}

.group-node-content {
  width: 100%;
  height: 100%;
}

/* 连接点样式统一 */
:deep(.vue-flow__handle) {
  width: 8px; height: 8px; background: #9ca3af;
  opacity: 0; transition: opacity 0.2s;
}

.group-node-body:hover :deep(.vue-flow__handle),
.group-node-body.selected :deep(.vue-flow__handle) {
  opacity: 1;
}

:deep(.vue-flow__handle-top) { transform: translate(-50%, -50%); }
:deep(.vue-flow__handle-bottom) { transform: translate(-50%, 50%); }
:deep(.vue-flow__handle-left) { transform: translate(-50%, -50%); }
:deep(.vue-flow__handle-right) { transform: translate(50%, -50%); }
</style>