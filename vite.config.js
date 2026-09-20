import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],

  server: {
    host: "localhost",
    port: 5173,

    // Backend API runs separately.
    // Vite proxy forwards /api requests to FastAPI.
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true
      }
    }
  },

  build: {
    outDir: "dist",
    sourcemap: false
  }
});