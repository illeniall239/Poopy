// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
public class Solution {
    public static Integer secondLargest(int[] nums) {
        long largest = Long.MIN_VALUE;
        long second = Long.MIN_VALUE;
        for (int n : nums) {
            if (n > largest) {
                second = largest;
                largest = n;
            } else if (n < largest && n > second) {
                second = n;
            }
        }
        return second == Long.MIN_VALUE ? null : (int) second;
    }
}
