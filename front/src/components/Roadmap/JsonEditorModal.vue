// JsonEditorModal.vue

<template>
  <div v-if="modelValue" class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <h3 class="modal-title">{{ isImportMode ? '导入数据' : '导出数据' }}</h3>
      
      <div class="modal-body">
        <p v-if="isImportMode" class="modal-description">
          请将有效的 JSON 数据粘贴到下方文本框中，然后点击“导入”按钮。这将替换当前画布上的所有内容。
        </p>
        <p v-else class="modal-description">
          这是当前画布内容的 JSON 表示。您可以复制并保存它，以便将来导入。
        </p>
        
        <textarea
          v-model="editableJson"
          :readonly="!isImportMode"
          class="json-textarea"
          :class="{ 'is-error': hasError }"
          placeholder="请在此处粘贴 JSON 数据..."
        ></textarea>
        <p v-if="hasError" class="error-message">JSON 格式无效，请检查后重试。</p>
      </div>
      
      <div class="modal-actions">
        <button class="btn btn-secondary" @click="close">关闭</button>
        <button v-if="isImportMode" class="btn btn-primary" @click="handleImport">导入</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

const props = defineProps({
  modelValue: Boolean,      // 控制模态框显示/隐藏 (v-model)
  jsonData: String,       // 传入的 JSON 字符串
  mode: {                 // 'import' 或 'export'
    type: String,
    default: 'export',
  },
});

const emit = defineEmits(['update:modelValue', 'import']);

const editableJson = ref('');
const hasError = ref(false);

const isImportMode = computed(() => props.mode === 'import');

// 当传入的 jsonData 变化时，更新文本框内容
watch(() => props.jsonData, (newVal) => {
  editableJson.value = newVal;
  hasError.value = false; // 重置错误状态
});

const close = () => {
  emit('update:modelValue', false);
};

const handleImport = () => {
  try {
    // 尝试解析 JSON 来验证格式
    JSON.parse(editableJson.value);
    hasError.value = false;
    emit('import', editableJson.value);
  } catch (e) {
    hasError.value = true;
    console.error("JSON parsing error:", e);
  }
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal-content {
  background-color: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 600px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.modal-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #1f2937;
}
.modal-description {
  margin: 0;
  font-size: 14px;
  color: #4b5563;
  line-height: 1.5;
}
.json-textarea {
  width: 100%;
  height: 300px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 12px;
  font-family: 'Courier New', Courier, monospace;
  font-size: 14px;
  resize: vertical;
  box-sizing: border-box;
}
.json-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}
.json-textarea.is-error {
  border-color: #ef4444;
}
.error-message {
  color: #ef4444;
  font-size: 13px;
  margin: 4px 0 0 0;
}
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}
.btn-secondary {
  background-color: #e5e7eb;
  color: #374151;
}
.btn-secondary:hover {
  background-color: #d1d5db;
}
.btn-primary {
  background-color: #3b82f6;
  color: white;
}
.btn-primary:hover {
  background-color: #2563eb;
}
</style>