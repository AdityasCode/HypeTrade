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
        target: 'https://hypetrade-gcp-server-800055345422.us-central1.run.app',
        changeOrigin: true,
        rewrite: path => path.replace(/^\/api/, '/api'),
      }
    }
  },
  base: '/',
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      external: [
          './src/config.ts'
      ]
    }
  }
})