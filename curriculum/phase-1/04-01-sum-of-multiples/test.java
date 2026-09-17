import java.util.Arrays;
import java.util.Objects;
import java.util.function.Supplier;

public class SolutionTest {
    static int passed = 0, failed = 0;

    static void check(String name, Supplier<Object> got, Object expected) {
        Object actual;
        try {
            actual = got.get();
        } catch (Throwable t) {
            failed++;
            System.out.println("FAIL - " + name + "\n    threw: " + t);
            return;
        }
        if (Objects.deepEquals(actual, expected)) {
            passed++;
            System.out.println("ok - " + name);
        } else {
            failed++;
            System.out.println("FAIL - " + name + "\n    expected: " + show(expected) + "\n    got:      " + show(actual));
        }
    }

    static String show(Object o) {
        if (o instanceof double[]) return Arrays.toString((double[]) o);
        if (o instanceof int[]) return Arrays.toString((int[]) o);
        if (o instanceof Object[]) return Arrays.deepToString((Object[]) o);
        return String.valueOf(o);
    }

    public static void main(String[] args) {
        check("multiples below 10", () -> Solution.sumOfMultiples(10), 23);
        check("15 is counted once, not twice", () -> Solution.sumOfMultiples(16), 60);
        check("n itself is not included (3)", () -> Solution.sumOfMultiples(3), 0);
        check("n itself is not included (15)", () -> Solution.sumOfMultiples(15), 45);
        check("the first multiple just below n is included", () -> Solution.sumOfMultiples(4), 3);
        check("zero gives zero", () -> Solution.sumOfMultiples(0), 0);
        check("one gives zero", () -> Solution.sumOfMultiples(1), 0);
        check("larger n", () -> Solution.sumOfMultiples(1000), 233168);
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
