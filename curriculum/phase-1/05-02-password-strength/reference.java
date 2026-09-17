// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
public class Solution {
    public record Strength(int score, String label) {}

    private static boolean isLower(char ch) {
        return ch >= 'a' && ch <= 'z';
    }

    private static boolean isUpper(char ch) {
        return ch >= 'A' && ch <= 'Z';
    }

    private static boolean isDigit(char ch) {
        return ch >= '0' && ch <= '9';
    }

    public static boolean hasLowercase(String password) {
        for (char ch : password.toCharArray()) {
            if (isLower(ch)) return true;
        }
        return false;
    }

    public static boolean hasUppercase(String password) {
        for (char ch : password.toCharArray()) {
            if (isUpper(ch)) return true;
        }
        return false;
    }

    public static boolean hasDigit(String password) {
        for (char ch : password.toCharArray()) {
            if (isDigit(ch)) return true;
        }
        return false;
    }

    public static boolean hasSymbol(String password) {
        for (char ch : password.toCharArray()) {
            if (!isLower(ch) && !isUpper(ch) && !isDigit(ch)) return true;
        }
        return false;
    }

    public static Strength passwordStrength(String password) {
        int score = 0;
        if (password.length() >= 8) score++;
        if (password.length() >= 12) score++;
        if (hasLowercase(password)) score++;
        if (hasUppercase(password)) score++;
        if (hasDigit(password)) score++;
        if (hasSymbol(password)) score++;

        if (score >= 5) return new Strength(score, "strong");
        if (score >= 3) return new Strength(score, "medium");
        return new Strength(score, "weak");
    }
}
