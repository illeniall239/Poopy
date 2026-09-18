// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

public class Solution {
    public static <T> Optional<T> last(List<T> items) {
        return items.isEmpty() ? Optional.empty() : Optional.of(items.get(items.size() - 1));
    }

    public static <T> List<List<T>> chunk(List<T> items, int size) {
        if (size < 1) {
            throw new IllegalArgumentException("size must be at least 1, got " + size);
        }
        List<List<T>> groups = new ArrayList<>();
        for (int start = 0; start < items.size(); start += size) {
            groups.add(new ArrayList<>(items.subList(start, Math.min(start + size, items.size()))));
        }
        return groups;
    }
}
