import java.util.Arrays;
import java.util.Objects;
import java.util.function.Supplier;

public class SolutionTest {
    static int passed = 0, failed = 0;
    static final int N = 200000;

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
            String shown = Arrays.deepToString(new Object[] { value });
            System.out.println("FAIL - " + name + "\n    expected: " + Arrays.deepToString(new Object[] { expected }) + "\n    got:      " + (shown.length() > 300 ? shown.substring(0, 300) + "..." : shown));
        }
    }

    static int[] sorted(int... nums) {
        Solution.quickSort(nums);
        return nums;
    }

    public static void main(String[] args) {
        check("sorts a small array with a duplicate", () -> sorted(5, 2, 9, 1, 5, 6), new int[] { 1, 2, 5, 5, 6, 9 });
        check("compares as numbers, with negatives", () -> sorted(10, -3, 9, 100, 0, -1000000000, 1), new int[] { -1000000000, -3, 0, 1, 9, 10, 100 });
        check("empty, single and two-element arrays", () -> new int[][] { sorted(), sorted(42), sorted(2, 1) }, new int[][] { {}, { 42 }, { 1, 2 } });
        check("sorts the same array in place", () -> {
            int[] nums = { 3, 1, 2 };
            Solution.quickSort(nums);
            return nums;
        }, new int[] { 1, 2, 3 });
        check("many repeated values", () -> sorted(2, 1, 2, 3, 1, 2, 3, 1, 2), new int[] { 1, 1, 1, 2, 2, 2, 2, 3, 3 });
        check("200000 shuffled numbers", () -> {
            int[] nums = new int[N];
            for (int i = 0; i < N; i++) nums[i] = (int) ((i * 7919L + 13) % 1000003) - 500000;
            int[] expected = nums.clone();
            Arrays.sort(expected);
            Solution.quickSort(nums);
            return Arrays.equals(nums, expected);
        }, true);
        check("200000 numbers already sorted and reversed", () -> {
            int[] up = new int[N], down = new int[N], expectedUp = new int[N], expectedDown = new int[N];
            for (int i = 0; i < N; i++) {
                up[i] = i;
                down[i] = N - i;
                expectedUp[i] = i;
                expectedDown[i] = i + 1;
            }
            Solution.quickSort(up);
            Solution.quickSort(down);
            return Arrays.equals(up, expectedUp) && Arrays.equals(down, expectedDown);
        }, true);
        check("200000 equal values", () -> {
            int[] same = new int[N];
            Arrays.fill(same, 7);
            Solution.quickSort(same);
            return Arrays.stream(same).allMatch(v -> v == 7);
        }, true);
        check("200000 values drawn from only three numbers", () -> {
            int[] few = new int[N];
            for (int i = 0; i < N; i++) few[i] = (i * 7) % 3;
            Solution.quickSort(few);
            int[] expected = new int[N];
            Arrays.fill(expected, 66667, 133334, 1);
            Arrays.fill(expected, 133334, N, 2);
            return Arrays.equals(few, expected);
        }, true);
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
