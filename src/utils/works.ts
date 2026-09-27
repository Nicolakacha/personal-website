import { getCollection, type CollectionEntry } from 'astro:content';

export function sortWorks(works: CollectionEntry<'works'>[]) {
  return works.sort(
    (a, b) =>
      a.data.order - b.data.order ||
      b.data.year.localeCompare(a.data.year) ||
      a.data.title.localeCompare(b.data.title)
  );
}

export async function getVisibleWorks() {
  const works = await getCollection('works', ({ data }) => data.status !== 'hidden');
  return sortWorks(works);
}
