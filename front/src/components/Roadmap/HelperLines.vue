<template>
  <div class="helper-lines">
    <div
      v-if="lines.vertical !== null"
      class="helper-line vertical"
      :style="{ left: `${lines.vertical}px` }"
    />
    <div
      v-if="lines.horizontal !== null"
      class="helper-line horizontal"
      :style="{ top: `${lines.horizontal}px` }"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useVueFlow } from '@vue-flow/core'

const lines = ref({ horizontal: null, vertical: null })

const {
  onNodeDragStart,
  onNodeDrag,
  onNodeDragStop,
  viewport,
  getNodes,
  getParent
} = useVueFlow()

const snapTolerance = 5
const dampingFactor = 0.4

/* ---------- 工具函数 ---------- */
const flowToScreen = pos => ({
  x: pos.x * viewport.value.zoom + viewport.value.x,
  y: pos.y * viewport.value.zoom + viewport.value.y
})

const getAbsolutePosition = node => {
  let x = node.computedPosition.x
  let y = node.computedPosition.y

  // 兼容两种 API 并做空值兜底
  const pickParent = id =>
    typeof getParent === 'function'
      ? getParent(id)               // 新版
      : getParent?.value?.[id]      // 旧版

  let p = pickParent(node.id)
  while (p) {
    x += p.computedPosition?.x ?? 0
    y += p.computedPosition?.y ?? 0
    p = pickParent(p.id)
  }
  return { x, y }
}

/* ---------- 辅助线逻辑 ---------- */
const resetLines = () => {
  lines.value = { horizontal: null, vertical: null }
}

onNodeDragStart(() => resetLines())

onNodeDrag(({ node }) => {
  resetLines()

  const allNodes = getNodes.value.filter(n => n.id !== node.id)
  const { zoom, x: vx, y: vy } = viewport.value

  /* 竖直对齐 */
  const verticalTargets = []
  allNodes.forEach(n => {
    const abs = getAbsolutePosition(n)
    const left   = abs.x
    const center = left + n.dimensions.width / 2
    const right  = left + n.dimensions.width
    verticalTargets.push(left, center, right)
  })

  const nodeAbs = getAbsolutePosition(node)
  const nodeVerticalRefs = [
    nodeAbs.x,
    nodeAbs.x + node.dimensions.width / 2,
    nodeAbs.x + node.dimensions.width
  ]

  let bestV = null
  let snapX = 0
  nodeVerticalRefs.some(ref => {
    return verticalTargets.some(target => {
      const dist = Math.abs(ref - target)
      if (dist < snapTolerance) {
        bestV = target
        snapX = target - (ref - nodeAbs.x) // 目标绝对坐标
        return true
      }
      return false
    })
  })

  if (bestV !== null) {
    const dx = (snapX - nodeAbs.x) * dampingFactor
    node.position.x += dx
    lines.value.vertical = bestV * zoom + vx
  }

  /* 水平对齐 */
  const horizontalTargets = []
  allNodes.forEach(n => {
    const abs = getAbsolutePosition(n)
    const top    = abs.y
    const center = top + n.dimensions.height / 2
    const bottom = top + n.dimensions.height
    horizontalTargets.push(top, center, bottom)
  })

  const nodeHorizontalRefs = [
    nodeAbs.y,
    nodeAbs.y + node.dimensions.height / 2,
    nodeAbs.y + node.dimensions.height
  ]

  let bestH = null
  let snapY = 0
  nodeHorizontalRefs.some(ref => {
    return horizontalTargets.some(target => {
      const dist = Math.abs(ref - target)
      if (dist < snapTolerance) {
        bestH = target
        snapY = target - (ref - nodeAbs.y)
        return true
      }
      return false
    })
  })

  if (bestH !== null) {
    const dy = (snapY - nodeAbs.y) * dampingFactor
    node.position.y += dy
    lines.value.horizontal = bestH * zoom + vy
  }
})

onNodeDragStop(() => resetLines())
</script>

<style scoped>
.helper-lines {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 100;
}

.helper-line {
  position: absolute;
  background-color: rgba(255, 0, 0, 0.5);
}

.vertical {
  width: 1px;
  height: 100%;
}

.horizontal {
  height: 1px;
  width: 100%;
}
</style>