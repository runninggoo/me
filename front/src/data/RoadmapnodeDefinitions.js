import { v4 as uuidv4 } from 'uuid';

// 节点类型定义保持不变
export const NodeTypes = {
  TEXT: 'text', // 为文本节点添加一个明确的类型
  TOPIC: 'topic',
  TASK: 'task',
  LIST: 'list',
  GROUP: 'group',
};

// 颜色主题保持不变
export const ColorThemes = {
  BLUE: { value: 'blue', text: '科技蓝', color: '#3b82f6', bg: '#eff6ff' },
  GREEN: { value: 'green', text: '增长绿', color: '#10b981', bg: '#f0fdf4' },
  YELLOW: { value: 'yellow', text: '活力黄', color: '#f59e0b', bg: '#fefce8' },
  PURPLE: { value: 'purple', text: '优雅紫', color: '#8b5cf6', bg: '#f5f3ff' },
  GRAY: { value: 'gray', text: '中性灰', color: '#6b7280', bg: '#f8fafc' },
};

export function createNodeData(type, overrides = {}) {
  // 通用基础数据
  const baseData = {
    label: '新节点',
    color: ColorThemes.GRAY.value,
    handles: {}, // 连接点由用户在侧边栏手动配置
  };

  switch (type) {
    case NodeTypes.TEXT:
      return { label: '文本', variant: 'title', width: 200, textAlign: 'left', ...overrides };
    
    case NodeTypes.TOPIC:
      return { ...baseData, label: '新话题', description: '这是一个核心话题...', color: ColorThemes.BLUE.value, textAlign: 'left', hasStatus: true, status: 'inprogress', ...overrides };

    case NodeTypes.TASK:
      return { ...baseData, label: '新任务', url: '', color: ColorThemes.GREEN.value, hasStatus: true, status: 'todo', ...overrides };

    case NodeTypes.LIST:
      return { ...baseData, label: '列表', color: ColorThemes.PURPLE.value, items: [{ id: uuidv4(), label: '列表项 1', status: 'todo' }], ...overrides };
      
    case NodeTypes.GROUP:
      return { ...baseData, label: '新分组', ...overrides };

    default:
      return { ...baseData, ...overrides };
  }
}