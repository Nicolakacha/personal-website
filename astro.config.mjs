import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://teikoh.example',
  trailingSlash: 'always',
  integrations: [sitemap()],
  server: {
    // Allows previewing the dev server through a tunnel (e.g. ngrok) whose
    // hostname changes each run. Only affects `astro dev`, not the static build.
    allowedHosts: true,
  },
});
