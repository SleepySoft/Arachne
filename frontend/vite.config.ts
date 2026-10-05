import react from "@vitejs/plugin-react";
import path from "path";
import { defineConfig } from "vite";

export default defineConfig(() => {
  const configuredBase = process.env.VITE_PUBLIC_BASE || "/";
  const publicBase = configuredBase.endsWith("/") ? configuredBase : `${configuredBase}/`;
  const apiPrefix = `${publicBase}api`;

  return {
    base: publicBase,
    plugins: [react()],
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
    },
    server: {
      port: 3000,
      proxy: {
        [apiPrefix]: {
          target: "http://localhost:16060",
          changeOrigin: true,
          rewrite: (path) => path.replace(new RegExp(`^${apiPrefix}`), "/api"),
        },
      },
    },
    build: {
      outDir: "dist",
      rollupOptions: {
        input: {
          main: path.resolve(__dirname, "index.html"),
          embed: path.resolve(__dirname, "embed.html"),
        },
      },
    },
  };
});
