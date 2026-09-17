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
        check("leftover cent goes to one person", () -> Solution.splitBill(10, 3), new Solution.Split(333, 1));
        check("even split has no extra cents", () -> Solution.splitBill(12, 4), new Solution.Split(300, 0));
        check("several leftover cents", () -> Solution.splitBill(100, 7), new Solution.Split(1428, 4));
        check("19.99 dollars is 1999 cents despite floating-point error", () -> Solution.splitBill(19.99, 2), new Solution.Split(999, 1));
        check("0.29 dollars is 29 cents despite floating-point error", () -> Solution.splitBill(0.29, 1), new Solution.Split(29, 0));
        check("fewer cents than people", () -> Solution.splitBill(0.02, 3), new Solution.Split(0, 2));
        check("zero bill", () -> Solution.splitBill(0, 5), new Solution.Split(0, 0));
        check("one person pays everything", () -> Solution.splitBill(1.15, 1), new Solution.Split(115, 0));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
