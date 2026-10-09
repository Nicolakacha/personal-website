import type { CollectionEntry } from 'astro:content';

export const INSTAGRAM_URL = 'https://instagram.com/teikoh_';
export const PERSON_ID = 'https://nicolastei.com/#person';

const schemaLanguage = (lang: string) => (lang === 'zh' ? 'zh-TW' : lang);

/** BreadcrumbList JSON-LD (Home › section › page) — a type Google shows in search results. */
export function breadcrumbStructuredData(items: { name: string; url: URL | string }[]) {
  return {
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: item.name,
      item: item.url.toString(),
    })),
  };
}

/** BlogPosting JSON-LD plus breadcrumbs for one note, so search engines read it as a dated article by Nicolas Tei. */
export function noteStructuredData(note: CollectionEntry<'notes'>, url: URL) {
  const home = new URL(note.data.lang === 'ja' ? '/jp/' : '/', url);
  const notesIndex = new URL(note.data.lang === 'ja' ? '/jp/notes/' : '/notes/', url);
  return [{
    '@type': 'BlogPosting',
    '@id': `${url}#article`,
    headline: note.data.title,
    description: note.data.description,
    datePublished: note.data.date?.toISOString(),
    inLanguage: schemaLanguage(note.data.lang),
    url: url.toString(),
    mainEntityOfPage: url.toString(),
    image: new URL('/og-default.jpg', url).toString(),
    author: { '@id': PERSON_ID },
  }, breadcrumbStructuredData([
    { name: 'Nicolas Tei', url: home },
    { name: 'Notes', url: notesIndex },
    { name: note.data.title ?? 'Note', url },
  ])];
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

/** CreativeWork JSON-LD plus breadcrumbs for one photo series. */
export function workStructuredData(work: CollectionEntry<'works'>, url: URL, lang: 'en' | 'ja', image: string | undefined) {
  const base = lang === 'ja' ? '/jp/' : '/';
  return [{
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
  }, breadcrumbStructuredData([
    { name: 'Nicolas Tei', url: new URL(base, url) },
    { name: 'Projects', url: new URL(`${base}projects/`, url) },
    { name: lang === 'ja' ? (work.data.titleJa ?? work.data.title) : work.data.title, url },
  ])];
}
