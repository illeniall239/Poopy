// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
public class Solution {
    public static long widestContainer(int[] heights) {
        int lo = 0, hi = heights.length - 1;
        long best = 0;
        while (lo < hi) {
            long area = (long) (hi - lo) * Math.min(heights[lo], heights[hi]);
            if (area > best) best = area;
            if (heights[lo] < heights[hi]) lo++;
            else hi--;
        }
        return best;
    }
}
