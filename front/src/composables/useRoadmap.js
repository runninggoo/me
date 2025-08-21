// src/composables/useRoadmap.js

import { ref, computed, nextTick, reactive } from 'vue';
import { useVueFlow } from '@vue-flow/core';
import { v4 as uuidv4 } from 'uuid';
import { createNodeData, NodeTypes } from 'src/data/RoadmapnodeDefinitions';

export function useRoadmap(elements) {
  const {
    addEdges,
    addNodes,
    removeNodes,
    removeEdges,
    getSelectedNodes,
    getEdges,
    findNode,
    screenToFlowCoordinate,
    fitView,
  } = useVueFlow();

  const selectedNode = ref(null);
  const selectedEdge = ref(null);
  const isAddModalOpen = ref(false);
  const isJsonModalOpen = ref(false);
  const jsonModalData = ref('');
  const jsonModalMode = ref('export');
  const nodeToTransfer = ref(null);
  const contextMenu = reactive({ visible: false, position: { x: 0, y: 0 }, targetNode: null });
  const isTransferModalOpen = ref(false);

  const isSelectionActive = computed(() => !!(selectedNode.value || selectedEdge.value));

  /**
   * [最终修复] 统一的、安全的节点删除函数，解决了时序问题。
   * @param {object} nodeToDelete 要删除的节点对象
   */
  const deleteNodeAndChildren = (nodeToDelete) => {
    if (!nodeToDelete) return;

    // 检查节点是否为带有子节点的 group
    if (nodeToDelete.type === 'group') {
      const allNodes = elements.value.filter(el => el.position);
      const children = allNodes.filter(child => child.parentNode === nodeToDelete.id);

      if (children.length > 0) {
        // 第一步：更新 elements 数组，转换子节点坐标
        elements.value = elements.value.map(el => {
          const isChild = children.some(child => child.id === el.id);
          if (isChild) {
            const newPosition = {
              x: el.position.x + nodeToDelete.position.x,
              y: el.position.y + nodeToDelete.position.y,
            };
            return {
              ...el,
              position: newPosition,
              parentNode: undefined,
              extent: undefined,
            };
          }
          return el;
        });

        // 第二步：使用 nextTick 确保上述更新完成后，再执行删除操作
        nextTick(() => {
          removeNodes([nodeToDelete], true);
        });

        // 提前返回，避免执行下面的默认删除逻辑
        return;
      }
    }

    // 默认情况：如果节点不是 group，或是空的 group，直接删除
    removeNodes([nodeToDelete], true);
  };

  const handleContextMenuAction = (action) => {
    const node = contextMenu.targetNode;
    if (!node) return;

    switch (action) {
      case 'copy': {
        const newPosition = { x: node.position.x + 20, y: node.position.y + 20 };
        const newNode = {
          id: `${node.type}-${uuidv4()}`,
          type: node.type,
          position: newPosition,
          data: JSON.parse(JSON.stringify(node.data)),
          selected: false,
          parentNode: node.parentNode,
          extent: node.parentNode ? 'parent' : undefined,
          style: node.style ? JSON.parse(JSON.stringify(node.style)) : undefined,
        };
        addNodes([newNode]);
        break;
      }
      case 'delete':
        deleteNodeAndChildren(node); // 调用修复后的函数
        break;
      case 'transfer':
        nodeToTransfer.value = node;
        isTransferModalOpen.value = true;
        break;
    }
    closeContextMenu();
  };
  
  const deleteSelection = () => {
    if (selectedNode.value) {
      deleteNodeAndChildren(selectedNode.value); // 调用修复后的函数
    }
    if (selectedEdge.value) {
      removeEdges([selectedEdge.value]);
    }
    deselectAll();
  };

  
  const deselectAll = () => {
    selectedNode.value = null;
    selectedEdge.value = null;
    getSelectedNodes.value.forEach(n => (n.selected = false));
    getEdges.value.forEach(e => (e.selected = false));
  };
  
  const closeContextMenu = () => {
    if (contextMenu.visible) {
      contextMenu.visible = false;
      contextMenu.targetNode = null;
    }
  };
  
  const onPaneClick = () => {
    deselectAll();
    closeContextMenu();
  };

  const onNodeClick = ({ node }) => {
    closeContextMenu();
    deselectAll(); 
    node.selected = true;
    selectedNode.value = node;
  };

  const onEdgeClick = ({ edge }) => {
    deselectAll();
    closeContextMenu();
    edge.selected = true;
    selectedEdge.value = edge;
  };

  const onNodeContextMenu = ({ event, node }) => {
    event.preventDefault();
    contextMenu.targetNode = node;
    contextMenu.position = { x: event.clientX, y: event.clientY };
    contextMenu.visible = true;
  };

  const onPaneContextMenu = (event) => {
    event.preventDefault();
    closeContextMenu();
  };

  const groupedNodesTree = computed(() => {
    const allNodes = elements.value.filter(el => el.position);
    const groupNodes = allNodes.filter(el => el.type === 'group');
    const nodeMap = {};
    const tree = [];
    
    const nodesToExclude = new Set();
    const targetNodeId = nodeToTransfer.value?.id;

    if (targetNodeId) {
      nodesToExclude.add(targetNodeId);
      const queue = [targetNodeId];

      while (queue.length > 0) {
        const currentId = queue.shift();
        const children = allNodes.filter(n => n.parentNode === currentId);
        for (const child of children) {
          queue.push(child.id);
          if (child.type === 'group') {
            nodesToExclude.add(child.id);
          }
        }
      }
    }

    groupNodes.forEach(node => {
      if (!nodesToExclude.has(node.id)) {
        nodeMap[node.id] = { ...node, children: [] };
      }
    });

    Object.values(nodeMap).forEach(node => {
      if (node.parentNode && nodeMap[node.parentNode]) {
        nodeMap[node.parentNode].children.push(node);
      } else {
        tree.push(node);
      }
    });
    return tree;
  });

  const handleTransferOwnership = (newParentId) => {
    const nodeToMove = findNode(nodeToTransfer.value?.id);
    if (!nodeToMove) {
      nodeToTransfer.value = null;
      return;
    }

    const oldParent = nodeToMove.parentNode ? findNode(nodeToMove.parentNode) : null;
    const newParent = newParentId ? findNode(newParentId) : null;
    let absoluteX = nodeToMove.position.x;
    let absoluteY = nodeToMove.position.y;
    if (oldParent) {
      absoluteX += oldParent.position.x;
      absoluteY += oldParent.position.y;
    }
    nodeToMove.parentNode = newParentId || undefined;
    nodeToMove.extent = newParentId ? 'parent' : undefined;
    if (newParent) {
      nodeToMove.position = {
        x: absoluteX - newParent.position.x,
        y: absoluteY - newParent.position.y,
      };
    } else {
      nodeToMove.position = {
        x: absoluteX,
        y: absoluteY,
      };
    }
    isTransferModalOpen.value = false;
    nodeToTransfer.value = null;
  };

  const openAddModal = () => {
    isAddModalOpen.value = true;
  };

  const addNode = (type) => {
    const position = screenToFlowCoordinate({
      x: window.innerWidth / 2.2,
      y: window.innerHeight / 3,
    });
    
    const newNode = {
      id: `${type}-${uuidv4()}`,
      type,
      data: createNodeData(type),
      position,
    };

    if (type === NodeTypes.GROUP) {
      newNode.style = { width: '400px', height: '300px' };
      newNode.zIndex = -1;
    }

    addNodes([newNode]);
  };

  const onElementPropertyUpdate = ({ target, key, value }) => {
    const element = target === 'node' ? selectedNode.value : selectedEdge.value;
    if (!element) return;
    const propertyTarget = target === 'node' ? element.data : element;
    if (key === null && typeof value === 'object') {
      Object.assign(propertyTarget, value);
    } else {
      propertyTarget[key] = value;
    }
  };

  const isValidConnection = (connection) => {
    const sourceNode = findNode(connection.source);
    const targetNode = findNode(connection.target);
    if (!sourceNode || !targetNode) return false;
    const sourceHandleType = sourceNode.data.handles?.[connection.sourceHandle];
    const targetHandleType = targetNode.data.handles?.[connection.targetHandle];
    return sourceHandleType === 'source' && targetHandleType === 'target';
  };

  const onConnect = (params) => {
    addEdges([{ ...params, id: `edge-${uuidv4()}`, markerEnd: 'arrowclosed' }]);
  };

  const openJsonModal = (mode) => {
    jsonModalMode.value = mode;
    if (mode === 'export') {
      jsonModalData.value = JSON.stringify(elements.value, null, 2);
    } else {
      jsonModalData.value = '[]';
    }
    isJsonModalOpen.value = true;
  };

  const importFromJson = (jsonString) => {
    try {
      const parsedElements = JSON.parse(jsonString);
      elements.value = parsedElements;
      isJsonModalOpen.value = false;
      nextTick(() => fitView());
    } catch (error) {
      alert(`导入失败: ${error.message}`);
    }
  };

  return {
    selectedNode,
    selectedEdge,
    isSelectionActive,
    isAddModalOpen,
    isJsonModalOpen,
    jsonModalData,
    jsonModalMode,
    onPaneClick,
    onNodeClick,
    onEdgeClick,
    onConnect,
    isValidConnection,
    onElementPropertyUpdate,
    openAddModal,
    addNode,
    deleteSelection,
    deselectAll,
    openJsonModal,
    importFromJson,
    contextMenu,
    onNodeContextMenu,
    onPaneContextMenu,
    closeContextMenu,
    handleContextMenuAction,
    isTransferModalOpen,
    groupedNodesTree,
    handleTransferOwnership,
  };
}