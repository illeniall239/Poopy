// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import java.util.concurrent.ThreadLocalRandom;

public class Solution {
    public static void quickSort(int[] nums) {
        sortRange(nums, 0, nums.length - 1);
    }

    private static void sortRange(int[] nums, int lo, int hi) {
        while (lo < hi) {
            int pivot = nums[ThreadLocalRandom.current().nextInt(lo, hi + 1)];
            // Three regions: [lo, lt) < pivot, [lt, i) == pivot, (gt, hi] > pivot.
            int lt = lo, i = lo, gt = hi;
            while (i <= gt) {
                if (nums[i] < pivot) swap(nums, i++, lt++);
                else if (nums[i] > pivot) swap(nums, i, gt--);
                else i++;
            }
            // Recurse into the smaller side and loop on the larger one to keep the stack O(log n).
            if (lt - lo < hi - gt) {
                sortRange(nums, lo, lt - 1);
                lo = gt + 1;
            } else {
                sortRange(nums, gt + 1, hi);
                hi = lt - 1;
            }
        }
    }

    private static void swap(int[] nums, int a, int b) {
        int t = nums[a];
        nums[a] = nums[b];
        nums[b] = t;
    }
}
