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

    static String rotated(int[] values, int k) {
        Solution.rotateRight(values, k);
        return Arrays.toString(values);
    }

    public static void main(String[] args) {
        check("rotates the given array by 3", () -> rotated(new int[] { 1, 2, 3, 4, 5, 6, 7 }, 3), "[5, 6, 7, 1, 2, 3, 4]");
        check("k = 0 leaves the array alone", () -> rotated(new int[] { 1, 2, 3 }, 0), "[1, 2, 3]");
        check("k equal to the length is a full turn", () -> rotated(new int[] { 1, 2, 3, 4 }, 4), "[1, 2, 3, 4]");
        check("k larger than the length wraps around", () -> rotated(new int[] { 1, 2, 3 }, 10), "[3, 1, 2]");
        check("empty array stays empty", () -> rotated(new int[] {}, 5), "[]");
        check("single element", () -> rotated(new int[] { 9 }, 4), "[9]");
        check("duplicates and negative values", () -> rotated(new int[] { -1, -1, 2, 0 }, 1), "[0, -1, -1, 2]");
        check("1000000 elements with a huge k in O(n)", () -> {
            int n = 1000000;
            int[] values = new int[n];
            for (int i = 0; i < n; i++) values[i] = i;
            Solution.rotateRight(values, 1000000000 + 500000);
            for (int i = 0; i < n; i++) {
                if (values[i] != (i + 500000) % n) return "first wrong index " + i;
            }
            return "all correct";
        }, "all correct");
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
