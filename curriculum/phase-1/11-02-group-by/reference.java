// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;

public class Solution {
    public static <T> Map<String, List<T>> groupBy(List<T> items, Function<T, String> keyOf) {
        Map<String, List<T>> groups = new LinkedHashMap<>();
        for (T item : items) {
            groups.computeIfAbsent(keyOf.apply(item), key -> new ArrayList<>()).add(item);
        }
        return groups;
    }
}
