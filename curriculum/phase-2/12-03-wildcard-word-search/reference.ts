// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export class TrieNode {
  children: Map<string, TrieNode> = new Map();
  isEndOfWord = false;
}

export class WordDictionary {
  root: TrieNode;

  constructor() {
    this.root = new TrieNode();
  }

  addWord(word: string): void {
    let node = this.root;
    for (const ch of word) {
      let next = node.children.get(ch);
      if (next === undefined) {
        next = new TrieNode();
        node.children.set(ch, next);
      }
      node = next;
    }
    node.isEndOfWord = true;
  }

  search(query: string): boolean {
    const matches = (node: TrieNode, i: number): boolean => {
      if (i === query.length) return node.isEndOfWord;
      const ch = query[i];
      if (ch !== ".") {
        const next = node.children.get(ch);
        return next !== undefined && matches(next, i + 1);
      }
      for (const child of node.children.values()) {
        if (matches(child, i + 1)) return true;
      }
      return false;
    };
    return matches(this.root, 0);
  }
}
