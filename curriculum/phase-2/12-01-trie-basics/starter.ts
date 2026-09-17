export class TrieNode {
  children: Map<string, TrieNode> = new Map();
  isEndOfWord = false;
}

export class Trie {
  constructor() {
    throw new Error("Not implemented");
  }

  insert(word: string): void {
    throw new Error("Not implemented");
  }

  search(word: string): boolean {
    throw new Error("Not implemented");
  }

  startsWith(prefix: string): boolean {
    throw new Error("Not implemented");
  }
}
