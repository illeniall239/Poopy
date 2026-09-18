// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import java.util.Arrays;

public class Solution {
    public static int fewestRemovals(int[][] intervals) {
        int[][] byEnd = intervals.clone();
        Arrays.sort(byEnd, (a, b) -> Integer.compare(a[1], b[1]));
        int removed = 0;
        long lastEnd = Long.MIN_VALUE;
        for (int[] iv : byEnd) {
            if (iv[0] < lastEnd) removed++;
            else lastEnd = iv[1];
        }
        return removed;
    }
}
