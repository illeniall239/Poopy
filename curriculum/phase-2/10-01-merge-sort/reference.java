// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import java.util.Arrays;

public class Solution {
    public static int[] mergeSort(int[] nums) {
        if (nums.length <= 1) return nums.clone();
        int mid = nums.length / 2;
        int[] left = mergeSort(Arrays.copyOfRange(nums, 0, mid));
        int[] right = mergeSort(Arrays.copyOfRange(nums, mid, nums.length));
        int[] merged = new int[nums.length];
        int i = 0, j = 0, k = 0;
        while (i < left.length && j < right.length) merged[k++] = left[i] <= right[j] ? left[i++] : right[j++];
        while (i < left.length) merged[k++] = left[i++];
        while (j < right.length) merged[k++] = right[j++];
        return merged;
    }
}
