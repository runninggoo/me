// src/components/Article/Toolbar.vue
<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue';
import tippy from 'tippy.js';
import {
  AlignCenter, AlignLeft, AlignRight, Bold, Code, Eraser, Highlighter, Italic, Link, List,
  ListOrdered, MessageSquareQuote, Palette, Redo, Sigma, Subscript, Superscript, Underline, Undo,
  Image as ImageIcon,
  Download, Upload,
  Strikethrough
} from 'lucide-vue-next';

const props = defineProps({
  editor: { type: Object, required: true },
  setLink: { type: Function, required: true },
  insertMath: { type: Function, required: true },
  triggerImageUpload: { type: Function, required: true },
  importContent: { type: Function, required: true },
  exportContent: { type: Function, required: true },
});

const tippyInstances = ref([]);

const currentBlockType = computed(() => {
  if (props.editor.isActive('heading', { level: 1 })) return 'h1';
  if (props.editor.isActive('heading', { level: 2 })) return 'h2';
  if (props.editor.isActive('heading', { level: 3 })) return 'h3';
  return 'p';
});

function handleHeadingChange(e) {
  const val = e.target.value;
  val === 'p'
    ? props.editor.chain().focus().setParagraph().run()
    : props.editor.chain().focus().setHeading({ level: +val.slice(1) }).run();
}

// 按钮提示文本映射
const tooltipTexts = {
  undo: '撤销',
  redo: '重做',
  bold: '粗体',
  italic: '斜体',
  underline: '下划线',
  strike: '删除线', 
  code: '行内代码', 
  link: '链接',
  subscript: '下标',
  superscript: '上标',
  alignLeft: '左对齐',
  alignCenter: '居中对齐',
  alignRight: '右对齐',
  bulletList: '无序列表',
  orderedList: '有序列表',
  blockquote: '引用',
  codeBlock: '代码块',
  highlight: '高亮',
  color: '文字颜色',
  clearFormatting: '清除格式',
  image: '插入图片',
  math: '插入公式',
  import: '导入 JSON',
  export: '导出 JSON',
};

onMounted(() => {
  const buttons = document.querySelectorAll('.toolbar button[data-tippy-content]');
  buttons.forEach(button => {
    const instance = tippy(button, {
      placement: 'top',
      theme: 'light-border',
    });
    tippyInstances.value.push(instance);
  });

  const colorPickerIcon = document.querySelector('.color-picker-wrapper .lucide-palette');
  if (colorPickerIcon) {
    const colorInstance = tippy(colorPickerIcon, {
      content: tooltipTexts.color,
      placement: 'top',
      theme: 'light-border',
    });
    tippyInstances.value.push(colorInstance);
  }
});

onUnmounted(() => {
  tippyInstances.value.forEach(instance => instance.destroy());
  tippyInstances.value = [];
});
</script>

