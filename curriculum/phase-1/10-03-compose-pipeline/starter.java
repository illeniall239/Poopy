import java.util.List;
import java.util.function.IntPredicate;
import java.util.function.IntUnaryOperator;

public class Solution {
    /** One step that runs the steps left to right (each runs exactly once per call); no steps gives back the input. Changing the list afterwards must not affect it. */
    public static IntUnaryOperator pipeline(List<IntUnaryOperator> steps) {
        throw new UnsupportedOperationException("Not implemented");
    }

    /** A step that runs step only if predicate holds for the input, and otherwise returns the input unchanged. */
    public static IntUnaryOperator when(IntPredicate predicate, IntUnaryOperator step) {
        throw new UnsupportedOperationException("Not implemented");
    }
}
