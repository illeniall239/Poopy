// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
public class Solution {
    public static int minShredSpeed(int[] stacks, int h) {
        int lo = 1, hi = 1;
        for (int p : stacks) hi = Math.max(hi, p);
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            long hours = 0;
            for (int p : stacks) hours += (p + (long) mid - 1) / mid;
            if (hours <= h) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }
}
