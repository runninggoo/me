// src/components/Mindmap/Toolbar.vue
<script setup>
import { ref, watch } from 'vue';
import {
  Plus,
  Trash2,
  Undo2,
  Redo2,
  Download,
  Upload,
} from 'lucide-vue-next';

const props = defineProps({
  isMindMapReady: Boolean,
  addNode: Function,
  removeNode: Function,
  undo: Function,
  redo: Function,
  setTheme: Function,
  getThemeList: Function,
  setLayout: Function,
  exportJson: Function,
  importJson: Function,
});

const themeList = ref([]);
const selectedTheme = ref('default');
const selectedLayout = ref('logicalStructure');
const importInput = ref(null);

// Defines the supported layout structures
const layoutList = ref([
    { name: '逻辑结构图', value: 'logicalStructure' },
    { name: '思维导图', value: 'mindMap' },
    { name: '组织结构图', value: 'organizationStructure' },
    { name: '目录组织图', value: 'catalogOrganization' },
    { name: '时间轴', value: 'timeline' },
    { name: '鱼骨图', value: 'fishbone' },
]);

// Watch the isMindMapReady state, and get the theme list when the mindmap is ready
watch(() => props.isMindMapReady, (ready) => {
  if (ready) {
    themeList.value = props.getThemeList();
  }
});

const handleThemeChange = (event) => {
  props.setTheme(event.target.value);
};

const handleLayoutChange = (event) => {
  props.setLayout(event.target.value);
};

const triggerImport = () => {
  importInput.value.click();
};

const handleFileImport = (event) => {
  const file = event.target.files[0];
  if (file) {
    props.importJson(file);
  }
  event.target.value = ''; // Reset for re-selecting the same file
};
</script>

<template>
  <div class="editor-toolbar">
    <div class="toolbar-group">
      <button class="icon-btn" @click="addNode" title="添加子节点">
        <Plus :size="18" />
      </button>
      <button class="icon-btn" @click="removeNode" title="删除节点">
        <Trash2 :size="18" />
      </button>
      <button class="icon-btn" @click="undo" title="撤销">
        <Undo2 :size="18" />
      </button>
      <button class="icon-btn" @click="redo" title="重做">
        <Redo2 :size="18" />
      </button>

      <div class="separator"></div>

      <select class="toolbar-select" v-model="selectedLayout" @change="handleLayoutChange" title="切换结构">
        <option v-for="layout in layoutList" :key="layout.value" :value="layout.value">
          {{ layout.name }}
        </option>
      </select>
      <select class="toolbar-select" v-model="selectedTheme" @change="handleThemeChange" title="切换主题">
        <option v-for="theme in themeList" :key="theme.value" :value="theme.value">
          {{ theme.name }}
        </option>
      </select>

      <div class="separator"></div>
      
      <button class="icon-btn" @click="triggerImport" title="导入JSON">
        <Upload :size="18" />
      </button>
      <input type="file" ref="importInput" @change="handleFileImport" accept=".json" style="display: none;" />
      <button class="icon-btn" @click="exportJson" title="导出JSON">
        <Download :size="18" />
      </button>
    </div>
  </div>
</template>

<style scoped>
/* —— Toolbar Container —— */
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
  align-items: center;
  gap: 4px;
}

/* —— Icon Buttons —— */
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

.icon-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* —— Select Dropdowns —— */
.toolbar-select {
  height: 32px;
  padding: 0 8px;
  font-size: 14px;
  border: none;
  border-radius: 6px;
  background-color: transparent;
  color: #333;
  cursor: pointer;
  transition: background-color 0.2s;
}

.toolbar-select:hover {
  background-color: #f1f1f1;
}

/* —— Visual Separator —— */
.separator {
  width: 1px;
  height: 20px;
  background-color: #e0e0e0;
  margin: 0 4px;
}
</style>