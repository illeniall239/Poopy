// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class Solution {
    public static List<Integer> dedupe(List<Integer> items) {
        Set<Integer> seen = new HashSet<>();
        List<Integer> result = new ArrayList<>();
        for (int i = 0; i < items.size(); i++) {
            if (!seen.contains(items.get(i))) {
                seen.add(items.get(i));
                result.add(items.get(i));
            }
        }
        return result;
    }
}
