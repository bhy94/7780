import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// elementPlus按需导入
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    // ...
    AutoImport({
      resolvers: [ElementPlusResolver()],
    }),
    Components({
      resolvers: [
        // 1. 配置elementPlus采用sass样式配色系统
        ElementPlusResolver({ importStyle: "sass" }),
      ],
    }),
  ],
  build: {
    // 输出目录
    outDir: 'build',
    // 静态资源服务的文件夹，默认是public
    assetsDir: '',
    // 生成静态资源的存放路径
    rollupOptions: {
      output: {
        // 入口文件的输出路径
        entryFileNames: 'js/[name].[hash].js',
        // chunk文件的输出路径
        chunkFileNames: 'js/[name].[hash].js',
        // CSS文件的输出路径
        assetFileNames: ({name}) => {
          if (/\.(css|sass|scss)$/.test(name)) {
            return 'css/[name].[hash].[ext]';
          }
          return '[ext]/[name].[hash].[ext]';
        },
      },
    },
  },
  resolve: {
    // 实际的路径转换  @  -> src
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  css: {
    preprocessorOptions: {
      scss: {
        // 2. 自动导入定制化样式文件进行样式覆盖
        additionalData: `
          @use "@/styles/element/index.scss" as *;
          @use "@/styles/var.scss" as *;
        `,
      }
    }
  },
  server: {
    port: 3030,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    }
  },
})
