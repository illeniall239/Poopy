// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import java.util.function.Supplier;

public class Solution {
    public record Counter(Supplier<Integer> increment, Supplier<Integer> decrement, Supplier<Integer> reset, Supplier<Integer> value) {}

    public static Counter makeCounter() {
        return makeCounter(0, 1);
    }

    public static Counter makeCounter(int start) {
        return makeCounter(start, 1);
    }

    public static Counter makeCounter(int start, int step) {
        // A lambda can only capture effectively final variables, so the mutable count lives inside a one-element array.
        int[] count = { start };
        return new Counter(
            () -> count[0] += step,
            () -> count[0] -= step,
            () -> count[0] = start,
            () -> count[0]);
    }
}
