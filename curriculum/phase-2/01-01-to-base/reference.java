// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
public class Solution {
    private static final String DIGITS = "0123456789abcdef";

    public static String toBase(int n, int base) {
        if (n == 0) return "0";
        StringBuilder digits = new StringBuilder();
        while (n > 0) {
            digits.append(DIGITS.charAt(n % base));
            n /= base;
        }
        return digits.reverse().toString();
    }

    public static int fromBase(String text, int base) {
        int value = 0;
        for (char ch : text.toCharArray()) value = value * base + DIGITS.indexOf(ch);
        return value;
    }
}
