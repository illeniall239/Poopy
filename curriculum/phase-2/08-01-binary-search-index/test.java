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
        int[] odds = { 1, 3, 5, 7, 9, 11 };
        check("finds a value in the middle", () -> List.of(Solution.binarySearch(odds, 7), Solution.binarySearch(odds, 5)), List.of(3, 2));
        check("finds the first and last values", () -> List.of(Solution.binarySearch(odds, 1), Solution.binarySearch(odds, 11)), List.of(0, 5));
        check("missing value between two elements", () -> Solution.binarySearch(odds, 4), -1);
        check("missing value below and above the range", () -> List.of(Solution.binarySearch(odds, 0), Solution.binarySearch(odds, 12)), List.of(-1, -1));
        check("empty array", () -> Solution.binarySearch(new int[] {}, 5), -1);
        check("one and two elements", () -> List.of(
            Solution.binarySearch(new int[] { 5 }, 5), Solution.binarySearch(new int[] { 5 }, 6),
            Solution.binarySearch(new int[] { 2, 4 }, 4), Solution.binarySearch(new int[] { 2, 4 }, 3)), List.of(0, -1, 1, -1));
        check("negative and very large values", () -> {
            int[] values = { -2000000000, -7, 0, 1999999999, 2000000000 };
            return List.of(Solution.binarySearch(values, -2000000000), Solution.binarySearch(values, 2000000000), Solution.binarySearch(values, 1));
        }, List.of(0, 4, -1));
        check("100000 searches in 1000000 values in O(log n)", () -> {
            int n = 1000000;
            int[] evens = new int[n];
            for (int i = 0; i < n; i++) evens[i] = 2 * i;
            int wrong = 0;
            for (int q = 0; q < 100000; q++) {
                int i = (int) ((q * 7919L) % n);
                if (Solution.binarySearch(evens, 2 * i) != i) wrong++;
                if (Solution.binarySearch(evens, 2 * i + 1) != -1) wrong++;
            }
            return wrong;
        }, 0);
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
