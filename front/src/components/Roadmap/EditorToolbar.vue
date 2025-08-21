<template>
  <div class="editor-toolbar">
    <!-- 整行 flex 居中 -->
    <div class="toolbar-group">
      <button ref="addBtn" class="icon-btn" @click="togglePicker" aria-label="添加节点">
        <Plus :size="18" />
      </button>
      <button
        class="icon-btn"
        :class="{ active: helperLinesActive }"
        @click="$emit('toggle-helper-lines')"
        aria-label="辅助线"
      >
        <LayoutGrid :size="18" />
      </button>
      <button
        class="icon-btn"
        :disabled="!isSelectionActive"
        @click="$emit('delete')"
        aria-label="删除选中"
      >
        <Trash2 :size="18" />
      </button>
      <button class="icon-btn" @click="$emit('open-json-modal', 'export')" aria-label="导出">
        <Download :size="18" />
      </button>
      <button class="icon-btn" @click="$emit('open-json-modal', 'import')" aria-label="导入">
        <Upload :size="18" />
      </button>
    </div>

    <!-- 弹层：位置动态计算 -->
    <Teleport to="body">
      <div
        v-if="pickerOpen"
        class="picker-popover"
        :style="pickerStyle"
      >
        <button
          v-for="t in types"
          :key="t.value"
          class="picker-item"
          @click="selectAndClose(t.value)"
        >
          <span :class="'icon icon-' + t.value">{{ t.icon }}</span>
          <span>{{ t.label }}</span>
        </button>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { Plus, Download, Upload, LayoutGrid, Trash2 } from 'lucide-vue-next'
import { NodeTypes } from 'src/data/RoadmapnodeDefinitions'

defineProps({
  isSelectionActive: Boolean,
  helperLinesActive: Boolean,
})
const emit = defineEmits(['add', 'delete', 'toggle-helper-lines', 'open-json-modal'])

/* 类型列表 */
const types = [
  { value: NodeTypes.TOPIC, label: '话题', icon: 'T' },
  { value: NodeTypes.TASK,  label: '任务', icon: '✓' },
  { value: NodeTypes.LIST,  label: '列表', icon: 'L' },
  { value: NodeTypes.GROUP, label: '分组', icon: 'G' },
  { value: NodeTypes.TEXT,  label: '文本', icon: 'A' },
]

const addBtn      = ref()
const pickerOpen  = ref(false)
const pickerStyle = ref({})

function togglePicker() {
  pickerOpen.value = !pickerOpen.value
  if (pickerOpen.value) {
    nextTick(() => {
      const rect = addBtn.value.getBoundingClientRect()
      pickerStyle.value = {
        position: 'absolute',
        top: `${rect.bottom + 4}px`,
        left: `${rect.left}px`,
        zIndex: 1000,
      }
    })
    const close = e => {
      if (!addBtn.value.contains(e.target) && !e.target.closest('.picker-popover')) {
        pickerOpen.value = false
        document.removeEventListener('click', close)
      }
    }
    document.addEventListener('click', close)
  }
}

function selectAndClose(type) {
  emit('add', type)
  pickerOpen.value = false
}
</script>

<style scoped>
/* —— 整行居中 —— */
.editor-toolbar {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #e0e0e0;
  background-color: #ffffff;
}

.toolbar-group {
  display: flex;
  gap: 4px;
}

/* —— 无边框图标按钮 —— */
.icon-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  color: #333;
  cursor: pointer;
  border-radius: 6px;
  transition: background-color 0.2s, color 0.2s;
}
.icon-btn:hover {
  background-color: #f1f1f1;
}
.icon-btn.active {
  background-color: #000;
  color: #fff;
}
.icon-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* —— 弹层样式不变 —— */
.picker-popover {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 4px 0;
  min-width: 120px;
}
.picker-item {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 6px 12px;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 14px;
  color: #334155;
}
.picker-item:hover {
  background: #f1f5f9;
}
.icon {
  width: 20px;
  height: 20px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
  color: #fff;
}
.icon.topic { background: #3b82f6; }
.icon.task  { background: #10b981; }
.icon.list  { background: #8b5cf6; }
.icon.group { background: #6b7280; }
.icon.text  { background: #f59e0b; }
</style>