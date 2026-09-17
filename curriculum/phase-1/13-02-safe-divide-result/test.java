import java.util.List;
import java.util.Objects;
import java.util.function.Supplier;

public class SolutionTest {
    static int passed = 0, failed = 0;

    static void check(String name, Supplier<Object> got, Object expected) {
        Object value;
        try {
            value = got.get();
        } catch (Throwable t) {
            failed++;
            System.out.println("FAIL - " + name + "\n    threw:    " + t);
            return;
        }
        if (Objects.deepEquals(value, expected)) {
            passed++;
            System.out.println("ok - " + name);
        } else {
            failed++;
            System.out.println("FAIL - " + name + "\n    expected: " + expected + "\n    got:      " + value);
        }
    }

    static Solution.Ok ok(double value) {
        return new Solution.Ok(value);
    }

    static Solution.Fail fail(String error) {
        return new Solution.Fail(error);
    }

    static Solution.Pair pair(double a, double b) {
        return new Solution.Pair(a, b);
    }

    public static void main(String[] args) {
        check("divides normally",
            () -> List.of(Solution.safeDivide(10, 4), Solution.safeDivide(0, 5), Solution.safeDivide(-9, 3)),
            List.of(ok(2.5), ok(0), ok(-3)));
        check("dividing by zero is a failure, not Infinity",
            () -> List.of(Solution.safeDivide(1, 0), Solution.safeDivide(0, 0)),
            List.of(fail("Cannot divide by zero"), fail("Cannot divide by zero")));
        check("non-finite inputs are a failure",
            () -> List.of(
                Solution.safeDivide(Double.NaN, 2),
                Solution.safeDivide(1, Double.POSITIVE_INFINITY),
                Solution.safeDivide(Double.NEGATIVE_INFINITY, 1)),
            List.of(fail("Inputs must be finite numbers"), fail("Inputs must be finite numbers"), fail("Inputs must be finite numbers")));
        check("the finite check comes before the zero check", () -> Solution.safeDivide(Double.NaN, 0), fail("Inputs must be finite numbers"));
        check("sums the quotients of all pairs", () -> Solution.sumOfQuotients(List.of(pair(10, 2), pair(9, 3))), ok(8));
        check("no pairs sums to 0", () -> Solution.sumOfQuotients(List.of()), ok(0));
        check("reports the first failing pair with its position",
            () -> List.of(
                Solution.sumOfQuotients(List.of(pair(1, 1), pair(5, 0), pair(Double.NaN, 1))),
                Solution.sumOfQuotients(List.of(pair(Double.POSITIVE_INFINITY, 1)))),
            List.of(fail("Pair 2: Cannot divide by zero"), fail("Pair 1: Inputs must be finite numbers")));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
