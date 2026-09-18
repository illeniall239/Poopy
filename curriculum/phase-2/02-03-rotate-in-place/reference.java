// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
public class Solution {
    public static void rotateRight(int[] values, int k) {
        int n = values.length;
        if (n == 0) return;
        int steps = k % n;
        reverse(values, 0, n - 1);
        reverse(values, 0, steps - 1);
        reverse(values, steps, n - 1);
    }

    private static void reverse(int[] values, int from, int to) {
        while (from < to) {
            int temp = values[from];
            values[from++] = values[to];
            values[to--] = temp;
        }
    }
}
