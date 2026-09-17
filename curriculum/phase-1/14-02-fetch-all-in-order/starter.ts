export type FetchPage = (url: string) => Promise<string>;

export async function fetchAll(urls: string[], fetchPage: FetchPage): Promise<string[]> {
  throw new Error("Not implemented");
}

export async function fetchOneByOne(urls: string[], fetchPage: FetchPage): Promise<string[]> {
  throw new Error("Not implemented");
}
