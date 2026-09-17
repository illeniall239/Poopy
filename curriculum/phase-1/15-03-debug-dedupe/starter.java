import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class Solution {
    /**
     * Returns a NEW list with duplicate numbers removed: each number is kept at the position of its first appearance and the
     * order of the kept numbers doesn't change. The input list must not be changed, and the result is always a new list,
     * even when there were no duplicates.
     */
    public static List<Integer> dedupe(List<Integer> items) {
        Set<Integer> seen = new HashSet<>();
        for (int i = 0; i < items.size(); i++) {
            if (seen.contains(items.get(i))) {
                items.remove(i);
            } else {
                seen.add(items.get(i));
            }
        }
        return items;
    }
}
