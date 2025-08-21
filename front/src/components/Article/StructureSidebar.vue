<script setup>
import { computed } from 'vue'

const props = defineProps({ editor: { type: Object, required: true } })

const nodeTypeLabels = {
    heading: (level) => `H${level}`,
    paragraph: 'P',
    blockquote: 'Quote',
    bulletList: 'bList',
    orderedList: 'oList',
    codeBlock: 'Code',
}

// 需要统计的内联节点类型
const inlineTypes = ['inlineImage', 'inlineMath']

const blocks = computed(() => {
    if (!props.editor) return []

    const result = []
    const editorRect = props.editor.view.dom.getBoundingClientRect()

    props.editor.state.doc.descendants((node, pos) => {
        const label = nodeTypeLabels[node.type.name]
        if (!label) return true

        const dom = props.editor.view.nodeDOM(pos)
        if (!dom) return true

        // 统计内部内联节点
        const counts = Object.fromEntries(inlineTypes.map(t => [t, 0]))
        node.descendants((child) => {
            if (inlineTypes.includes(child.type.name)) counts[child.type.name]++
        })

        const badges = [
            counts.inlineImage ? `IMG×${counts.inlineImage}` : '',
            counts.inlineMath ? `MATH×${counts.inlineMath}` : ''
        ].filter(Boolean)

        result.push({
            key: pos,
            label: typeof label === 'function' ? label(node.attrs.level) : label,
            badges,
            top: dom.getBoundingClientRect().top - editorRect.top,
            height: dom.getBoundingClientRect().height
        })
        return true
    })
    return result
})
</script>

<template>
    <div class="structure-sidebar">
        <div v-for="b in blocks" :key="b.key" class="sidebar-item"
            :style="{ top: `${b.top}px`, height: `${b.height}px` }">
            <span class="label">{{ b.label }}</span>
            <span v-if="b.badges.length" class="badges">
                {{ b.badges.join(' ') }}
            </span>
        </div>
    </div>
</template>

<style scoped>
.structure-sidebar {
    position: absolute;
    top: 0;
    right: -6rem;
    width: 5.5rem;
    height: 100%;
    pointer-events: none;
}

.sidebar-item {
    position: absolute;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
}

.label {
    font-size: 0.75rem;
    font-family: monospace;
    color: #adb5bd;
}

.badges {
    font-size: 0.6rem;
    color: #68cef8;
    margin-top: 2px;
}
</style>