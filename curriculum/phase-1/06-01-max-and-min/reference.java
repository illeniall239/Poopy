// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
public class Solution {
    public record MaxMin(double max, double min) {}

    public static MaxMin maxAndMin(double[] nums) {
        if (nums.length == 0) return null;
        double max = nums[0];
        double min = nums[0];
        for (double n : nums) {
            if (n > max) max = n;
            if (n < min) min = n;
        }
        return new MaxMin(max, min);
    }
}
