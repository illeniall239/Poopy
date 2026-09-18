// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
type CacheNode = { key: number; value: number; prev: CacheNode | null; next: CacheNode | null };

export class LRUCache {
  private capacity: number;
  private nodes = new Map<number, CacheNode>();
  // Sentinels: head.next is the most recently used, tail.prev the least.
  private head: CacheNode = { key: -1, value: -1, prev: null, next: null };
  private tail: CacheNode = { key: -1, value: -1, prev: null, next: null };

  constructor(capacity: number) {
    this.capacity = capacity;
    this.head.next = this.tail;
    this.tail.prev = this.head;
  }

  get(key: number): number {
    const node = this.nodes.get(key);
    if (node === undefined) return -1;
    this.unlink(node);
    this.pushFront(node);
    return node.value;
  }

  put(key: number, value: number): void {
    const existing = this.nodes.get(key);
    if (existing !== undefined) {
      existing.value = value;
      this.unlink(existing);
      this.pushFront(existing);
      return;
    }
    if (this.nodes.size === this.capacity) {
      const oldest = this.tail.prev as CacheNode;
      this.unlink(oldest);
      this.nodes.delete(oldest.key);
    }
    const node: CacheNode = { key, value, prev: null, next: null };
    this.nodes.set(key, node);
    this.pushFront(node);
  }

  private unlink(node: CacheNode): void {
    (node.prev as CacheNode).next = node.next;
    (node.next as CacheNode).prev = node.prev;
  }

  private pushFront(node: CacheNode): void {
    node.prev = this.head;
    node.next = this.head.next;
    (this.head.next as CacheNode).prev = node;
    this.head.next = node;
  }
}
