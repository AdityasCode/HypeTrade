import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  esbuild: {
    logOverride: { 'this-is-undefined-in-esm': 'silent' }, // common for react
  },
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'https://<your-cloud-run-url>.a.run.app',
        changeOrigin: true,
        rewrite: path => path.replace(/^\/api/, '/api'),
      }
    }
  },
  base: '/',
  build: {
    outDir: 'dist'
  }
})