export class TrieNode {
  children: Map<string, TrieNode> = new Map();
  isEndOfWord = false;
}

export class WordDictionary {
  constructor() {
    throw new Error("Not implemented");
  }

  addWord(word: string): void {
    throw new Error("Not implemented");
  }

  /** True if some stored word matches query, where "." matches any single letter. */
  search(query: string): boolean {
    throw new Error("Not implemented");
  }
}
