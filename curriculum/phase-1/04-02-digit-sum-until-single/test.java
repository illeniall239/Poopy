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
        check("one pass is enough", () -> Solution.digitSumUntilSingle(16), 7);
        check("needs several passes", () -> Solution.digitSumUntilSingle(493193), 2);
        check("10 is two digits and becomes 1", () -> Solution.digitSumUntilSingle(10), 1);
        check("a single digit is returned unchanged (0)", () -> Solution.digitSumUntilSingle(0), 0);
        check("a single digit is returned unchanged (9)", () -> Solution.digitSumUntilSingle(9), 9);
        check("sum that lands exactly on 10", () -> Solution.digitSumUntilSingle(19), 1);
        check("zeros inside the number", () -> Solution.digitSumUntilSingle(1000000), 1);
        check("largest safe integer", () -> Solution.digitSumUntilSingle(9007199254740991L), 4);
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
