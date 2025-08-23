// main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router/index.js'

// Vue Flow 核心样式
import '@vue-flow/core/dist/style.css'
import '@vue-flow/core/dist/theme-default.css'
import '@vue-flow/controls/dist/style.css'

//TipTapEditor 核心样式
import 'katex/dist/katex.min.css'
import 'highlight.js/styles/github-dark.css'
import 'tippy.js/dist/tippy.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

app.mount('#app')
