import { getImage } from 'astro:assets';

const images = import.meta.glob<{ default: ImageMetadata }>(
  '/src/assets/{works,found}/**/*.{jpg,jpeg,png}',
  { eager: true }
);

function firstImageFilename(sequence: any[]): string | null {
  for (const block of sequence) {
    if (block.type === 'image') return block.src;
    if (block.type === 'pair') return block.images[0].src;
  }
  return null;
}

/** Resolves a work/found entry's first sequence photo into an absolute OG image URL, for social-share previews (falls back to the site default when there's no sequence yet). */
export async function getEntryOgImage(
  routeSlug: string,
  sequence: any[],
  collection: 'works' | 'found',
  site: URL | undefined
): Promise<string | undefined> {
  const filename = firstImageFilename(sequence);
  if (!filename) return undefined;
  const image = images[`/src/assets/${collection}/${routeSlug}/${filename}`];
  if (!image) return undefined;
  const optimized = await getImage({ src: image.default, width: 1200, format: 'jpg' });
  return site ? new URL(optimized.src, site).toString() : optimized.src;
}
