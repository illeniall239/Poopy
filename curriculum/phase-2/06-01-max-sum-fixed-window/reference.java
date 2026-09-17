// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
public class Solution {
    public static int maxSumFixedWindow(int[] values, int k) {
        if (values.length < k) return 0;
        int sum = 0;
        for (int i = 0; i < k; i++) sum += values[i];
        int best = sum;
        for (int i = k; i < values.length; i++) {
            sum += values[i] - values[i - k];
            if (sum > best) best = sum;
        }
        return best;
    }
}
