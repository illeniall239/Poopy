export class ListNode {
  val: number;
  next: ListNode | null;

  constructor(val: number, next: ListNode | null = null) {
    this.val = val;
    this.next = next;
  }
}

export function middleNode(head: ListNode | null): ListNode | null {
  throw new Error("Not implemented");
}

export function hasCycle(head: ListNode | null): boolean {
  throw new Error("Not implemented");
}
