import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const posts = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/posts' }),
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    date: z.coerce.date(),
    draft: z.boolean().default(false),
    tags: z.array(z.string()).default([]),
  }),
});

const image = z.object({
  src: z.string(),
  alt: z.string().default(''),
});

// Page blocks, keyed by `type` (Pages CMS `blockKey`).
const block = z.discriminatedUnion('type', [
  z.object({ type: z.literal('text'), body: z.string().default('') }),
  image.extend({ type: z.literal('image') }),
  image.extend({ type: z.literal('imageInline') }),
  image.extend({ type: z.literal('imageWide') }),
  z.object({ type: z.literal('columns2'), images: z.array(image).default([]) }),
  z.object({ type: z.literal('columns3'), images: z.array(image).default([]) }),
]);

const work = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/work' }),
  schema: z.object({
    title: z.string(),
    byline: z.string().optional(),
    draft: z.boolean().default(false),
    blocks: z.array(block).default([]),
  }),
});

export const collections = { posts, work };
