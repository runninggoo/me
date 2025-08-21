// src/components/Article/extensions.js

// --- 基础扩展 (Tiptap 运行的核心) ---
import { Document } from '@tiptap/extension-document';
import { Text } from '@tiptap/extension-text';
import { History } from '@tiptap/extension-history';
import HardBreak from '@tiptap/extension-hard-break';

// --- 核心用户体验 (UX) 扩展 ---
import { Dropcursor } from '@tiptap/extension-dropcursor';
import { Gapcursor } from '@tiptap/extension-gapcursor';

// --- 块级节点 (Block Nodes) ---
import { Paragraph } from '@tiptap/extension-paragraph';
import { Heading } from '@tiptap/extension-heading';
import { Blockquote } from '@tiptap/extension-blockquote';
import { BulletList } from '@tiptap/extension-bullet-list';
import { OrderedList } from '@tiptap/extension-ordered-list';
import { ListItem } from '@tiptap/extension-list-item';
import { CodeBlockLowlight } from '@tiptap/extension-code-block-lowlight';
import { common, createLowlight } from 'lowlight';

// --- 自定义块级节点 ---
import CustomImage from './CustomNodes/custom_image';

// --- 标记与内联节点 (Marks & Inline Nodes) ---
import { Bold } from '@tiptap/extension-bold';
import { Italic } from '@tiptap/extension-italic';
import { Underline } from '@tiptap/extension-underline';
import { Strike } from '@tiptap/extension-strike';
import { Link } from '@tiptap/extension-link';
import { Code } from '@tiptap/extension-code';
import { Color } from '@tiptap/extension-color';
import { TextStyle } from '@tiptap/extension-text-style';
import Highlight from '@tiptap/extension-highlight';
import { Subscript } from '@tiptap/extension-subscript';
import { Superscript } from '@tiptap/extension-superscript';
import Mathematics from '@tiptap/extension-mathematics';

// --- 功能性扩展 ---
import CharacterCount from '@tiptap/extension-character-count';
import Placeholder from '@tiptap/extension-placeholder';
import TextAlign from '@tiptap/extension-text-align';
import NodeRange from '@tiptap/extension-node-range';

// --- 配置 ---
const lowlight = createLowlight(common);

export const tiptapExtensions = [
  // 基础 & 核心UX
  Document,
  Text,
  History,
  HardBreak,
  Dropcursor,
  Gapcursor,
  
  // 块级节点
  Paragraph,
  Heading.configure({ levels: [1, 2, 3] }),
  Blockquote,
  BulletList,
  OrderedList,
  ListItem,
  CodeBlockLowlight.configure({ lowlight }),
  CustomImage,

  // 标记与内联节点
  Bold,
  Italic,
  Underline,
  Strike,
  Code,
  Link.configure({ openOnClick: false }),
  Highlight,
  Subscript,
  Superscript,
  Mathematics,
  TextStyle,
  Color,

  // 功能性扩展
  Placeholder.configure({ placeholder: '千里之行，始于足下...' }),
  CharacterCount,
  TextAlign.configure({ types: ['heading', 'paragraph'] }),
  NodeRange
];