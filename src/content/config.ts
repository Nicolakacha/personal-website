import { defineCollection, z } from 'astro:content';

const altImage = z.object({
  src: z.string(),
  alt: z.string().optional(),
  decorative: z.boolean().default(false),
}).refine((image) => image.decorative || Boolean(image.alt?.trim()), {
  message: 'alt is required unless decorative: true',
});

const imageBlock = z.object({
  src: z.string(), alt: z.string().optional(), decorative: z.boolean().default(false),
  type: z.literal('image'),
  size: z.enum(['small', 'medium', 'large', 'full']).default('large'),
  align: z.enum(['left', 'center', 'right']).default('center'),
  gapAfter: z.enum(['tight', 'normal', 'large', 'pause']).default('normal'),
  caption: z.string().optional(),
}).refine((image) => image.decorative || Boolean(image.alt?.trim()), { message: 'alt is required unless decorative: true' });
const pairBlock = z.object({
  type: z.literal('pair'), images: z.tuple([altImage, altImage]),
  size: z.enum(['small', 'medium', 'large']).default('medium'),
  ratio: z.enum(['equal', 'left-heavy', 'right-heavy']).default('equal'),
  gapAfter: z.enum(['tight', 'normal', 'large', 'pause']).default('normal'), caption: z.string().optional(),
});
const breakBlock = z.object({ type: z.literal('break'), size: z.enum(['large', 'pause']).default('pause') });

const sequence = z.array(z.union([imageBlock, pairBlock, breakBlock])).default([]);

const works = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(), nativeTitle: z.string().optional(),
    routeSlug: z.string().regex(/^[a-z0-9]+(-[a-z0-9]+)*$/), year: z.string(),
    status: z.enum(['published', 'hidden', 'ongoing']).default('hidden'), order: z.number().default(0),
    deck: z.string().max(140).optional(), description: z.string().optional(), location: z.string().optional(),
    sequence,
  }),
});
const found = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(), nativeTitle: z.string().optional(),
    routeSlug: z.string().regex(/^[a-z0-9]+(-[a-z0-9]+)*$/), year: z.string(),
    status: z.enum(['published', 'hidden', 'ongoing']).default('hidden'), order: z.number().default(0),
    deck: z.string().max(140).optional(), description: z.string().optional(),
    provenance: z.string().optional(),
    sequence,
  }),
});
const notes = defineCollection({ type: 'content', schema: z.object({ title: z.string().optional(), date: z.date().optional(), routeSlug: z.string().regex(/^[a-z0-9]+(-[a-z0-9]+)*$/), status: z.enum(['published', 'hidden']).default('published') }) });
const about = defineCollection({ type: 'content', schema: z.object({ title: z.string().default('About') }) });
export const collections = { works, found, notes, about };




