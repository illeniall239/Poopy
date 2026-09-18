// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
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
