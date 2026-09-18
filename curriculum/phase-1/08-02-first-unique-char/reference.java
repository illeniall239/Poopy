// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import java.util.HashMap;
import java.util.Map;

public class Solution {
    public static int firstUniqueIndex(String text) {
        Map<Character, Integer> counts = new HashMap<>();
        for (char ch : text.toCharArray()) {
            Integer current = counts.get(ch);
            counts.put(ch, current == null ? 1 : current + 1);
        }
        for (int i = 0; i < text.length(); i++) {
            if (counts.get(text.charAt(i)) == 1) return i;
        }
        return -1;
    }
}
