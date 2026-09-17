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
        check("finds a run among unrelated values", () -> Solution.longestConsecutiveRun(new int[] { 100, 4, 200, 1, 3, 2 }), 4);
        check("run spread over the whole array", () -> Solution.longestConsecutiveRun(new int[] { 0, 3, 7, 2, 5, 8, 4, 6, 0, 1 }), 9);
        check("no two values are consecutive",
            () -> Solution.longestConsecutiveRun(new int[] { 10, 30, 20 }) * 10 + Solution.longestConsecutiveRun(new int[] { 5 }), 11);
        check("negative values", () -> Solution.longestConsecutiveRun(new int[] { -1, 0, 1, -3, -2 }), 5);
        check("duplicates count once",
            () -> Solution.longestConsecutiveRun(new int[] { 1, 2, 2, 3 }) * 10 + Solution.longestConsecutiveRun(new int[] { 7, 7, 7 }), 31);
        check("empty array gives 0", () -> Solution.longestConsecutiveRun(new int[] {}), 0);
        check("picks the longest of several runs", () -> Solution.longestConsecutiveRun(new int[] { 9, 1, 4, 2, 10, 11, 12, 3, 20 }), 4);
        check("does not change the input", () -> {
            int[] values = { 3, 1, 2 };
            Solution.longestConsecutiveRun(values);
            return Arrays.toString(values);
        }, "[3, 1, 2]");
        check("400000 shuffled consecutive values in O(n)", () -> {
            int n = 400000;
            int[] values = new int[n];
            for (int i = 0; i < n; i++) values[i] = (int) (((long) i * 7919) % n) - 1000;
            return Solution.longestConsecutiveRun(values);
        }, 400000);
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
