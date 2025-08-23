<template>
  <div class="viewer-wrapper" tabindex="0" @keydown="onKeyDown">
    <VueFlow
      :model-value="modelValue"
      :nodes-draggable="false"
      :nodes-connectable="false"
      :elements-selectable="true"
      :select-nodes-on-drag="false"
      @node-click="onNodeClick"
      @edge-click="onEdgeClick"
      @pane-click="onPaneClick"
    >
      <template #node-text="props"><TextNode v-bind="props" /></template>
      <template #node-topic="props"><TopicNode v-bind="props" /></template>
      <template #node-task="props">
        <TaskNode v-bind="props" @updateNodeData="patch => applyPatch(props.id, patch)" />
      </template>
      <template #node-list="props">
        <ListNode v-bind="props" @updateNodeData="patch => applyPatch(props.id, patch)" />
      </template>
      <template #node-group="props"><GroupNode v-bind="props" /></template>

      <Background bg-color="#fafafa" />
    </VueFlow>

    <TaskDetailSidebar
      v-if="isTaskSidebarOpen"
      :node="selectedNode"
      @close="deselectAll"
    />
  </div>
</template>

<script setup>
import { VueFlow } from '@vue-flow/core';
import { Background} from '@vue-flow/background'
import '@vue-flow/core/dist/style.css';

import TextNode from './TextNode.vue';
import TopicNode from './TopicNode.vue';
import TaskNode from './TaskNode.vue';
import ListNode from './ListNode.vue';
import GroupNode from './GroupNode.vue';
import TaskDetailSidebar from './TaskDetailSidebar.vue';

import { useRoadmapViewer } from 'src/composables/useRoadmapViewer';

const props = defineProps({ modelValue: Array });

function applyPatch(nodeId, patch) {
  const node = props.modelValue.find(el => el.id === nodeId);
  if (node) Object.assign(node.data, patch);
}

const {
  selectedNode,
  isTaskSidebarOpen,
  deselectAll,
  onNodeClick,
  onEdgeClick,
  onPaneClick,
  onKeyDown,
} = useRoadmapViewer(props.modelValue);
</script>

<style scoped>
.viewer-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
  outline: none;
}
</style>