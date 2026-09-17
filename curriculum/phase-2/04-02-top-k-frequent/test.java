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
        check("most frequent first", () -> Solution.topKFrequent(new int[] { 1, 1, 1, 2, 2, 3 }, 2), List.of(1, 2));
        check("k = 1 gives the single most frequent value", () -> Solution.topKFrequent(new int[] { 4, 5, 5, 6 }, 1), List.of(5));
        check("ties go to the value that appears first",
            () -> List.of(Solution.topKFrequent(new int[] { 9, 4, 4, 9, 1 }, 2), Solution.topKFrequent(new int[] { 4, 9, 9, 4, 1 }, 2)),
            List.of(List.of(9, 4), List.of(4, 9)));
        check("frequency beats first appearance", () -> Solution.topKFrequent(new int[] { 3, 1, 1, 3, 2, 2, 2 }, 3), List.of(2, 3, 1));
        check("all distinct values keep their order", () -> Solution.topKFrequent(new int[] { 5, 3, 8, 1 }, 3), List.of(5, 3, 8));
        check("negative values and zero", () -> Solution.topKFrequent(new int[] { -1, -1, 0, 0, 0, 2 }, 2), List.of(0, -1));
        check("k equal to the number of distinct values", () -> Solution.topKFrequent(new int[] { 7, 8, 8, 9, 9, 9 }, 3), List.of(9, 8, 7));
        check("does not change the input", () -> {
            int[] values = { 2, 1, 2 };
            Solution.topKFrequent(values, 1);
            return Arrays.toString(values);
        }, "[2, 1, 2]");
        check("400000 values with 100000 distinct in O(n)", () -> {
            int n = 400000;
            int[] values = new int[n + 5];
            for (int i = 0; i < n; i++) values[i] = i % 100000;
            int[] extra = { 12345, 777, 12345, 777, 12345 };
            System.arraycopy(extra, 0, values, n, 5);
            return Solution.topKFrequent(values, 3);
        }, List.of(12345, 777, 0));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
