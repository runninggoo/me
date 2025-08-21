// src/composables/useTiptapEditor.js
import { onBeforeUnmount } from 'vue'
import { useEditor } from '@tiptap/vue-3'
import { tiptapExtensions } from 'src/components/Article/extensions'

export function useTiptapEditor(initialContent = '') {
  const editor = useEditor({
    extensions: tiptapExtensions,
    content:'',
    editable: true,
  })

  onBeforeUnmount(() => {
    editor.value?.destroy()
  })

  // 重构 setLink 函数，使其支持编辑和创建
  const setLink = () => {
    if (!editor.value) return
    const currentLink = editor.value.isActive('link')
    const currentHref = editor.value.getAttributes('link').href

    const url = window.prompt('请输入 URL', currentLink ? currentHref : '')

    // 如果用户输入了 URL
    if (url) {
      editor.value.chain().focus().extendMarkRange('link').setLink({ href: url }).run()
    } else if (url === '') {
      // 如果用户清空了 URL
      editor.value.chain().focus().unsetLink().run()
    }
  }

  const insertMath = () => {
    if (!editor.value) return
    const formula = window.prompt('LaTeX 公式', 'c = \\sqrt{a^2 + b^2}')
    if (formula) {
      editor.value.chain().focus().insertInlineMath({ latex: formula }).run()
    }
  }

const triggerImageUpload = () => {
    if (!editor.value) return
    const input = document.createElement('input')
    input.type = 'file'
    input.accept = 'image/*'
    input.onchange = (e) => {
      const file = e.target.files?.[0]
      if (!file) return
      const url = URL.createObjectURL(file)
      // 调用新的命令
      editor.value.chain().focus().setInlineImage({ src: url }).run()
    }
    input.click()
  }

  return {
    editor,
    setLink,
    insertMath,
    triggerImageUpload,
  }
}