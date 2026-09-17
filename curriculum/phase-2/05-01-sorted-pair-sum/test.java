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
            String shown = String.valueOf(value);
            System.out.println("FAIL - " + name + "\n    expected: " + expected + "\n    got:      " + (shown.length() > 300 ? shown.substring(0, 300) + "..." : shown));
        }
    }

    static String pair(int[] values, long target) {
        return Arrays.toString(Solution.sortedPairSum(values, target));
    }

    public static void main(String[] args) {
        check("finds a pair in the middle", () -> pair(new int[] { 1, 2, 3, 4, 6 }, 6), "[2, 4]");
        check("smallest first value wins", () -> pair(new int[] { 1, 2, 3, 4 }, 5) + pair(new int[] { 0, 1, 2, 3, 4, 5 }, 5), "[1, 4][0, 5]");
        check("a position can't be used twice", () -> pair(new int[] { 2, 3, 4 }, 6) + pair(new int[] { 1, 3, 7 }, 6), "[2, 4]null");
        check("equal values at two positions form a pair", () -> pair(new int[] { 3, 3 }, 6) + pair(new int[] { 1, 4, 4, 9 }, 8), "[3, 3][4, 4]");
        check("negative values and zero", () -> pair(new int[] { -5, -2, 0, 4, 9 }, 2) + pair(new int[] { -3, 0, 0, 3 }, 0), "[-2, 4][-3, 3]");
        check("no pair gives null", () -> pair(new int[] { 1, 2, 3 }, 100) + pair(new int[] {}, 0) + pair(new int[] { 7 }, 14), "nullnullnull");
        check("does not change the input", () -> {
            int[] values = { 1, 2, 3 };
            Solution.sortedPairSum(values, 4);
            return Arrays.toString(values);
        }, "[1, 2, 3]");
        check("extreme values", () -> pair(new int[] { -1000000000, 0, 1000000000 }, 0), "[-1000000000, 1000000000]");
        check("400000 even values with an odd target in O(n)", () -> {
            int n = 400000;
            int[] values = new int[n];
            for (int i = 0; i < n; i++) values[i] = 2 * i;
            return pair(values, 2L * n - 3);
        }, "null");
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
