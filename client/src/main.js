import {createApp} from 'vue'
import App from './App.vue'
// 存储
import {createPinia} from 'pinia'
// 路由
import router from "@/router";
// element ui
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
// element ui icons
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import Particles from "particles.vue3";

// common css
import '@/assets/css/common.css'

const app = createApp(App)

const pinia = createPinia()
app.use(pinia)

app.use(router)

app.use(ElementPlus)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

app.use(Particles)

// 挂载
app.mount('#app')