<template>
  <div class="toolbar">
    <div class="toolbar-group">
      <button @click="editor.chain().focus().undo().run()" :disabled="!editor.can().chain().undo().run()"
        :data-tippy-content="tooltipTexts.undo">
        <Undo :size="18" />
      </button>
      <button @click="editor.chain().focus().redo().run()" :disabled="!editor.can().chain().redo().run()"
        :data-tippy-content="tooltipTexts.redo">
        <Redo :size="18" />
      </button>
    </div>
    <div class="toolbar-group">
      <select class="block-type-select" :value="currentBlockType" @change="handleHeadingChange">
        <option value="p">段落</option>
        <option value="h1">标题 1</option>
        <option value="h2">标题 2</option>
        <option value="h3">标题 3</option>
      </select>
    </div>
    <div class="toolbar-group">
      <button @click="editor.chain().focus().toggleBold().run()" :class="{ 'is-active': editor.isActive('bold') }"
        :data-tippy-content="tooltipTexts.bold">
        <Bold :size="18" />
      </button>
      <button @click="editor.chain().focus().toggleItalic().run()" :class="{ 'is-active': editor.isActive('italic') }"
        :data-tippy-content="tooltipTexts.italic">
        <Italic :size="18" />
      </button>
      <button @click="editor.chain().focus().toggleUnderline().run()"
        :class="{ 'is-active': editor.isActive('underline') }" :data-tippy-content="tooltipTexts.underline">
        <Underline :size="18" />
      </button>
      <button @click="editor.chain().focus().toggleStrike().run()" :class="{ 'is-active': editor.isActive('strike') }"
        :data-tippy-content="tooltipTexts.strike">
        <Strikethrough :size="18" />
      </button>
      <button @click="editor.chain().focus().toggleCode().run()" :class="{ 'is-active': editor.isActive('code') }"
        :data-tippy-content="tooltipTexts.code">
        <Code :size="18" />
      </button>
      <button @click="setLink" :class="{ 'is-active': editor.isActive('link') }"
        :data-tippy-content="tooltipTexts.link">
        <Link :size="18" />
      </button>
      <button @click="editor.chain().focus().toggleSubscript().run()"
        :class="{ 'is-active': editor.isActive('subscript') }" :data-tippy-content="tooltipTexts.subscript">
        <Subscript :size="18" />
      </button>
      <button @click="editor.chain().focus().toggleSuperscript().run()"
        :class="{ 'is-active': editor.isActive('superscript') }" :data-tippy-content="tooltipTexts.superscript">
        <Superscript :size="18" />
      </button>
    </div>
    <div class="toolbar-group">
      <button @click="editor.chain().focus().setTextAlign('left').run()"
        :class="{ 'is-active': editor.isActive({ textAlign: 'left' }) }" :data-tippy-content="tooltipTexts.alignLeft">
        <AlignLeft :size="18" />
      </button>
      <button @click="editor.chain().focus().setTextAlign('center').run()"
        :class="{ 'is-active': editor.isActive({ textAlign: 'center' }) }"
        :data-tippy-content="tooltipTexts.alignCenter">
        <AlignCenter :size="18" />
      </button>
      <button @click="editor.chain().focus().setTextAlign('right').run()"
        :class="{ 'is-active': editor.isActive({ textAlign: 'right' }) }" :data-tippy-content="tooltipTexts.alignRight">
        <AlignRight :size="18" />
      </button>
    </div>
    <div class="toolbar-group">
      <button @click="editor.chain().focus().toggleBulletList().run()"
        :class="{ 'is-active': editor.isActive('bulletList') }" :data-tippy-content="tooltipTexts.bulletList">
        <List :size="18" />
      </button>
      <button @click="editor.chain().focus().toggleOrderedList().run()"
        :class="{ 'is-active': editor.isActive('orderedList') }" :data-tippy-content="tooltipTexts.orderedList">
        <ListOrdered :size="18" />
      </button>
      <button @click="editor.chain().focus().toggleBlockquote().run()"
        :class="{ 'is-active': editor.isActive('blockquote') }" :data-tippy-content="tooltipTexts.blockquote">
        <MessageSquareQuote :size="18" />
      </button>
      <button @click="editor.chain().focus().toggleCodeBlock().run()"
        :class="{ 'is-active': editor.isActive('codeBlock') }" :data-tippy-content="tooltipTexts.codeBlock">
        <Code :size="18" />
      </button>
    </div>
    <div class="toolbar-group">
      <button @click="editor.chain().focus().toggleHighlight().run()"
        :class="{ 'is-active': editor.isActive('highlight') }" :data-tippy-content="tooltipTexts.highlight">
        <Highlighter :size="18" />
      </button>
      <div class="color-picker-wrapper">
        <Palette :size="18" :color="editor.getAttributes('textStyle').color || '#000000'" />
        <button class="button" :data-tippy-content="tooltipTexts.color" @click="$refs.colorInput.click()">
          <Palette :size="18" :color="editor.getAttributes('textStyle').color || '#000000'" />
        </button>
        <input ref="colorInput" type="color" :value="editor.getAttributes('textStyle').color || '#000000'"
          @input="editor.chain().focus().setColor($event.target.value).run()"
          style="position: absolute; opacity: 0; width: 0; height: 0;" />
      </div>
      <button @click="editor.chain().focus().unsetAllMarks().run()" :data-tippy-content="tooltipTexts.clearFormatting">
        <Eraser :size="18" />
      </button>
    </div>
    <div class="toolbar-group">
      <button @click="triggerImageUpload" :data-tippy-content="tooltipTexts.image">
        <ImageIcon :size="18" />
      </button>
      <button @click="insertMath" :data-tippy-content="tooltipTexts.math">
        <Sigma :size="18" />
      </button>
    </div>
    <div class="toolbar-group">
      <button @click="importContent" :data-tippy-content="tooltipTexts.import">
        <Upload :size="18" />
      </button>
      <button @click="exportContent" :data-tippy-content="tooltipTexts.export">
        <Download :size="18" />
      </button>
    </div>
  </div>
</template>

<style scoped>
.toolbar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px;
  padding: 8px 12px;
  border-bottom: 1px solid #e0e0e0;
  justify-content: center;
  background-color: #ffffff;
}

.toolbar-group {
  display: flex;
  gap: 2px;
  align-items: center;
}

.toolbar button,
.block-type-select {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  color: #333;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.toolbar button:hover,
.block-type-select:hover {
  background-color: #f1f1f1;
}

.toolbar button.is-active {
  background-color: #000;
  color: #fff;
}

.toolbar button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.block-type-select {
  width: auto;
  padding: 0 8px;
  font-size: 14px;
}

.color-picker-wrapper {
  position: relative;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 6px;
  transition: background-color 0.2s ease;
}

.color-picker-wrapper:hover {
  background-color: #f1f1f1;
}

.color-input {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}
</style>
