// src/components/Mindmap/Nodesidebar.vue
<script setup>
import { ref, watch, computed } from 'vue';

const props = defineProps({
  activeNodes: Array,
  updateNodeData: Function,
});

// 为简单起见，我们只编辑第一个选中的节点
const activeNode = computed(() => props.activeNodes.length > 0 ? props.activeNodes[0] : null);

const nodeText = ref('');
const nodeFontSize = ref(16);
const nodeColor = ref('#000000');
const nodeBgColor = ref('#ffffff');
const nodeHyperlink = ref('');
const nodeNote = ref('');

// 一个标志位，防止 watch 循环触发
let isUpdatingInternally = false;

// 监听激活节点的变化，并更新表单内容
watch(activeNode, (newNode) => {
    if (!newNode) {
    return; 
  }
  isUpdatingInternally = true;
  if (newNode) {
    nodeText.value = newNode.data.text || '';
    nodeFontSize.value = newNode.style.fontSize.value || 16;
    nodeColor.value = newNode.style.color.value || '#000000';
    nodeBgColor.value = newNode.style.backgroundColor.value || '#ffffff';
    nodeHyperlink.value = newNode.data.hyperlink || '';
    nodeNote.value = newNode.data.note || '';
  }
  // 使用 setTimeout 确保在 DOM 更新后重置标志位
  setTimeout(() => { isUpdatingInternally = false; }, 0);
}, { deep: true, immediate: true });

// 将表单中的修改应用到思维导图节点
const applyChanges = () => {
  if (!activeNode.value || isUpdatingInternally) return;

  const newData = {
    text: nodeText.value,
    hyperlink: nodeHyperlink.value,
    note: nodeNote.value,
  };
  
  const newStyle = {
    fontSize: nodeFontSize.value,
    color: nodeColor.value,
    backgroundColor: nodeBgColor.value
  };

  // 调用从 useMindMap 传递过来的更新函数
  props.updateNodeData(activeNode.value, { data: newData, style: newStyle });
};

// 监听表单各项数据的变化，并调用应用修改的函数
watch([nodeText, nodeFontSize, nodeColor, nodeBgColor, nodeHyperlink, nodeNote], () => {
    applyChanges();
});

</script>

<template>
  <div class="sidebar">
    <div v-if="activeNode" class="sidebar-content">
      <h4>节点属性</h4>
      <div class="form-group">
        <label>文本</label>
        <textarea v-model="nodeText" rows="3"></textarea>
      </div>
      <div class="form-group">
        <label>字号</label>
        <input type="number" v-model.number="nodeFontSize" />
      </div>
      <div class="form-group">
        <label>文字颜色</label>
        <input type="color" v-model="nodeColor" />
      </div>
      <div class="form-group">
        <label>背景颜色</label>
        <input type="color" v-model="nodeBgColor" />
      </div>
       <div class="form-group">
        <label>超链接</label>
        <input type="text" v-model.trim="nodeHyperlink" placeholder="https://example.com" />
      </div>
      <div class="form-group">
        <label>备注</label>
        <textarea v-model="nodeNote" rows="5"></textarea>
      </div>
    </div>
    <div v-else class="placeholder">
      <p>请选择一个节点以编辑其属性。</p>
    </div>
  </div>
</template>

<style>
.sidebar {
  width: 280px;
  padding: 16px;
  background-color: #f8f9fa;
  border-left: 1px solid #dee2e6;
  height: 100%;
  overflow-y: auto;
  box-sizing: border-box;
}
.sidebar-content h4 {
  margin-top: 0;
  margin-bottom: 24px;
  font-size: 18px;
  color: #212529;
}
.form-group {
  margin-bottom: 16px;
}
.form-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 14px;
  font-weight: 500;
  color: #495057;
}
.form-group input[type="text"],
.form-group input[type="number"],
.form-group textarea {
  width: 100%;
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  box-sizing: border-box;
}
.form-group input[type="color"] {
  width: 100%;
  height: 38px;
  padding: 4px;
  border: 1px solid #ced4da;
  border-radius: 4px;
}
.placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #6c757d;
  text-align: center;
}
</style>