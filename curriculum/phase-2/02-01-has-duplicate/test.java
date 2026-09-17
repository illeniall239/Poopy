import java.util.Arrays;
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

    public static void main(String[] args) {
        check("finds a repeated value", () -> Solution.hasDuplicate(new int[] { 1, 2, 3, 1 }), true);
        check("all distinct values", () -> Solution.hasDuplicate(new int[] { 1, 2, 3 }), false);
        check("empty array has no duplicates", () -> Solution.hasDuplicate(new int[] {}), false);
        check("a single value is not a duplicate of itself", () -> Solution.hasDuplicate(new int[] { 7 }), false);
        check("negative values and their opposites are different",
            () -> List.of(Solution.hasDuplicate(new int[] { -1, 1, -2, 2, 0 }), Solution.hasDuplicate(new int[] { -5, 3, -5 })),
            List.of(false, true));
        check("duplicates as the last two values", () -> Solution.hasDuplicate(new int[] { 4, 8, 15, 16, 23, 42, 42 }), true);
        check("does not change the input", () -> {
            int[] values = { 3, 1, 2, 3 };
            Solution.hasDuplicate(values);
            return Arrays.toString(values);
        }, "[3, 1, 2, 3]");
        check("400000 distinct values in O(n)", () -> {
            int n = 400000;
            int[] values = new int[n];
            for (int i = 0; i < n; i++) values[i] = (int) ((long) i * 7919 % n);
            return Solution.hasDuplicate(values);
        }, false);
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
