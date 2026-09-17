// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
public class Solution {
    public static int[] sortedPairSum(int[] values, long target) {
        int lo = 0, hi = values.length - 1;
        while (lo < hi) {
            long sum = (long) values[lo] + values[hi];
            if (sum == target) return new int[] { values[lo], values[hi] };
            if (sum < target) lo++;
            else hi--;
        }
        return null;
    }
}
