public class Solution {
    /** score 0-6 and label "weak" (0-2), "medium" (3-4) or "strong" (5-6). */
    public record Strength(int score, String label) {}

    /** True if password contains at least one letter a-z. */
    public static boolean hasLowercase(String password) {
        throw new UnsupportedOperationException("Not implemented");
    }

    /** True if password contains at least one letter A-Z. */
    public static boolean hasUppercase(String password) {
        throw new UnsupportedOperationException("Not implemented");
    }

    /** True if password contains at least one digit 0-9. */
    public static boolean hasDigit(String password) {
        throw new UnsupportedOperationException("Not implemented");
    }

    /** True if password contains at least one character that is not a-z, A-Z or 0-9 (spaces count). */
    public static boolean hasSymbol(String password) {
        throw new UnsupportedOperationException("Not implemented");
    }

    /** One point each for: length >= 8, length >= 12, hasLowercase, hasUppercase, hasDigit, hasSymbol. */
    public static Strength passwordStrength(String password) {
        throw new UnsupportedOperationException("Not implemented");
    }
}
