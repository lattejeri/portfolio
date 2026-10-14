// @ts-check
import { defineConfig } from 'astro/config';

// GitHub Pages project sites live at https://<user>.github.io/<repo>/.
// If you rename the repo, update `base` here and `media.output` in .pages.yml.
// Using a custom domain or a <user>.github.io repo? Set base to '/'.
export default defineConfig({
  site: 'https://lattejeri.github.io',
  base: '/site',
});
