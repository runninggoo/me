import { createNodeData, NodeTypes } from './RoadmapnodeDefinitions';

export const initialRoadmap = [
  {
    id: 'topic-1',
    type: NodeTypes.TOPIC,
    position: { x: 450, y: 50 },
    data: createNodeData(NodeTypes.TOPIC, {
      label: 'My Roadmap Core',
    })
  },
  {
    id: 'task-1',
    type: NodeTypes.TASK,
    position: { x: 25, y: 70 },
    data: createNodeData(NodeTypes.TASK, {
      label: 'Complete Project Deployment',
    }),
    parentNode: 'group-1',
    extent: 'parent',
  },
  {
    id: 'group-1',
    type: NodeTypes.GROUP,
    position: { x: 50, y: 50 },
    width: 350,
    height: 200,
    // 优化：设置 zIndex 使其位于其他节点之下
    zIndex: -1,
    data: createNodeData(NodeTypes.GROUP, {
      label: 'Phase One',
      color: 'blue',
    }),
  }
];

export const initialArticle = {
  type: 'doc',
  content: [
    {
      type: 'heading',
      attrs: {
        textAlign: null,
        level: 1
      },
      content: [
        {
          type: 'text',
          text: 'Titles'
        }
      ]
    },
    {
      type: 'paragraph',
      attrs: {
        textAlign: null
      },
      content: [
        {
          type: 'text',
          text: 'the word is the world.'
        }
      ]
    }
  ]
};

export const initialMindmap = {
  data: { text: '根节点' },
  children: [
    { data: { text: '子节点 1' } },
    { data: { text: '子节点 2' } }
  ]
};