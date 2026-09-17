// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
public class Solution {
    public static int daysToEscape(int depth, int climb, int slide) {
        if (climb >= depth) return 1;
        if (climb <= slide) return -1;
        // Before the last day the snail must reach depth - climb; each full day gains climb - slide.
        return (int) Math.ceil((double) (depth - climb) / (climb - slide)) + 1;
    }
}
