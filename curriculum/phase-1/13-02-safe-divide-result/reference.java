// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import java.util.List;

public class Solution {
    public sealed interface Result permits Ok, Fail {}
    public record Ok(double value) implements Result {}
    public record Fail(String error) implements Result {}

    public record Pair(double a, double b) {}

    public static Result safeDivide(double a, double b) {
        if (!Double.isFinite(a) || !Double.isFinite(b)) return new Fail("Inputs must be finite numbers");
        if (b == 0) return new Fail("Cannot divide by zero");
        return new Ok(a / b);
    }

    public static Result sumOfQuotients(List<Pair> pairs) {
        double sum = 0;
        for (int i = 0; i < pairs.size(); i++) {
            Result result = safeDivide(pairs.get(i).a(), pairs.get(i).b());
            if (result instanceof Fail fail) return new Fail("Pair " + (i + 1) + ": " + fail.error());
            if (result instanceof Ok ok) sum += ok.value();
        }
        return new Ok(sum);
    }
}
