import { Node, mergeAttributes } from '@tiptap/core';
import { VueNodeViewRenderer } from '@tiptap/vue-3';
import InlineImageView from './ImageView.vue'; 

export default Node.create({
  name: 'inlineImage', // 命名为 inlineImage 以示区别
  group: 'inline',
  inline: true,
  atom: true,
  draggable: true, // 内联节点需要是可拖拽的，才能在文本中移动

  addAttributes() {
    return {
      src: {
        default: null,
      },
      alt: {
        default: null,
      },
      title: {
        default: null,
      },
      // 使用 width 属性来控制大小
      width: {
        default: '80px', // 给一个默认的初始尺寸
        parseHTML: element => element.style.width || '80px',
        renderHTML: attributes => {
          return {
            style: `width: ${attributes.width}`,
          };
        },
      },
    };
  },

  parseHTML() {
    return [
      {
        tag: 'img[src][data-inline-image]', // 只有带特定标记的 img 才被解析
      },
    ];
  },

  renderHTML({ HTMLAttributes }) {
    return ['img', mergeAttributes(HTMLAttributes, { 'data-inline-image': '' })];
  },

  addNodeView() {
    return VueNodeViewRenderer(InlineImageView);
  },

  addCommands() {
    return {
      setInlineImage: options => ({ commands }) => {
        return commands.insertContent({
          type: this.name,
          attrs: options,
        });
      },
    };
  },
});