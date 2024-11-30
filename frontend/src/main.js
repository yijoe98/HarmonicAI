import { createApp } from 'vue'
import App from '@/App.vue'
import Router from '@/router'
import ElementPlus from 'element-plus'

// createApp(App).mount('#app')
createApp(App).use(Router).use(ElementPlus).mount('#app');
