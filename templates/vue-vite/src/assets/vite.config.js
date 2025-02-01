import { fileURLToPath, URL } from 'node:url'
import { resolve } from 'node:path';
import path from 'node:path';
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'


// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
//  root: resolve('./src'),
  base: '/static/vite/',
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  build: {
    manifest: "manifest.json",
    outDir: path.resolve('./build'),
    rollupOptions: {
      input: {
        main: resolve('./src/main.js'),
//        test: resolve('./src/test.js'),
      },
    },
  },
})
