import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://teikoh.example',
  trailingSlash: 'always',
  integrations: [sitemap()],
});
