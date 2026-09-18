// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import java.util.List;
import java.util.function.IntPredicate;
import java.util.function.IntUnaryOperator;

public class Solution {
    public static IntUnaryOperator pipeline(List<IntUnaryOperator> steps) {
        return steps.stream().reduce(IntUnaryOperator.identity(), IntUnaryOperator::andThen);
    }

    public static IntUnaryOperator when(IntPredicate predicate, IntUnaryOperator step) {
        return n -> predicate.test(n) ? step.applyAsInt(n) : n;
    }
}
