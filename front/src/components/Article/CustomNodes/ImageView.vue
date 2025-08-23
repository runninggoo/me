// src/components/Article/CustomNodes/ImageView.vue
<script setup>
import { nextTick } from 'vue';
import { nodeViewProps, NodeViewWrapper } from '@tiptap/vue-3';

const props = defineProps(nodeViewProps);

const changeSize = (delta) => {
  if (!props.editor.isEditable) return;
  const current = parseInt(props.node.attrs.width, 10) || 80
  const newWidth = Math.max(20, current + delta)

  // 1. 先更新属性
  props.updateAttributes({ width: `${newWidth}px` })

  // 2. 延迟一帧后把选区设回该节点
  nextTick(() => {
    // getPos() 是 NodeView 提供的，返回节点在文档中的绝对位置
    props.editor.commands.setNodeSelection(props.getPos())
  })
}
</script>

<template>
  <NodeViewWrapper as="span" class="inline-image-wrapper" contenteditable="false" draggable="true" data-drag-handle>
    <img :src="props.node.attrs.src" :alt="props.node.attrs.alt" :title="props.node.attrs.title"
      :style="{ width: props.node.attrs.width }" class="inline-image"
      :class="{ 'ProseMirror-selectednode': props.selected }" />

    <div v-if="props.selected && props.editor.isEditable" class="zoom-toolbar">
      <button @mousedown="changeSize(-10); ">-</button>
      <button @mousedown="changeSize(10); ">+</button>
    </div>
  </NodeViewWrapper>
</template>

<style lang="scss">
.inline-image-wrapper {
  display: inline-block;
  position: relative;
  line-height: 0;
  vertical-align: middle;
}

.inline-image {
  border: 2px solid transparent;
  border-radius: 4px;
  transition: border-color 0.2s;

  &.ProseMirror-selectednode {
    border-color: #68CEF8;
  }
}

.zoom-toolbar {
  position: absolute;
  top: -24px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 4px;
  background: #333;
  border-radius: 5px;
  padding: 2px;
  z-index: 10;
  user-select: none;

  button {
    width: 20px;
    height: 20px;
    border: none;
    background: #555;
    color: white;
    cursor: pointer;
    border-radius: 3px;
    font-weight: bold;

    &:hover {
      background: #68CEF8;
      color: #333;
    }
  }
}
</style>