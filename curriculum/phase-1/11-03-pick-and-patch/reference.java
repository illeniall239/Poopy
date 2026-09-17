// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class Solution {
    public static <V> Map<String, V> pick(Map<String, V> obj, List<String> keys) {
        Map<String, V> result = new LinkedHashMap<>();
        for (String key : keys) {
            if (obj.containsKey(key)) result.put(key, obj.get(key));
        }
        return result;
    }

    public static <V> Map<String, V> applyPatch(Map<String, V> original, Map<String, V> patch) {
        Map<String, V> result = new LinkedHashMap<>(original);
        patch.forEach((key, value) -> {
            if (value != null) result.put(key, value);
        });
        return result;
    }
}
