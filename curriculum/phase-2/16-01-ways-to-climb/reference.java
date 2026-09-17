// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
public class Solution {
    public static long climbWays(int n) {
        long twoBelow = 1, oneBelow = 1;
        for (int i = 2; i <= n; i++) {
            long current = oneBelow + twoBelow;
            twoBelow = oneBelow;
            oneBelow = current;
        }
        return oneBelow;
    }
}
