import java.util.ArrayList;
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
        } catch (Throwable e) {
            failed++;
            System.out.println("FAIL - " + name + "\n    threw: " + e);
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

    static List<Integer> addAll(Solution.KthLargest tracker, int... values) {
        List<Integer> out = new ArrayList<>();
        for (int v : values) out.add(tracker.add(v));
        return out;
    }

    public static void main(String[] args) {
        check("3rd largest as numbers arrive", () -> addAll(new Solution.KthLargest(3), 4, 5, 8, 2, 9, 4),
                Arrays.asList(null, null, 4, 4, 5, 5));
        check("k = 1 tracks the maximum", () -> addAll(new Solution.KthLargest(1), 3, 1, 7, 7),
                List.of(3, 3, 7, 7));
        check("duplicates count separately", () -> addAll(new Solution.KthLargest(2), 5, 5, 5, 6, 6),
                Arrays.asList(null, 5, 5, 5, 6));
        check("negative numbers", () -> addAll(new Solution.KthLargest(2), -1, -5, -3, 0),
                Arrays.asList(null, -5, -3, -1));
        check("instances keep separate numbers", () -> {
            Solution.KthLargest a = new Solution.KthLargest(2);
            Solution.KthLargest b = new Solution.KthLargest(1);
            return Arrays.asList(a.add(1), b.add(10), a.add(2), b.add(3));
        }, Arrays.asList(null, 10, 1, 10));
        check("200 000 additions with k = 50 000, O(log k) each", () -> {
            Solution.KthLargest tracker = new Solution.KthLargest(50000);
            long sum = 0;
            Integer last = null;
            for (int i = 0; i < 200000; i++) {
                last = tracker.add((int) ((i * 7919L) % 200003));
                if (last != null) sum += last;
            }
            return List.of(last, sum);
        }, List.of(150000, 16136295473L));

        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
