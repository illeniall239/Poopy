// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export class TrieNode {
  children: Map<string, TrieNode> = new Map();
  isEndOfWord = false;
}

export class Autocomplete {
  root: TrieNode;

  constructor(words: string[]) {
    this.root = new TrieNode();
    for (const word of words) {
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
  }

  suggest(prefix: string, n: number): string[] {
    let node = this.root;
    for (const ch of prefix) {
      const next = node.children.get(ch);
      if (next === undefined) return [];
      node = next;
    }
    const out: string[] = [];
    const collect = (cur: TrieNode, path: string): void => {
      if (out.length >= n) return;
      if (cur.isEndOfWord) out.push(path);
      for (const ch of [...cur.children.keys()].sort()) {
        if (out.length >= n) return;
        collect(cur.children.get(ch)!, path + ch);
      }
    };
    collect(node, prefix);
    return out;
  }
}
