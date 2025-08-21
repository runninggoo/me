<template>
  <!-- 整个编辑器：Toolbar + 画布区域，占满视口，无滚动条 -->
  <div class="editor-wrapper">
    <!-- 1️⃣ 顶部固定 Toolbar -->
    <EditorToolbar
      :is-selection-active="isSelectionActive"
      :helper-lines-active="showHelperLines"
      @delete="deleteSelection"
      @toggle-helper-lines="toggleHelperLines"
      @open-json-modal="openJsonModal"
      @add="addNode" 
    />

    <!-- 2️⃣ 画布区域：占剩余全部高度 -->
    <div class="editor-body">
      <VueFlow
        v-model="elements"
        :is-valid-connection="isValidConnection"
        :expand-parent="true"
        :select-nodes-on-drag="false"
        @connect="onConnect"
        @node-click="onNodeClick"
        @edge-click="onEdgeClick"
        @pane-click="onPaneClick"
        @node-context-menu="onNodeContextMenu"
        @pane-context-menu="onPaneContextMenu"
      >
        <!-- 节点模板 -->
        <template #node-text="props"><TextNode v-bind="props" /></template>
        <template #node-topic="props"><TopicNode v-bind="props" /></template>
        <template #node-task="props">
          <TaskNode
            v-bind="props"
            @updateNodeData="d => onElementPropertyUpdate({ target:'node', key:null, value:d })"
          />
        </template>
        <template #node-list="props">
          <ListNode
            v-bind="props"
            @updateNodeData="d => onElementPropertyUpdate({ target:'node', key:null, value:d })"
          />
        </template>
        <template #node-group="props">
          <GroupNode v-bind="props" @resize="onNodeResize" />
        </template>

        <!-- 背景、控制器、小地图 -->
        <Background bg-color="#fafafa" />
        <Controls />
        <MiniMap
          :node-color="getNodeColor"
          node-stroke-color="#4b5563"
          :node-border-radius="4"
        />
      </VueFlow>

      <!-- 辅助线（仅当开启时渲染） -->
      <HelperLines v-if="showHelperLines" />

      <!-- 右键菜单（绝对定位，不影响滚动） -->
      <ContextMenu
        :visible="contextMenu.visible"
        :position="contextMenu.position"
        @select-option="handleContextMenuAction"
      />
    </div>

    <!-- 3️⃣ 浮层/侧边栏：绝对定位，不占流 -->
    <NodeEditorSidebar
      v-if="selectedNode"
      :model-value="selectedNode.data"
      :node-type="selectedNode.type"
      @update:property="onElementPropertyUpdate"
      @close="deselectAll"
    />
    <EdgeEditorSidebar
      v-if="selectedEdge"
      :model-value="selectedEdge"
      @update:property="onElementPropertyUpdate"
      @close="deselectAll"
    />
    <JsonEditorModal
      v-model="isJsonModalOpen"
      :json-data="jsonModalData"
      :mode="jsonModalMode"
      @import="importFromJson"
    />
    <TransferOwnershipModal
      v-if="isTransferModalOpen"
      v-model="isTransferModalOpen"
      :nodes-tree="groupedNodesTree"
      @confirm="handleTransferOwnership"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { VueFlow } from '@vue-flow/core'
import { Background} from '@vue-flow/background'
import { Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'
import '@vue-flow/minimap/dist/style.css'
import '@vue-flow/core/dist/style.css'
import '@vue-flow/controls/dist/style.css'

import EditorToolbar from './EditorToolbar.vue'
import NodeEditorSidebar from './NodeEditorSidebar.vue'
import EdgeEditorSidebar from './EdgeEditorSidebar.vue'
import JsonEditorModal from './JsonEditorModal.vue'
import HelperLines from './HelperLines.vue'
import TextNode from './TextNode.vue'
import TopicNode from './TopicNode.vue'
import TaskNode from './TaskNode.vue'
import ListNode from './ListNode.vue'
import GroupNode from './GroupNode.vue'
import ContextMenu from './ContextMenu.vue'
import TransferOwnershipModal from './TransferOwnershipModal.vue'

import { useRoadmap } from 'src/composables/useRoadmap'
import { ColorThemes } from 'src/data/RoadmapnodeDefinitions'

const props = defineProps({modelValue: { type: Array, default: () => [] }})
const emit  = defineEmits(['update:modelValue'])

const elements = computed({
  get: () => props.modelValue,
  set: v => emit('update:modelValue', v),
})

const {
  selectedNode,
  selectedEdge,
  isSelectionActive,
  isJsonModalOpen,
  jsonModalData,
  jsonModalMode,
  onPaneClick,
  onNodeClick,
  onEdgeClick,
  onConnect,
  isValidConnection,
  onElementPropertyUpdate,
  addNode,
  deleteSelection,
  deselectAll,
  openJsonModal,
  importFromJson,
  contextMenu,
  onNodeContextMenu,
  onPaneContextMenu,
  closeContextMenu,
  handleContextMenuAction,
  isTransferModalOpen,
  groupedNodesTree,
  handleTransferOwnership,
} = useRoadmap(elements)

const showHelperLines = ref(true)
const toggleHelperLines = () => {
  showHelperLines.value = !showHelperLines.value
}

const getNodeColor = node => {
  if (node.type === 'group') return 'rgba(100, 116, 139, 0.2)'
  const themeKey = node.data.color?.toUpperCase()
  return ColorThemes[themeKey]?.color || ColorThemes.GRAY.color
}

/* 节点 resize 回调 */
function onNodeResize({ id, width, height }) {
  elements.value = elements.value.map(el =>
    el.id === id ? { ...el, width, height } : el
  )
}
</script>

<style scoped>
.editor-wrapper {
  display: flex;
  flex-direction: column;
  height: 100vh;     
  overflow: hidden;   
}

.editor-body {
  position: relative;
  flex: 1 1 0;
  min-height: 0;   
}

.editor-body :deep(.vue-flow) {
  width: 100%;
  height: 100%;
}
</style>