// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
public class Solution {
    public static double power(double base, int exp) {
        if (exp == 0) return 1;
        double half = power(base, exp / 2);
        return exp % 2 == 0 ? half * half : half * half * base;
    }
}
