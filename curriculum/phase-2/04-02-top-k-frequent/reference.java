// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class Solution {
    public static List<Integer> topKFrequent(int[] values, int k) {
        Map<Integer, Integer> counts = new LinkedHashMap<>();
        for (int value : values) counts.merge(value, 1, Integer::sum);

        // byCount.get(c) holds the values seen exactly c times, in first-appearance order.
        List<List<Integer>> byCount = new ArrayList<>(values.length + 1);
        for (int c = 0; c <= values.length; c++) byCount.add(new ArrayList<>());
        for (Map.Entry<Integer, Integer> entry : counts.entrySet()) byCount.get(entry.getValue()).add(entry.getKey());

        List<Integer> result = new ArrayList<>(k);
        for (int count = values.length; count >= 1; count--) {
            for (int value : byCount.get(count)) {
                if (result.size() == k) return result;
                result.add(value);
            }
        }
        return result;
    }
}
