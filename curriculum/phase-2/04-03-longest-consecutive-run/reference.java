// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import java.util.HashSet;
import java.util.Set;

public class Solution {
    public static int longestConsecutiveRun(int[] values) {
        Set<Integer> present = new HashSet<>();
        for (int v : values) present.add(v);
        int best = 0;
        for (int start : present) {
            if (present.contains(start - 1)) continue;
            int length = 1;
            while (present.contains(start + length)) length++;
            best = Math.max(best, length);
        }
        return best;
    }
}
