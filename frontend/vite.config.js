import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
    plugins: [react()],
    server: {
        port: 5173,
        allowedHosts: [
            "unsalty-catalogic-amee.ngrok-free.dev",
            "ai-consoler-frontend.onrender.com",
            ".onrender.com"
        ],
        proxy: {
            '/api': {
                target: 'http://localhost:8000',
                changeOrigin: true
            }
        }
    },
    preview: {
        allowedHosts: [
            "ai-consoler-frontend.onrender.com",
            ".onrender.com"
        ]
    }
})
