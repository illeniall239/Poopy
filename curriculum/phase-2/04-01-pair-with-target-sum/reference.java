// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import java.util.HashMap;
import java.util.Map;

public class Solution {
    public static int[] pairWithTargetSum(int[] values, long target) {
        Map<Long, Integer> firstIndexOf = new HashMap<>();
        for (int j = 0; j < values.length; j++) {
            Integer i = firstIndexOf.get(target - values[j]);
            if (i != null) return new int[] { i, j };
            firstIndexOf.putIfAbsent((long) values[j], j);
        }
        return new int[] { -1, -1 };
    }
}
