<script setup>
import { watch, onBeforeUnmount } from 'vue'
import { useEditor, EditorContent } from '@tiptap/vue-3'
// 关键：必须导入与编辑器完全相同的扩展配置
// 以确保所有自定义节点（如图片）都能被正确渲染。
// 请确保这个路径是正确的。
import { tiptapExtensions } from './extensions'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({ type: 'doc', content: [] })
  }
})

// 使用 useEditor 初始化一个 Tiptap 实例
const editor = useEditor({
  // 核心配置：将编辑器设置为不可编辑状态
  editable: false,
  // 传入与编辑器相同的扩展，这是正确渲染内容的前提
  extensions: tiptapExtensions,
  // 将 v-model 的初始值作为编辑器的内容
  content: props.modelValue,
})

// 监听 v-model 的变化
// 如果父组件传入的 JSON 数据发生改变，则更新查看器的内容
watch(
  () => props.modelValue,
  (newValue) => {
    if (editor.value && newValue) {
      // 检查内容是否真的不同，以避免不必要的更新
      const isSame = JSON.stringify(editor.value.getJSON()) === JSON.stringify(newValue);
      if (!isSame) {
        // 使用 setContent 更新查看器的内容
        editor.value.commands.setContent(newValue, false);
      }
    }
  },
  { deep: true } // 使用深度监听来检测对象内部的变化
)

// 在组件卸载前销毁 Tiptap 实例，防止内存泄漏
onBeforeUnmount(() => {
  editor.value?.destroy()
})
</script>

<template>
  <div v-if="editor" class="tiptap-viewer-layout">
    <EditorContent :editor="editor" class="ProseMirror" />
  </div>
</template>

<style lang="scss">

.tiptap-viewer-layout {
  background-color: #fafafa; 
  padding: 20px;
  height: 100%; 
  overflow-y: auto;   
  box-sizing: border-box; 
}

.ProseMirror {
  line-height: 1.7;
  font-size: 16px;
  color: #1a1a1a;
  
  margin: 0 10%;
  &:focus {
    outline: none;
  }

  p.is-editor-empty:first-child::before {
    display: none; 
  }

  blockquote {
    padding-left: 1rem;
    border-left: 3px solid #ccc; 
    margin-left: 0;
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

  img {
    max-width: 100%;
    height: auto;
  }

  .inline-image-wrapper {
    display: inline-block;
    position: relative;
    line-height: 0;
    vertical-align: middle;
  }

  .inline-image {
    border: 2px solid transparent;
    border-radius: 4px;

    &.ProseMirror-selectednode {
      border-color: transparent; 
    }
  }
}
</style>