// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import java.util.ArrayList;
import java.util.List;

public class Solution {
    public static List<Integer> flatten(List<?> items) {
        List<Integer> result = new ArrayList<>();
        for (Object item : items) {
            if (item instanceof List<?> inner) result.addAll(flatten(inner));
            else result.add((Integer) item);
        }
        return result;
    }

    public static int depth(List<?> items) {
        int deepestInner = 0;
        for (Object item : items) {
            if (item instanceof List<?> inner) deepestInner = Math.max(deepestInner, depth(inner));
        }
        return 1 + deepestInner;
    }
}
