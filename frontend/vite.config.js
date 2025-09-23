import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // permite acesso pelo IP da rede
    port: 5173  // porta padrão do Vite, você pode mudar se quiser
  }
})
