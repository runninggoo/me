import { ref, computed } from 'vue';

export function useRoadmapViewer() {
  const selectedNode = ref(null);
  const selectedEdge = ref(null);

  const isTaskSidebarOpen = computed(() => selectedNode.value?.type === 'task');

  const deselectAll = () => {
    selectedNode.value = null;
    selectedEdge.value = null;
  };

  const onNodeClick = ({ node }) => {
    deselectAll();
    node.selected = true;
    selectedNode.value = node;
  };

  const onEdgeClick = ({ edge }) => {
    deselectAll();
    edge.selected = true;
    selectedEdge.value = edge;
  };

  const onPaneClick = () => deselectAll();

  const onKeyDown = (e) => {
    if (e.key === 'Escape') deselectAll();
  };

  return {
    selectedNode,
    isTaskSidebarOpen,
    deselectAll,
    onNodeClick,
    onEdgeClick,
    onPaneClick,
    onKeyDown,
  };
}