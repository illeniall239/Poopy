// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export class ListNode {
  val: number;
  next: ListNode | null;

  constructor(val: number, next: ListNode | null = null) {
    this.val = val;
    this.next = next;
  }
}

export function middleNode(head: ListNode | null): ListNode | null {
  let slow = head;
  let fast = head;
  while (fast !== null && fast.next !== null) {
    slow = (slow as ListNode).next;
    fast = fast.next.next;
  }
  return slow;
}

export function hasCycle(head: ListNode | null): boolean {
  let slow = head;
  let fast = head;
  while (fast !== null && fast.next !== null) {
    slow = (slow as ListNode).next;
    fast = fast.next.next;
    if (slow === fast) return true;
  }
  return false;
}
