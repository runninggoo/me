// src/components/Article/TipTapEditor.vue
<script setup>
import { watch,nextTick } from 'vue'
import { EditorContent } from '@tiptap/vue-3'
import { useTiptapEditor } from '../../composables/useTiptapEditor'
import Toolbar from './Toolbar.vue'
import StructureSidebar from './StructureSidebar.vue'

const { editor, setLink, insertMath, triggerImageUpload } = useTiptapEditor()

const props = defineProps({
  modelValue: { type: [Object, Array], default: () => ({ type: 'doc', content: [] }) }
})
const emit = defineEmits(['update:modelValue'])

watch(
  () => editor.value,
  (ed) => {
    if (!ed) return
    nextTick(() => ed.commands.setContent(props.modelValue, false))
    ed.on('update', () => emit('update:modelValue', ed.getJSON()))
  },
  { immediate: true }
)

const exportContent = () => {
  if (!editor.value) return;
  try {
    const jsonContent = editor.value.getJSON();
    const jsonString = JSON.stringify(jsonContent, null, 2);
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'editor-content.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  } catch (error) {
    console.error("Failed to export content:", error);
  }
};

const importContent = () => {
  if (!editor.value) return;
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = '.json';
  input.onchange = (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const json = JSON.parse(e.target.result);
        editor.value.commands.setContent(json, true);
      } catch (error) {
        console.error("Failed to parse JSON file:", error);
        alert("Error: The selected file is not valid JSON.");
      }
    };
    reader.readAsText(file);
  };
  input.click();
};
</script>

<template>
  <div v-if="editor" class="full-width-editor-layout">
    <Toolbar
      :editor="editor"
      :set-link="setLink"
      :insert-math="insertMath"
      :trigger-image-upload="triggerImageUpload"
      :import-content="importContent"
      :export-content="exportContent"
    />

    <div class="editor-content-wrapper" ref="editorContentRef">
      <EditorContent :editor="editor" class="editor-content" />

      <StructureSidebar :editor="editor" />

      <div v-if="editor?.storage.characterCount" class="status-bar">
        {{ editor.storage.characterCount.characters() }} 字符
      </div>
    </div>
  </div>
</template>

<style lang="scss">
::selection {
  background-color: #70cff850;
}

.full-width-editor-layout {
  background-color: #fafafa; 
  width: 100%;
  height: 100%;
}

.editor-content-wrapper {
  max-width: 900px;
  margin: 40px auto;
  position: relative;
}

.editor-content {
  flex-grow: 1;
}

.ProseMirror {
  min-height: 200px;
  line-height: 1.7;
  font-size: 16px;
  color: #1a1a1a;
}

.ProseMirror:focus {
  outline: none;
}


/* 为单击选中和范围选中提供统一的视觉效果 */
.ProseMirror-selectednode,
.ProseMirror-selectednoderange {
  outline: 3px solid #68CEF8;
  border-radius: 4px;
}

/* Dropcursor 的样式，用于拖拽时显示插入位置 */
.ProseMirror-gapcursor {
  display: none;
  pointer-events: none;
  position: absolute;
}
.ProseMirror-gapcursor:after {
  content: "";
  display: block;
  position: absolute;
  top: -2px;
  width: 20px;
  height: 2px;
  border-top: 1px solid black;
  animation: ProseMirror-cursor-blink 1.1s steps(2, start) infinite;
}
@keyframes ProseMirror-cursor-blink {
  to {
    visibility: hidden;
  }
}
.ProseMirror-focused .ProseMirror-gapcursor {
  display: block;
}


.structure-sidebar {
  position: absolute;
  top: 0;
  right: -5rem;
  width: 4rem;
  height: 100%;
  pointer-events: none;
}

.sidebar-label {
  position: absolute;
  width: 100%;
  display: flex;
  align-items: flex-start;
  justify-content: center;

  span {
    color: #adb5bd;
    font-size: 0.75rem;
    font-family: monospace;
    padding-top: 0.4em;
  }
}

.ProseMirror {
  p.is-editor-empty:first-child::before {
    content: attr(data-placeholder);
    float: left;
    color: #adb5bd;
    pointer-events: none;
    height: 0;
  }

  blockquote {
    padding-left: 1rem;
    border-left: 3px solid #333;
  }

  pre {
    background: #f1f3f5;
    border-radius: 8px;
    padding: 1rem;
    font-family: 'JetBrains Mono', monospace;
    color: #343a40;

    code {
      background: none;
      color: inherit;
      font-size: 0.9rem;
      padding: 0;
    }
  }
}

.status-bar {
  padding: 4px 12px;
  font-size: 12px;
  color: #666;
  text-align: right;
}
</style>