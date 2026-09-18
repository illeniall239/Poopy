// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
public class Solution {
    public static boolean canReachLastIndex(int[] jumps) {
        int farthest = 0;
        for (int i = 0; i <= farthest && i < jumps.length; i++) {
            farthest = Math.max(farthest, i + jumps[i]);
        }
        return farthest >= jumps.length - 1;
    }
}
