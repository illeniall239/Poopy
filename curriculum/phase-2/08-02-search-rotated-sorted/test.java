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
        int[] rotated = { 40, 50, 60, 10, 20, 30 };
        check("target in the part after the rotation point",
            () -> List.of(Solution.searchRotated(rotated, 20), Solution.searchRotated(rotated, 10)), List.of(4, 3));
        check("target in the part before the rotation point",
            () -> List.of(Solution.searchRotated(rotated, 50), Solution.searchRotated(rotated, 40), Solution.searchRotated(rotated, 60)), List.of(1, 0, 2));
        check("missing target",
            () -> List.of(Solution.searchRotated(rotated, 35), Solution.searchRotated(rotated, 5), Solution.searchRotated(rotated, 70)), List.of(-1, -1, -1));
        check("not rotated at all", () -> List.of(
            Solution.searchRotated(new int[] { 10, 20, 30, 40 }, 30), Solution.searchRotated(new int[] { 10, 20, 30, 40 }, 25)), List.of(2, -1));
        check("rotated by one in each direction", () -> List.of(
            Solution.searchRotated(new int[] { 2, 3, 4, 5, 1 }, 1),
            Solution.searchRotated(new int[] { 5, 1, 2, 3, 4 }, 5),
            Solution.searchRotated(new int[] { 5, 1, 2, 3, 4 }, 4)), List.of(4, 0, 4));
        check("one and two elements", () -> List.of(
            Solution.searchRotated(new int[] { 7 }, 7), Solution.searchRotated(new int[] { 7 }, 8),
            Solution.searchRotated(new int[] { 3, 1 }, 1), Solution.searchRotated(new int[] { 3, 1 }, 3),
            Solution.searchRotated(new int[] { 3, 1 }, 2)), List.of(0, -1, 1, 0, -1));
        check("empty array", () -> Solution.searchRotated(new int[] {}, 7), -1);
        check("every element of every rotation of a small array", () -> {
            int[] base = { -9, -4, 0, 3, 8, 15, 21 };
            int len = base.length, wrong = 0;
            for (int k = 0; k < len; k++) {
                int[] nums = new int[len];
                for (int j = 0; j < len; j++) nums[j] = base[(j - k + len) % len];
                for (int i = 0; i < len; i++) {
                    if (Solution.searchRotated(nums, nums[i]) != i) wrong++;
                    if (Solution.searchRotated(nums, nums[i] + 1) != -1) wrong++;
                }
            }
            return wrong;
        }, 0);
        check("100000 searches in 1000000 rotated values in O(log n)", () -> {
            int n = 1000000, k = 300000;
            int[] nums = new int[n];
            for (int j = 0; j < n; j++) nums[j] = 2 * ((j + k) % n);
            int wrong = 0;
            for (int q = 0; q < 100000; q++) {
                int i = (int) ((q * 7919L) % n);
                if (Solution.searchRotated(nums, 2 * i) != (i - k + n) % n) wrong++;
                if (Solution.searchRotated(nums, 2 * i + 1) != -1) wrong++;
            }
            return wrong;
        }, 0);
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
