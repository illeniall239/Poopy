// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
public class Solution {
    private static final String ALPHABET = "abcdefghijklmnopqrstuvwxyz";

    public static String caesarShift(String text, int shift) {
        StringBuilder result = new StringBuilder();
        for (char ch : text.toCharArray()) {
            char lower = Character.toLowerCase(ch);
            int index = ALPHABET.indexOf(lower);
            if (index == -1) {
                result.append(ch);
                continue;
            }
            char shifted = ALPHABET.charAt(((index + shift) % 26 + 26) % 26);
            result.append(ch == lower ? shifted : Character.toUpperCase(shifted));
        }
        return result.toString();
    }
}
