import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.HashSet;
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

    /** Sorts each subset and then the list of subsets, so any output order is accepted. */
    static List<List<Integer>> normalize(List<List<Integer>> sets) {
        List<List<Integer>> out = new ArrayList<>();
        for (List<Integer> s : sets) {
            List<Integer> copy = new ArrayList<>(s);
            copy.sort(null);
            out.add(copy);
        }
        out.sort((x, y) -> {
            for (int i = 0; i < Math.min(x.size(), y.size()); i++) {
                int c = Integer.compare(x.get(i), y.get(i));
                if (c != 0) return c;
            }
            return Integer.compare(x.size(), y.size());
        });
        return out;
    }

    static int distinctCount(List<List<Integer>> sets) {
        return new HashSet<>(normalize(sets)).size();
    }

    public static void main(String[] args) {
        check("all subsets of three numbers", () -> normalize(Solution.subsets(new int[] {1, 2, 3})),
                normalize(List.of(List.of(), List.of(1), List.of(2), List.of(3), List.of(1, 2), List.of(1, 3),
                        List.of(2, 3), List.of(1, 2, 3))));
        check("empty array has only the empty subset", () -> Solution.subsets(new int[] {}), List.of(List.of()));
        check("one number", () -> normalize(Solution.subsets(new int[] {5})), List.of(List.of(), List.of(5)));
        check("negative and unsorted numbers", () -> normalize(Solution.subsets(new int[] {3, -1})),
                List.of(List.of(), List.of(-1), List.of(-1, 3), List.of(3)));
        check("each stored subset is its own copy", () -> {
            int[] nums = {4, 8, 15, 16, 23, 42, -1, -2, -3, 0};
            List<List<Integer>> result = Solution.subsets(nums);
            return List.of(result.size(), distinctCount(result), Arrays.toString(nums));
        }, List.of(1024, 1024, "[4, 8, 15, 16, 23, 42, -1, -2, -3, 0]"));
        check("all 65 536 subsets of 16 numbers", () -> {
            int[] nums = new int[16];
            for (int i = 0; i < 16; i++) nums[i] = i * 3 - 20;
            List<List<Integer>> result = Solution.subsets(nums);
            return List.of(result.size(), distinctCount(result));
        }, List.of(65536, 65536));

        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
