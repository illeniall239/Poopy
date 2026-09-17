import java.util.Arrays;
import java.util.Objects;
import java.util.function.Supplier;

public class SolutionTest {
    static int passed = 0, failed = 0;

    static void check(String name, Supplier<Object> got, Object expected) {
        Object actual;
        try {
            actual = got.get();
        } catch (Throwable t) {
            failed++;
            System.out.println("FAIL - " + name + "\n    threw: " + t);
            return;
        }
        if (Objects.deepEquals(actual, expected)) {
            passed++;
            System.out.println("ok - " + name);
        } else {
            failed++;
            System.out.println("FAIL - " + name + "\n    expected: " + show(expected) + "\n    got:      " + show(actual));
        }
    }

    static String show(Object o) {
        if (o instanceof double[]) return Arrays.toString((double[]) o);
        if (o instanceof int[]) return Arrays.toString((int[]) o);
        if (o instanceof Object[]) return Arrays.deepToString((Object[]) o);
        return String.valueOf(o);
    }

    public static void main(String[] args) {
        check("unsorted distinct values", () -> Solution.secondLargest(new int[]{3, 1, 2}), 2);
        check("duplicates of the largest are skipped", () -> Solution.secondLargest(new int[]{5, 5, 4}), 4);
        check("all negative numbers", () -> Solution.secondLargest(new int[]{-1, -3, -2}), -2);
        check("all values equal gives null", () -> Solution.secondLargest(new int[]{7, 7, 7}), null);
        check("empty array gives null", () -> Solution.secondLargest(new int[]{}), null);
        check("single-element array gives null", () -> Solution.secondLargest(new int[]{9}), null);
        check("new largest pushes old largest into second place", () -> Solution.secondLargest(new int[]{1, 2, 3, 10}), 3);
        check("second largest appears after the largest", () -> Solution.secondLargest(new int[]{10, 1, 8, 10, 8}), 8);
        check("zero can be the answer", () -> Solution.secondLargest(new int[]{0, -4, 6}), 0);
        check("does not modify the input", () -> {
            int[] nums = {4, 9, 2, 9};
            Solution.secondLargest(nums);
            return nums;
        }, new int[]{4, 9, 2, 9});
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
