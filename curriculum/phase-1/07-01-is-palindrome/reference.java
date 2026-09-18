// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
public class Solution {
    public static boolean isPalindrome(String text) {
        StringBuilder letters = new StringBuilder();
        for (char ch : text.toLowerCase().toCharArray()) {
            if (ch >= 'a' && ch <= 'z') letters.append(ch);
        }
        for (int i = 0, j = letters.length() - 1; i < j; i++, j--) {
            if (letters.charAt(i) != letters.charAt(j)) return false;
        }
        return true;
    }
}
