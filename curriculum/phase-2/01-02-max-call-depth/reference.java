// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class Solution {
    public static int maxCallDepth(Map<String, List<String>> calls, String entry) {
        return depthFrom(entry, calls, new HashMap<>(), new HashSet<>());
    }

    private static int depthFrom(String fn, Map<String, List<String>> calls, Map<String, Integer> finished, Set<String> onStack) {
        Integer known = finished.get(fn);
        if (known != null) return known;
        if (!onStack.add(fn)) return -1;
        int deepest = 0;
        for (String callee : calls.getOrDefault(fn, List.of())) {
            int depth = depthFrom(callee, calls, finished, onStack);
            if (depth == -1) return -1;
            deepest = Math.max(deepest, depth);
        }
        onStack.remove(fn);
        finished.put(fn, deepest + 1);
        return deepest + 1;
    }
}
