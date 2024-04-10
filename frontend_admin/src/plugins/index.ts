// Plugins
import router from '../router' 
import ElementPlus from 'element-plus'

// Types
import type {App} from 'vue'

// Styles
import 'element-plus/dist/index.css'
import '../styles/style.css'
import '../styles/tailwind.css'
import 'animate.css'
import 'normalize.css/normalize.css'


export function registerPlugins (app: App) {
  app
    .use(ElementPlus)
    .use(router)
}
