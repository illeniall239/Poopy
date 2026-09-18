// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import java.util.HashMap;
import java.util.Map;

public class Solution {
    public static String smallestCoveringWindow(String s, String t) {
        if (t.isEmpty() || s.length() < t.length()) return "";
        Map<Character, Integer> need = new HashMap<>();
        for (int i = 0; i < t.length(); i++) need.merge(t.charAt(i), 1, Integer::sum);
        int missing = need.size();
        Map<Character, Integer> have = new HashMap<>();
        int bestStart = 0, bestLength = Integer.MAX_VALUE, left = 0;
        for (int right = 0; right < s.length(); right++) {
            char ch = s.charAt(right);
            if (!need.containsKey(ch)) continue;
            int count = have.merge(ch, 1, Integer::sum);
            if (count == need.get(ch)) missing--;
            while (missing == 0) {
                if (right - left + 1 < bestLength) {
                    bestStart = left;
                    bestLength = right - left + 1;
                }
                char out = s.charAt(left++);
                if (need.containsKey(out)) {
                    int remaining = have.merge(out, -1, Integer::sum);
                    if (remaining < need.get(out)) missing++;
                }
            }
        }
        return bestLength == Integer.MAX_VALUE ? "" : s.substring(bestStart, bestStart + bestLength);
    }
}
