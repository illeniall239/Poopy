import java.util.Arrays;
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

    static String pair(int[] values, long target) {
        return Arrays.toString(Solution.pairWithTargetSum(values, target));
    }

    public static void main(String[] args) {
        check("finds a simple pair", () -> pair(new int[] { 2, 7, 11, 15 }, 9), "[0, 1]");
        check("an element doesn't pair with itself", () -> pair(new int[] { 3, 2, 4 }, 6), "[1, 2]");
        check("equal values at two positions form a pair", () -> pair(new int[] { 3, 3 }, 6), "[0, 1]");
        check("smallest j wins, then smallest i",
            () -> pair(new int[] { 1, 3, 2, 4, 3 }, 6) + pair(new int[] { 2, 2, 4 }, 6) + pair(new int[] { 1, 5, 1, 5 }, 6),
            "[2, 3][0, 2][0, 1]");
        check("no pair gives [-1, -1]",
            () -> pair(new int[] { 5 }, 10) + pair(new int[] {}, 0) + pair(new int[] { 1, 2, 3 }, 100),
            "[-1, -1][-1, -1][-1, -1]");
        check("negative values and zero",
            () -> pair(new int[] { -3, 4, 0, 3, 90 }, 0) + pair(new int[] { 0, 7, 0 }, 0), "[0, 3][0, 2]");
        check("does not change the input", () -> {
            int[] values = { 4, 1, 3 };
            Solution.pairWithTargetSum(values, 4);
            return Arrays.toString(values);
        }, "[4, 1, 3]");
        check("extreme values", () -> pair(new int[] { -1000000000, 1000000000, -1000000000 }, -2000000000L), "[0, 2]");
        check("400000 values with the only pair at the end in O(n)", () -> {
            int n = 400000;
            int[] values = new int[n];
            for (int i = 0; i < n; i++) values[i] = i;
            return pair(values, 2L * n - 3);
        }, "[399998, 399999]");
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
