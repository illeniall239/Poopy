// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Solution {
    public static List<List<Integer>> zeroSumTriplets(int[] values) {
        int[] sorted = values.clone();
        Arrays.sort(sorted);
        List<List<Integer>> result = new ArrayList<>();
        for (int i = 0; i + 2 < sorted.length; i++) {
            if (i > 0 && sorted[i] == sorted[i - 1]) continue;
            int lo = i + 1, hi = sorted.length - 1;
            while (lo < hi) {
                int sum = sorted[i] + sorted[lo] + sorted[hi];
                if (sum < 0) lo++;
                else if (sum > 0) hi--;
                else {
                    result.add(List.of(sorted[i], sorted[lo], sorted[hi]));
                    lo++;
                    while (lo < hi && sorted[lo] == sorted[lo - 1]) lo++;
                    hi--;
                }
            }
        }
        return result;
    }
}
