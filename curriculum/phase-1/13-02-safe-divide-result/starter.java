import java.util.List;

public class Solution {
    /** A result that says whether the operation worked: Ok carries the value, Fail carries the error message. */
    public sealed interface Result permits Ok, Fail {}
    public record Ok(double value) implements Result {}
    public record Fail(String error) implements Result {}

    public record Pair(double a, double b) {}

    /** Ok(a / b); Fail("Inputs must be finite numbers") if either is NaN or infinite (checked first); Fail("Cannot divide by zero") if b is 0. Never throws. */
    public static Result safeDivide(double a, double b) {
        throw new UnsupportedOperationException("Not implemented");
    }

    /** Ok(sum of every pair's quotient) (0 for no pairs), or for the first failing pair Fail("Pair <position from 1>: <that pair's error>"). Never throws. */
    public static Result sumOfQuotients(List<Pair> pairs) {
        throw new UnsupportedOperationException("Not implemented");
    }
}
