export class TrieNode {
  children: Map<string, TrieNode> = new Map();
  isEndOfWord = false;
}

export class Autocomplete {
  constructor(words: string[]) {
    throw new Error("Not implemented");
  }

  /** The first n stored words in alphabetical order that begin with prefix. */
  suggest(prefix: string, n: number): string[] {
    throw new Error("Not implemented");
  }
}
