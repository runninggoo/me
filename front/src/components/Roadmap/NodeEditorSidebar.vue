<!-- src/components/Roadmap/NodeeditorSidebar.vue -->
<template>
  <aside class="editor-sidebar" v-if="modelValue && nodeType">
    <div class="sidebar-header">
      <h3 class="sidebar-title">编辑 {{ nodeType }}</h3>
    </div>

    <div class="sidebar-content">
      <div class="sidebar-section">
        <div v-for="field in fieldsToRender" :key="field.key" class="sidebar-field">
          <label :for="`node-${field.key}`">{{ field.label }}</label>

          <input v-if="field.type === 'text'" :id="`node-${field.key}`" type="text" :value="modelValue[field.key]"
            @input="emitUpdate(field.key, $event.target.value)" :placeholder="field.placeholder" />
          <textarea v-if="field.type === 'textarea'" :id="`node-${field.key}`" :value="modelValue[field.key]"
            @input="emitUpdate(field.key, $event.target.value)" :rows="field.rows || 3"></textarea>
          <select v-if="field.type === 'select'" :id="`node-${field.key}`" :value="modelValue[field.key]"
            @change="emitUpdate(field.key, $event.target.value)">
            <option v-for="opt in field.options" :key="opt.value" :value="opt.value">{{ opt.text }}</option>
          </select>
          <div v-if="field.type === 'button-group'" class="button-group">
            <button v-for="opt in field.options" :key="opt.value"
              :class="{ active: modelValue[field.key] === opt.value }" @click="emitUpdate(field.key, opt.value)">{{
              opt.text }}</button>
          </div>
          <div v-if="field.type === 'checkbox'" class="checkbox-field">
            <input :id="`node-${field.key}`" type="checkbox" :checked="modelValue[field.key]"
              @change="emitUpdate(field.key, $event.target.checked)" />
            <label :for="`node-${field.key}`">{{ field.checkboxLabel }}</label>
          </div>
        </div>
      </div>

      <div class="sidebar-section" v-if="hasField('items')">
        <h4 class="section-title">列表项</h4>
        <div class="list-item-editor">
          <div v-for="(item, index) in modelValue.items" :key="item.id" class="list-item-control">
            <input type="checkbox" :checked="item.status === 'done'" @change="toggleItemStatus(index)" />
            <input type="text" :value="item.label" @input="updateItemLabel(index, $event.target.value)"
              placeholder="输入列表项..." />
            <button @click="removeItem(index)" class="remove-item-btn" title="删除">&times;</button>
          </div>
          <button class="add-item-btn" @click="addItem">＋ 添加列表项</button>
        </div>
      </div>

      <div class="sidebar-section" v-if="hasField('color')">
        <h4 class="section-title">通用配置</h4>
        <div class="sidebar-field">
          <label>主题色</label>
          <div class="color-swatches">
            <button v-for="theme in ColorThemes" :key="theme.value" class="color-swatch"
              :class="{ 'is-active': modelValue.color === theme.value }" :style="{ '--swatch-color': theme.color }"
              @click="emitUpdate('color', theme.value)" :title="theme.text"></button>
          </div>
        </div>
      </div>

      <div class="sidebar-section" v-if="hasField('handles')">
        <h4 class="section-title">连接点配置</h4>
        <div class="handle-editor">
          <div class="handle-node-placeholder"></div>
          <div v-for="pos in ['top', 'right', 'bottom', 'left']" :key="pos"
            :class="['handle-control-group', `handle-${pos}`]">
            <button @click="cycleHandleState(pos)" :class="['handle-btn', getHandleClass(pos)]"
              :title="getHandleTooltip(pos)">{{ getHandleLabel(pos) }}</button>
          </div>
        </div>
      </div>
    </div>

    <div class="sidebar-footer">
      <button class="sidebar-close-btn" @click="$emit('close')">关闭</button>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue';
import { v4 as uuidv4 } from 'uuid';
import { NodeTypes, ColorThemes } from 'src/data/RoadmapnodeDefinitions';

