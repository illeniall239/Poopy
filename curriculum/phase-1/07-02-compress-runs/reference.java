// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
public class Solution {
    public static String compressRuns(String text) {
        StringBuilder result = new StringBuilder();
        int i = 0;
        while (i < text.length()) {
            char ch = text.charAt(i);
            int count = 0;
            while (i < text.length() && text.charAt(i) == ch) {
                count++;
                i++;
            }
            result.append(ch);
            if (count > 1) result.append(count);
        }
        return result.toString();
    }
}
