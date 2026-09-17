// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;

public class Solution {
    public static List<String> permutations(String s) {
        if (s.isEmpty()) return List.of("");
        Set<String> results = new TreeSet<>();
        for (int i = 0; i < s.length(); i++) {
            String rest = s.substring(0, i) + s.substring(i + 1);
            for (String tail : permutations(rest)) results.add(s.charAt(i) + tail);
        }
        return new ArrayList<>(results);
    }
}