const props = defineProps({ modelValue: Object, nodeType: String });
const emit = defineEmits(['update:property', 'close']);

const nodeSchema = {
  [NodeTypes.TEXT]: [
    { key: 'label', type: 'textarea', label: '文本内容', rows: 4 },
    {
      key: 'variant', type: 'select', label: '文本样式', options: [
        { value: 'title', text: '大标题 (Title)' },
        { value: 'paragraph', text: '段落 (Paragraph)' }
      ]
    },
    {
      key: 'textAlign', type: 'button-group', label: '对齐方式', options: [
        { value: 'left', text: '居左' }, { value: 'center', text: '居中' }, { value: 'right', text: '居右' }
      ]
    },
  ],
  [NodeTypes.TOPIC]: [
    { key: 'label', type: 'text', label: '标题' },
    { key: 'description', type: 'textarea', label: '内容' },
    {
      key: 'textAlign', type: 'button-group', label: '对齐方式', options: [
        { value: 'left', text: '居左' }, { value: 'center', text: '居中' }, { value: 'right', text: '居右' }
      ]
    },
    { key: 'color' }, // 标记字段存在，但由下面特殊区域渲染
    { key: 'handles' },
  ],
  [NodeTypes.TASK]: [
    { key: 'label', type: 'text', label: '按钮文字' },
    { key: 'url', type: 'text', label: '目标网址 (URL)', placeholder: 'https://...' },
    { key: 'status', type: 'button-group', label: '状态', options: [
    { value: 'todo', text: '待办' },
    { value: 'done', text: '完成' }] },
    { key: 'color' },
    { key: 'handles' },
  ],
  [NodeTypes.LIST]: [
    { key: 'label', type: 'text', label: '列表标题' },
    { key: 'items' }, // 标记存在，由特殊区域渲染
    { key: 'color' },
    { key: 'handles' },
  ],
  [NodeTypes.GROUP]: [
    { key: 'label', type: 'text', label: '分组标题' },
    { key: 'color' },
    { key: 'handles' },
  ],
};

// 2. 创建一个计算属性，它会根据 Schema 生成需要渲染的字段列表
const fieldsToRender = computed(() => {
  if (!props.nodeType) return [];
  const schema = nodeSchema[props.nodeType] || [];
  return schema
    .filter(field => field.type) // 只选择有 `type` 的字段进行通用渲染
    .filter(field => !field.condition || field.condition(props.modelValue)); // 根据条件判断是否渲染
});

// 3. 重构 hasField 逻辑以适应新的 Schema
const hasField = (fieldKey) => {
  if (!props.nodeType) return false;
  const schema = nodeSchema[props.nodeType] || [];
  return schema.some(field => field.key === fieldKey);
};

const emitUpdate = (key, value) => emit('update:property', { target: 'node', key, value });


// 列表项逻辑
const updateItems = (newItems) => emitUpdate('items', newItems);
const toggleItemStatus = (index) => {
  const newItems = [...props.modelValue.items];
  newItems[index].status = newItems[index].status === 'done' ? 'todo' : 'done';
  updateItems(newItems);
};
const updateItemLabel = (index, label) => {
  const newItems = [...props.modelValue.items];
  newItems[index].label = label;
  updateItems(newItems);
};
const removeItem = (index) => updateItems(props.modelValue.items.filter((_, i) => i !== index));
const addItem = () => updateItems([...props.modelValue.items, { id: uuidv4(), label: '新列表项', status: 'todo' }]);

// 连接点逻辑
const getHandleLabel = (pos) => (props.modelValue.handles?.[pos] === 'source' ? 'S' : props.modelValue.handles?.[pos] === 'target' ? 'T' : '○');
const getHandleClass = (pos) => (props.modelValue.handles?.[pos] === 'source' ? 'is-source' : props.modelValue.handles?.[pos] === 'target' ? 'is-target' : 'is-off');
const getHandleTooltip = (pos) => { /* ... */ };
const cycleHandleState = (pos) => {
  const currentType = props.modelValue.handles?.[pos];
  const newHandles = { ...props.modelValue.handles };
  if (currentType === 'source') newHandles[pos] = 'target';
  else if (currentType === 'target') delete newHandles[pos];
  else newHandles[pos] = 'source';
  emitUpdate('handles', newHandles);
};
</script>

