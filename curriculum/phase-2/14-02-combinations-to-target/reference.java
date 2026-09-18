// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Solution {
    public static List<List<Integer>> combinationsToTarget(int[] candidates, int target) {
        int[] sorted = candidates.clone();
        Arrays.sort(sorted);
        List<List<Integer>> result = new ArrayList<>();
        explore(sorted, 0, target, new ArrayList<>(), result);
        return result;
    }

    private static void explore(int[] sorted, int start, int remaining, List<Integer> path, List<List<Integer>> result) {
        if (remaining == 0) {
            result.add(new ArrayList<>(path));
            return;
        }
        for (int i = start; i < sorted.length && sorted[i] <= remaining; i++) {
            path.add(sorted[i]);
            explore(sorted, i, remaining - sorted[i], path, result);
            path.remove(path.size() - 1);
        }
    }
}
