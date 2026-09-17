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
            System.out.println("FAIL - " + name + "\n    expected: " + Arrays.deepToString(new Object[] { expected }) + "\n    got:      " + Arrays.deepToString(new Object[] { value }));
        }
    }

    public static void main(String[] args) {
        check("sorts a small array with a duplicate", () -> Solution.mergeSort(new int[] { 5, 2, 9, 1, 5, 6 }), new int[] { 1, 2, 5, 5, 6, 9 });
        check("compares as numbers, not as strings", () -> Solution.mergeSort(new int[] { 10, 9, 100, 1 }), new int[] { 1, 9, 10, 100 });
        check("negative numbers and zero", () -> Solution.mergeSort(new int[] { -3, 0, -7, 4, -1000000000, 1000000000 }),
            new int[] { -1000000000, -7, -3, 0, 4, 1000000000 });
        check("empty and single-element arrays", () -> new int[][] { Solution.mergeSort(new int[] {}), Solution.mergeSort(new int[] { 42 }) },
            new int[][] { {}, { 42 } });
        check("already sorted, reversed and all equal", () -> new int[][] {
            Solution.mergeSort(new int[] { 1, 2, 3, 4, 5 }), Solution.mergeSort(new int[] { 5, 4, 3, 2, 1 }), Solution.mergeSort(new int[] { 7, 7, 7, 7 }) },
            new int[][] { { 1, 2, 3, 4, 5 }, { 1, 2, 3, 4, 5 }, { 7, 7, 7, 7 } });
        check("odd length where one half has leftovers", () -> Solution.mergeSort(new int[] { 8, 1, 9, 2, 10, 3, 11 }), new int[] { 1, 2, 3, 8, 9, 10, 11 });
        check("returns a new array and leaves the input unchanged", () -> {
            int[] nums = { 3, 1, 2 };
            int[] result = Solution.mergeSort(nums);
            return List.of(Arrays.equals(result, new int[] { 1, 2, 3 }), Arrays.equals(nums, new int[] { 3, 1, 2 }), result != nums);
        }, List.of(true, true, true));
        check("1000000 shuffled numbers in O(n log n)", () -> {
            int n = 1000000;
            int[] nums = new int[n];
            for (int i = 0; i < n; i++) nums[i] = (int) ((i * 7919L + 13) % 1000003) - 500000;
            int[] expected = nums.clone();
            Arrays.sort(expected);
            return Arrays.equals(Solution.mergeSort(nums), expected);
        }, true);
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