<style scoped>
.editor-sidebar {
  position: fixed;
  top: 0;
  right: 0;
  height: 100vh;
  width: 340px;
  max-width: 100vw;
  box-sizing: border-box;
  background-color: #ffffff;
  border-left: 1px solid #e2e8f0;
  box-shadow: -2px 0 16px rgba(0, 0, 0, 0.05);
  z-index: 20;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar-header {
  padding: 16px 20px;
  border-bottom: 1px solid #f1f5f9;
}

.sidebar-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  text-transform: capitalize;
}

.sidebar-content {
  flex: 1 1 0;
  overflow-y: auto; 
  overflow-x: hidden;
  padding: 20px 30px;
}

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid #f1f5f9;
  background-color: #f8fafc;
}

.sidebar-close-btn {
  width: 100%;
  background-color: #475569;
  color: white;
  border: none;
  padding: 12px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}

.sidebar-section {
  border-top: 1px solid #f1f5f9;
  padding-top: 24px;
  margin-top: 24px;
}

.sidebar-section:first-child {
  border-top: none;
  padding-top: 0;
  margin-top: 0;
}

.section-title {
  font-size: 14px;
  font-weight: 600;
  color: #475569;
  margin: 0 0 16px 0;
}

.sidebar-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.sidebar-field label {
  font-weight: 500;
  font-size: 14px;
  color: #334155;
}

.sidebar-field input[type="text"],
.sidebar-field textarea,
.sidebar-field select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
}

.checkbox-field {
  display: flex;
  align-items: center;
  gap: 8px;
}

.checkbox-field label {
  font-weight: normal;
}

.button-group {
  display: flex;
}

.button-group button {
  flex-grow: 1;
  padding: 8px;
  border: 1px solid #d1d5db;
  background: #fff;
  cursor: pointer;
}

.button-group button:first-child {
  border-top-left-radius: 6px;
  border-bottom-left-radius: 6px;
}

.button-group button:last-child {
  border-top-right-radius: 6px;
  border-bottom-right-radius: 6px;
  border-left-width: 0;
}

.button-group button.active {
  background: #e0e7ff;
  color: #4338ca;
  border-color: #c7d2fe;
  z-index: 1;
}

.color-swatches {
  display: flex;
  gap: 10px;
}

.color-swatch {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 2px solid transparent;
  cursor: pointer;
  background-color: var(--swatch-color);
}

.color-swatch.is-active {
  border-color: #ffffff;
  box-shadow: 0 0 0 2px var(--swatch-color);
}

.list-item-control {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.list-item-control input[type="text"] {
  flex-grow: 1;
}

.remove-item-btn {
  border: none;
  background: #f1f5f9;
  color: #64748b;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  cursor: pointer;
}

.add-item-btn {
  margin-top: 8px;
  background: #f8fafc;
  border: 1px dashed #cbd5e1;
  padding: 8px;
  border-radius: 6px;
  text-align: center;
}

.handle-editor {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 20px auto;
}

.handle-node-placeholder {
  width: 60px;
  height: 60px;
  background-color: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  margin: auto;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.handle-control-group {
  position: absolute;
}

.handle-btn {
  border: 1px solid #d1d5db;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  font-weight: bold;
  cursor: pointer;
}

.handle-btn.is-source {
  background-color: #3b82f6;
  color: white;
}

.handle-btn.is-target {
  background-color: #10b981;
  color: white;
}

.handle-btn.is-off {
  background-color: #f8fafc;
  color: #94a3b8;
}

.handle-top {
  top: -14px;
  left: 50%;
  transform: translateX(-50%);
}

.handle-bottom {
  bottom: -14px;
  left: 50%;
  transform: translateX(-50%);
}

.handle-left {
  left: -14px;
  top: 50%;
  transform: translateY(-50%);
}

.handle-right {
  right: -14px;
  top: 50%;
  transform: translateY(-50%);
}
</style>