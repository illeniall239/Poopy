// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
public class Solution {
    public record CollatzResult(int steps, long peak) {}

    public static CollatzResult collatzSteps(int n) {
        long current = n;
        int steps = 0;
        long peak = current;
        while (current != 1) {
            current = current % 2 == 0 ? current / 2 : 3 * current + 1;
            steps++;
            if (current > peak) peak = current;
        }
        return new CollatzResult(steps, peak);
    }
}
