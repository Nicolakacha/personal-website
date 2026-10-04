import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://nicolastei.com',
  trailingSlash: 'always',
  integrations: [
    sitemap({
      // /ja/about and /ja/notes/* are legacy duplicates of the canonical
      // /jp/about and /jp/notes/* pages (see their canonicalOverride) — keep
      // those duplicates out so the sitemap only lists canonical URLs.
      filter: (page) =>
        !page.endsWith('/ja/about/') &&
        !/\/ja\/notes\/[^/]+\/$/.test(page),
    }),
  ],
  server: {
    // Allows previewing the dev server through a tunnel (e.g. ngrok) whose
    // hostname changes each run. Only affects `astro dev`, not the static build.
    allowedHosts: true,
  },
});
