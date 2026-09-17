// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import java.util.ArrayList;
import java.util.List;

public class Solution {
    public static List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        explore(nums, 0, new ArrayList<>(), result);
        return result;
    }

    private static void explore(int[] nums, int i, List<Integer> path, List<List<Integer>> result) {
        if (i == nums.length) {
            result.add(new ArrayList<>(path));
            return;
        }
        path.add(nums[i]);
        explore(nums, i + 1, path, result);
        path.remove(path.size() - 1);
        explore(nums, i + 1, path, result);
    }
}
