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

    public static void main(String[] args) {
        check("best window in the middle", () -> Solution.maxSumFixedWindow(new int[] { 2, 1, 5, 1, 3, 2 }, 3), 9);
        check("best window at the end",
            () -> Solution.maxSumFixedWindow(new int[] { 2, 3, 4, 1, 5 }, 2) * 10 + Solution.maxSumFixedWindow(new int[] { 4, -1, 2, -7, 5, 6 }, 1), 76);
        check("all negative values give a negative sum", () -> Solution.maxSumFixedWindow(new int[] { -1, -2, -3, -4 }, 2), -3);
        check("window covers the whole array",
            () -> Solution.maxSumFixedWindow(new int[] { 1, 2, 3 }, 3) * 10 + Solution.maxSumFixedWindow(new int[] { 5 }, 1), 65);
        check("k larger than the array gives 0",
            () -> Solution.maxSumFixedWindow(new int[] { 1, 2 }, 3) + Solution.maxSumFixedWindow(new int[] {}, 1), 0);
        check("all windows equal", () -> Solution.maxSumFixedWindow(new int[] { 3, 3, 3, 3 }, 2), 6);
        check("does not change the input", () -> {
            int[] values = { 1, 2, 3 };
            Solution.maxSumFixedWindow(values, 2);
            return Arrays.toString(values);
        }, "[1, 2, 3]");
        check("400000 values with a window of 200500 in O(n)", () -> {
            int n = 400000;
            int[] values = new int[n];
            for (int i = 0; i < n; i++) values[i] = i % 1000;
            return Solution.maxSumFixedWindow(values, 200500);
        }, 200 * 499500 + 374750);
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
