import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import ViteFonts from 'unplugin-fonts/vite'
import { fileURLToPath, URL } from 'node:url'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    ViteFonts({
      google: {
        families: [{
          name: 'Roboto',
          styles: 'wght@100;300;400;500;700;900',
        }],
      },
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
  define: { 'process.env': {} },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
    extensions: [
      '.js',
      '.json',
      '.jsx',
      '.mjs',
      '.ts',
      '.tsx',
      '.vue',
    ],
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    }
  },
})
