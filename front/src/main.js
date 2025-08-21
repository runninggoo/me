// main.js
import { createApp } from 'vue'
import App from './App.vue'

// Vue Flow 核心样式
import '@vue-flow/core/dist/style.css'
import '@vue-flow/core/dist/theme-default.css'
import '@vue-flow/controls/dist/style.css'

//TipTapEditor 核心样式
import 'katex/dist/katex.min.css'
import 'highlight.js/styles/github-dark.css'
import 'tippy.js/dist/tippy.css'

createApp(App).mount('#app')
