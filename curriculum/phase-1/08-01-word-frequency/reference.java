// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import java.util.LinkedHashMap;
import java.util.Map;

public class Solution {
    public static Map<String, Integer> wordFrequency(String text) {
        Map<String, Integer> counts = new LinkedHashMap<>();
        StringBuilder word = new StringBuilder();
        for (char ch : (text.toLowerCase() + " ").toCharArray()) {
            if (ch >= 'a' && ch <= 'z') {
                word.append(ch);
            } else if (word.length() > 0) {
                Integer current = counts.get(word.toString());
                counts.put(word.toString(), current == null ? 1 : current + 1);
                word.setLength(0);
            }
        }
        return counts;
    }
}
