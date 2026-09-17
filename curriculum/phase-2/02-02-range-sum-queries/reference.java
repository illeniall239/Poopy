// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
public class Solution {
    public static long[] rangeSums(int[] values, int[][] queries) {
        // prefix[k] is the sum of the first k values.
        long[] prefix = new long[values.length + 1];
        for (int k = 0; k < values.length; k++) prefix[k + 1] = prefix[k] + values[k];
        long[] sums = new long[queries.length];
        for (int q = 0; q < queries.length; q++) sums[q] = prefix[queries[q][1] + 1] - prefix[queries[q][0]];
        return sums;
    }
}
