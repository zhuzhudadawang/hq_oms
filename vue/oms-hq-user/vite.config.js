import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  },
  server: {
    port: 3000,
    open: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },
   // 新增：构建优化配置（拆分大依赖、调整警告阈值）
  // build: {
  //   rollupOptions: {
  //     output: {
  //       // 关键：把大型依赖单独打包成独立 chunk
  //       manualChunks: {
  //         'echarts': ['echarts'], // ECharts 单独拆分（解决图表相关 chunk 过大）
  //         'element-plus': ['element-plus'], // Element Plus 单独拆分（可选，进一步优化）
  //         'shared-utils': ['axios', 'lodash'] // 共享工具库拆分（如果项目用到了可保留）
  //       }
  //     }
  //   }
  // }
})
