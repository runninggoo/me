<!-- src/components/Mindmap/MindMapViewer.vue -->
<script setup>
import { onMounted, ref, watch } from 'vue'
import MindMap from 'simple-mind-map'

/* —— 插件 —— */
import MiniMap   from 'simple-mind-map/src/plugins/MiniMap.js'
import Drag      from 'simple-mind-map/src/plugins/Drag.js'
MindMap.usePlugin(Drag).usePlugin(MiniMap)

/* —— 主题包 —— */
import Themes from 'simple-mind-map-plugin-themes'
Themes.init(MindMap)      // 注册主题，跟 Editor 保持一致

const props    = defineProps({ modelValue: { type: Object, default: null } })
const emit     = defineEmits(['update:model-value'])
const container = ref(null)
let mindMapInst = null

/* 统一的「数据/主题/布局」注入函数 */
const setUpMindMap = (containerEl, initialData) => {
  // 1. 准备节点数据
  let nodeData = { data: { text: '根节点' }, children: [] }
  if (initialData) {
    nodeData = initialData.root ? initialData.root : initialData
  }

  // 2. 实例化
  mindMapInst = new MindMap({
    el: containerEl,
    data: nodeData,
    readonly: true,        // 只读
    defaultTheme: 'default'
  })

  // 3. 应用布局 / 主题（如果外部提供了）
  if (initialData?.layout) {
    mindMapInst.setLayout(initialData.layout)
  }
  if (initialData?.theme?.template) {
    mindMapInst.setTheme(initialData.theme.template)
  }
}

/* 首次挂载 */
onMounted(() => {
  setUpMindMap(container.value, props.modelValue)
})

/* 外部数据变化时重新渲染（热切换主题/布局也走这里） */
watch(
  () => props.modelValue,
  (newVal) => {
    if (newVal && mindMapInst) {
      // 重新注入完整数据（含主题/布局）
      setUpMindMap(container.value, newVal)
    }
  },
  { deep: true }
)
</script>

<template>
  <div ref="container" class="mindmap-viewer"></div>
</template>

<style scoped>
.mindmap-viewer {
  width: 100%;
  height: 100%;
  overflow: hidden;
}
</style>