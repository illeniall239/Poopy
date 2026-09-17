// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import java.util.HashSet;
import java.util.Set;

public class Solution {
    public static boolean hasDuplicate(int[] values) {
        Set<Integer> seen = new HashSet<>();
        for (int value : values) {
            if (!seen.add(value)) return true;
        }
        return false;
    }
}
