// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import java.util.ArrayDeque;

public class Solution {
    public static boolean isBalanced(String s) {
        ArrayDeque<Character> stack = new ArrayDeque<>();
        for (char ch : s.toCharArray()) {
            if (ch == '(' || ch == '[' || ch == '{') {
                stack.push(ch);
            } else if (ch == ')' || ch == ']' || ch == '}') {
                char opener = ch == ')' ? '(' : ch == ']' ? '[' : '{';
                if (stack.isEmpty() || stack.pop() != opener) return false;
            }
        }
        return stack.isEmpty();
    }
}
