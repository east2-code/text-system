import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import i18n from './i18n'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

// 读取主题
const theme = localStorage.getItem('theme') || 'colorful'
document.body.setAttribute('data-theme', theme)

const minimal = localStorage.getItem('minimal') === '1'
document.body.setAttribute('data-minimal', minimal ? '1' : '')

const app = createApp(App)
app.use(router)
app.use(ElementPlus)
app.use(i18n)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
app.mount('#app')