// useMindmap.js
import { ref, shallowRef, onBeforeUnmount, readonly } from 'vue';
import MindMap from 'simple-mind-map';

//plugins
import MiniMap from 'simple-mind-map/src/plugins/MiniMap.js'
import Drag from 'simple-mind-map/src/plugins/Drag.js';
import Select from 'simple-mind-map/src/plugins/Select.js';
//import RichText from 'simple-mind-map/src/plugins/RichText.js'
//import Formula from 'simple-mind-map/src/plugins/Formula.js'

//theme
import Themes from 'simple-mind-map-plugin-themes';
import themeList from 'simple-mind-map-plugin-themes/themeList';

MindMap.usePlugin(Drag).usePlugin(Select).usePlugin(MiniMap);

//注册主题
Themes.init(MindMap);

export function useMindMap() {
  const mindMap = shallowRef(null);
  const isMindMapReady = ref(false);
  const isContextMenuVisible = ref(false);
  const contextMenuPosition = ref({ top: 0, left: 0 });
  const isNodeContextMenu = ref(false);
  const showContextMenu = (e, isNode) => {
    e.preventDefault();
    contextMenuPosition.value = { top: e.clientY, left: e.clientX };
    isContextMenuVisible.value = true;
    isNodeContextMenu.value = isNode;
  };
  const hideContextMenu = () => {
    isContextMenuVisible.value = false;
  };

  const init = (containerEl, initialData) => {
    let dataForConstructor = { 
      data: { text: "根节点" },
      children: []
    };

    if (initialData) {
      if (initialData.root) {
        dataForConstructor = initialData.root;
      } else {
        dataForConstructor = initialData;
      }
    }

    mindMap.value = new MindMap({
      el: containerEl,
      data: dataForConstructor,
      defaultTheme: 'default',
    });

    if (initialData && initialData.root) {
        if(initialData.layout) {
            mindMap.value.setLayout(initialData.layout);
        }
        if(initialData.theme && initialData.theme.template) {
            mindMap.value.setTheme(initialData.theme.template);
        }
    }

    isMindMapReady.value = true;
    mindMap.value.on('node_contextmenu', (e) => {
      showContextMenu(e, true);
    });
    mindMap.value.on('contextmenu', (e) => {
      showContextMenu(e, false);
    });
  };

  onBeforeUnmount(() => {
    mindMap.value?.off('node_contextmenu', showContextMenu);
    mindMap.value?.off('contextmenu', showContextMenu);
    mindMap.value?.destroy();
  });

  const addNode = () => mindMap.value?.execCommand('INSERT_CHILD_NODE');
  const removeNode = () => mindMap.value?.execCommand('REMOVE_NODE');
  const undo = () => mindMap.value?.execCommand('BACK');
  const redo = () => mindMap.value?.execCommand('FORWARD');
  const resetlayout = ()=> mindMap.execCommand('RESET_LAYOUT');
  const setTheme = (theme) => mindMap.value?.setTheme(theme);
  const setLayout = (layout) => mindMap.value?.setLayout(layout);
  const getThemeList = () => {return themeList;};

  const exportJson = () => {
    const data = mindMap.value?.getData(true);
    if (!data) return;
    const jsonStr = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = '思维导图.json';
    a.click();
    URL.revokeObjectURL(url);
  };

  const importJson = (file) => {
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (event) => {
      try {
        const data = JSON.parse(event.target.result);
        mindMap.value?.setData(data);
      } catch (e) {
        alert('解析JSON文件失败，请检查文件格式。');
        console.error(e);
      }
    };
    reader.readAsText(file);
  };


  const copyNode = () => {
    mindMap.value?.renderer.copy();
    hideContextMenu();
  };

  const cutNode = () => {
    mindMap.value?.renderer.cut();
    hideContextMenu();
  };

  const pasteNode = () => {
    mindMap.value?.renderer.paste();
    hideContextMenu();
  };

  const removeCurrentNode = () => {
    // simple-mind-map 的 REMOVE_NODE 命令会删除当前激活的节点
    // 由于右键点击时节点会自动激活，所以可以直接调用
    mindMap.value?.execCommand('REMOVE_NODE');
    hideContextMenu();
  };

  const setDataJson = (json) => mindMap.value?.setData(json)   // 父组件塞 JSON
  const getDataJson = () => mindMap.value?.getData(true)       // 拿 JSON

  return {
    mindMap,
    isMindMapReady: readonly(isMindMapReady),
    init,
    addNode,
    removeNode,
    undo,
    redo,
    setTheme,
    getThemeList,
    setLayout,
    exportJson,
    importJson,
    isContextMenuVisible: readonly(isContextMenuVisible),
    contextMenuPosition: readonly(contextMenuPosition),
    isNodeContextMenu: readonly(isNodeContextMenu),
    hideContextMenu,
    copyNode,
    cutNode,
    pasteNode,
    removeCurrentNode,
    setDataJson,
    getDataJson
    };
}
