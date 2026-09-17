// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
const OPENER_OF: Record<string, string> = { ")": "(", "]": "[", "}": "{" };

export function isBalanced(s: string): boolean {
  const stack: string[] = [];
  for (const ch of s) {
    if (ch === "(" || ch === "[" || ch === "{") stack.push(ch);
    else if (ch in OPENER_OF) {
      if (stack.length === 0 || stack.pop() !== OPENER_OF[ch]) return false;
    }
  }
  return stack.length === 0;
}
