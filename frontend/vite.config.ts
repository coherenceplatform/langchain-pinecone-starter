import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [svelte()],
  strictPort: true,
  hmr: {
      Port: process.env.PORT,
      clientPort: 443
  }
})