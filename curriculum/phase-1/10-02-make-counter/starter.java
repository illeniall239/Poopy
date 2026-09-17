import java.util.function.Supplier;

public class Solution {
    /** Four functions that share one private count; each returns the count after the call. */
    public record Counter(Supplier<Integer> increment, Supplier<Integer> decrement, Supplier<Integer> reset, Supplier<Integer> value) {}

    /** A counter starting at 0 with step 1. */
    public static Counter makeCounter() {
        return makeCounter(0, 1);
    }

    /** A counter starting at start with step 1. */
    public static Counter makeCounter(int start) {
        return makeCounter(start, 1);
    }

    /** A new, independent counter: increment adds step, decrement subtracts step, reset goes back to start, value reads without changing. */
    public static Counter makeCounter(int start, int step) {
        throw new UnsupportedOperationException("Not implemented");
    }
}
