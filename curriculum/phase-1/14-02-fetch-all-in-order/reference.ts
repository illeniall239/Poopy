// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export type FetchPage = (url: string) => Promise<string>;

export async function fetchAll(urls: string[], fetchPage: FetchPage): Promise<string[]> {
  return Promise.all(urls.map((url) => fetchPage(url)));
}

export async function fetchOneByOne(urls: string[], fetchPage: FetchPage): Promise<string[]> {
  const pages: string[] = [];
  for (const url of urls) {
    pages.push(await fetchPage(url));
  }
  return pages;
}
