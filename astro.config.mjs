import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://nicolastei.com',
  trailingSlash: 'always',
  integrations: [
    sitemap({
      // Found is hidden from nav and has no content yet, and /jp is an
      // unlinked trial Japanese mirror — keep both out of the sitemap.
      filter: (page) => !page.includes('/found/') && !page.includes('/jp/'),
    }),
  ],
  server: {
    // Allows previewing the dev server through a tunnel (e.g. ngrok) whose
    // hostname changes each run. Only affects `astro dev`, not the static build.
    allowedHosts: true,
  },
});
