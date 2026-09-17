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
        check("sequence from 6", () -> Solution.collatzSteps(6), new Solution.CollatzResult(8, 16));
        check("1 needs no steps and its peak is itself", () -> Solution.collatzSteps(1), new Solution.CollatzResult(0, 1));
        check("2 needs exactly one step", () -> Solution.collatzSteps(2), new Solution.CollatzResult(1, 2));
        check("the starting number can be the peak", () -> Solution.collatzSteps(16), new Solution.CollatzResult(4, 16));
        check("odd start climbs before falling", () -> Solution.collatzSteps(7), new Solution.CollatzResult(16, 52));
        check("27 takes a long path", () -> Solution.collatzSteps(27), new Solution.CollatzResult(111, 9232));
        check("large start", () -> Solution.collatzSteps(837799), new Solution.CollatzResult(524, 2974984576L));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
