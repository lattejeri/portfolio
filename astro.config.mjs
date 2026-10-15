// @ts-check
import { defineConfig, fontProviders } from 'astro/config';

// Redaction ships in degradation levels: plain, 10, 20, 35, 50, 70, 100.
// Each becomes its own family + CSS variable, e.g. --font-redaction-35.
const redactionLevels = ['', '10', '20', '35', '50', '70', '100'];

const redaction = redactionLevels.map((level) => {
  const file = (style) =>
    `./src/assets/fonts/redaction/Redaction${level ? `_${level}` : ''}-${style}.woff2`;
  return {
    provider: fontProviders.local(),
    name: level ? `Redaction ${level}` : 'Redaction',
    cssVariable: level ? `--font-redaction-${level}` : '--font-redaction',
    fallbacks: ['Georgia', 'serif'],
    options: {
      variants: [
        { src: [file('Regular')], weight: 400, style: 'normal' },
        { src: [file('Italic')], weight: 400, style: 'italic' },
        { src: [file('Bold')], weight: 700, style: 'normal' },
      ],
    },
  };
});

// GitHub Pages project sites live at https://<user>.github.io/<repo>/.
// If you rename the repo, update `base` here and `media.output` in .pages.yml.
// Using a custom domain or a <user>.github.io repo? Set base to '/'.
export default defineConfig({
  site: 'https://lattejeri.github.io',
  base: '/site',
  fonts: [
    {
      provider: fontProviders.google(),
      name: 'Inter Tight',
      cssVariable: '--font-inter-tight',
      weights: ['100 900'],
      styles: ['normal', 'italic'],
      subsets: ['latin'],
      fallbacks: ['system-ui', 'sans-serif'],
    },
    {
      provider: fontProviders.google(),
      name: 'Just Me Again Down Here',
      cssVariable: '--font-just-me',
      weights: [400],
      subsets: ['latin'],
      fallbacks: ['cursive'],
    },
    ...redaction,
  ],
});
