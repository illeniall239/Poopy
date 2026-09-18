// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
public class Solution {
    public static double[] runningAverages(double[] nums) {
        double[] result = new double[nums.length];
        double sum = 0;
        for (int i = 0; i < nums.length; i++) {
            sum += nums[i];
            result[i] = sum / (i + 1);
        }
        return result;
    }
}
