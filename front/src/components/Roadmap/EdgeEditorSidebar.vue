<template>
  <aside class="editor-sidebar" v-if="modelValue">
    <div class="sidebar-header">
      <h3 class="sidebar-title">编辑连线</h3>
    </div>

    <div class="sidebar-content">
      <div class="sidebar-section">
        <div class="sidebar-field">
          <label for="edge-label">标签</label>
          <input id="edge-label" type="text" :value="modelValue.label" @input="emitUpdate('label', $event.target.value)"
            placeholder="输入标签..." />
        </div>

        <div class="sidebar-field">
          <label for="edge-path-type">路径类型</label>
          <select id="edge-path-type" :value="modelValue.type || 'default'"
            @change="emitUpdate('type', $event.target.value === 'default' ? undefined : $event.target.value)">
            <option value="default">曲线 (Default)</option>
            <option value="smoothstep">步进线 (SmoothStep)</option>
            <option value="straight">直线 (Straight)</option>
          </select>
        </div>

        <div class="sidebar-field">
          <label>选项</label>
          <div class="checkbox-field">
            <input id="edge-animated" type="checkbox" :checked="modelValue.animated"
              @change="emitUpdate('animated', $event.target.checked)" />
            <label for="edge-animated">启用流动动画</label>
          </div>
          <div class="checkbox-field">
            <input id="edge-arrow" type="checkbox" v-model="hasArrow" />
            <label for="edge-arrow">显示箭头</label>
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
import { computed } from 'vue'

const props = defineProps({ modelValue: Object });
const emit = defineEmits(['update:property', 'close']);

const emitUpdate = (key, value) => emit('update:property', { target: 'edge', key, value });

const hasArrow = computed({
  get: () => !!props.modelValue?.markerEnd,
  set: (value) => emitUpdate('markerEnd', value ? 'arrowclosed' : undefined),
});
</script>

<style scoped>
.editor-sidebar {
  position: fixed;
  /* 关键：相对视口固定，不随画布滚动 */
  top: 0;
  right: 0;
  height: 100vh;
  /* 占满视口高度 */
  width: 340px;
  max-width: 100vw;
  /* 关键：永远不超过视口宽度 */
  box-sizing: border-box;
  /* padding/border 不再额外占宽 */
  background-color: #ffffff;
  border-left: 1px solid #e2e8f0;
  box-shadow: -2px 0 16px rgba(0, 0, 0, 0.05);
  z-index: 20;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  /* 整体不滚动 */
}

.sidebar-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.sidebar-content {
  flex: 1 1 0;
  overflow-y: auto;
  /* 仅纵向滚动 */
  overflow-x: hidden;
  /* 强制去掉横向滚动条 */
  padding: 20px 5px;
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

.sidebar-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

.sidebar-field label {
  font-weight: 500;
  font-size: 14px;
  color: #334155;
}

.sidebar-field input[type="text"],
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
  margin-top: 8px;
}

.checkbox-field label {
  font-weight: normal;
  font-size: 14px;
}

.checkbox-field input[type="checkbox"] {
  width: 16px;
  height: 16px;
  accent-color: #3b82f6;
  cursor: pointer;
}
</style>