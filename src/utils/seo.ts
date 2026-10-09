import type { CollectionEntry } from 'astro:content';

export const INSTAGRAM_URL = 'https://instagram.com/teikoh_';
export const PERSON_ID = 'https://nicolastei.com/#person';

const schemaLanguage = (lang: string) => (lang === 'zh' ? 'zh-TW' : lang);

/** BlogPosting JSON-LD for one note, so search engines read it as a dated article by Nicolas Tei. */
export function noteStructuredData(note: CollectionEntry<'notes'>, url: URL) {
  return {
    '@type': 'BlogPosting',
    '@id': `${url}#article`,
    headline: note.data.title,
    description: note.data.description,
    datePublished: note.data.date?.toISOString(),
    inLanguage: schemaLanguage(note.data.lang),
    url: url.toString(),
    mainEntityOfPage: url.toString(),
    author: { '@id': PERSON_ID },
  };
}

function photoCount(sequence: CollectionEntry<'works'>['data']['sequence']) {
  return sequence.reduce((count, block) => count + (block.type === 'image' ? 1 : block.type === 'pair' ? 2 : 0), 0);
}

/** Meta description for a work page: its own deck when written, otherwise a factual summary. */
export function workDescription(work: CollectionEntry<'works'>, lang: 'en' | 'ja') {
  if (lang === 'ja' && work.data.deckJa) return work.data.deckJa;
  if (lang === 'en' && (work.data.deck ?? work.data.description)) return work.data.deck ?? work.data.description;
  const count = photoCount(work.data.sequence);
  return lang === 'ja'
    ? `写真家 Nicolas Tei による写真作品「${work.data.titleJa ?? work.data.title}」（${work.data.year}年、${count}点）。フォトブックとして構成された写真のシークエンス。`
    : `“${work.data.title}” — a photo series by Nicolas Tei (${work.data.year}, ${count} photographs), presented as a photo-book sequence.`;
}

/** CreativeWork JSON-LD for one photo series. */
export function workStructuredData(work: CollectionEntry<'works'>, url: URL, lang: 'en' | 'ja', image: string | undefined) {
  return {
    '@type': 'CreativeWork',
    '@id': `${url}#work`,
    name: lang === 'ja' ? (work.data.titleJa ?? work.data.title) : work.data.title,
    alternateName: lang === 'ja' ? work.data.title : work.data.titleJa,
    description: workDescription(work, lang),
    genre: 'Photography',
    dateCreated: work.data.year,
    inLanguage: lang,
    url: url.toString(),
    image,
    creator: { '@id': PERSON_ID },
  };
}
