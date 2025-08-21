// src/components/Mindmap/Mindmapeditor.vue
<script setup>
import { onMounted, ref, nextTick } from 'vue';
import { useMindMap } from '../../composables/useMindMap';
import Toolbar from './Toolbar.vue';
import ContextMenu from './ContextMenu.vue';

const props = defineProps({
  modelValue: { type: Object, default: null }
})
const emit = defineEmits(['update:model-value'])

const {
  mindMap,
  isMindMapReady,
  addNode,
  removeNode,
  undo,
  redo,
  init,
  setTheme,
  getThemeList,
  setLayout,
  exportJson,
  importJson,
  isContextMenuVisible,
  contextMenuPosition,
  isNodeContextMenu,
  hideContextMenu,
  copyNode,
  cutNode,
  pasteNode,
  removeCurrentNode,
  setDataJson,
  getDataJson
} = useMindMap();

const mindMapContainer = ref(null);

onMounted(() => {
  if (mindMapContainer.value) {
    init(mindMapContainer.value);
  }
  // 首次把父组件给的 JSON 写进去
  nextTick(() => props.modelValue && setDataJson(props.modelValue))

  // 监听任何改动，回传最新 JSON
  mindMap.value?.on('data_change', () => {
    emit('update:model-value', getDataJson())
  })
})
</script>

<template>
  <div class="mindmap-editor-layout" @click="hideContextMenu">
    <Toolbar
      :is-mind-map-ready="isMindMapReady"
      :add-node="addNode"
      :remove-node="removeNode"
      :undo="undo"
      :redo="redo"
      :set-theme="setTheme"
      :get-theme-list="getThemeList"
      :set-layout="setLayout"
      :export-json="exportJson"
      :import-json="importJson"
    />
    <div ref="mindMapContainer" class="mindmap-container"></div>
    <ContextMenu
      :is-visible="isContextMenuVisible"
      :position="contextMenuPosition"
      :is-node="isNodeContextMenu"
      @add="addNode"
      @copy="copyNode"
      @cut="cutNode"
      @paste="pasteNode"
      @delete="removeCurrentNode"
      @close="hideContextMenu"
    />
  </div>
</template>

<style>
.mindmap-editor-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100%;
  overflow: hidden;
}
.mindmap-container {
  flex-grow: 1; 
}
</style>