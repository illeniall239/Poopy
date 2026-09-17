import java.util.ArrayList;
import java.util.Arrays;
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

    /** Sorts each combination and then the list, so any output order is accepted. */
    static List<List<Integer>> normalize(List<List<Integer>> combos) {
        List<List<Integer>> out = new ArrayList<>();
        for (List<Integer> c : combos) {
            List<Integer> copy = new ArrayList<>(c);
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

    public static void main(String[] args) {
        check("one repeat and one single",
                () -> normalize(Solution.combinationsToTarget(new int[] {2, 3, 6, 7}, 7)),
                List.of(List.of(2, 2, 3), List.of(7)));
        check("three combinations",
                () -> normalize(Solution.combinationsToTarget(new int[] {2, 3, 5}, 8)),
                List.of(List.of(2, 2, 2, 2), List.of(2, 3, 3), List.of(3, 5)));
        check("no combination possible", () -> Solution.combinationsToTarget(new int[] {2}, 1), List.of());
        check("same candidate many times", () -> normalize(Solution.combinationsToTarget(new int[] {1}, 3)),
                List.of(List.of(1, 1, 1)));
        check("unsorted candidates, no duplicate combinations", () -> {
            int[] candidates = {8, 4, 2};
            return List.of(normalize(Solution.combinationsToTarget(candidates, 8)), Arrays.toString(candidates));
        }, List.of(List.of(List.of(2, 2, 2, 2), List.of(2, 2, 4), List.of(4, 4), List.of(8)), "[8, 4, 2]"));
        check("order does not make a new combination",
                () -> normalize(Solution.combinationsToTarget(new int[] {1, 2}, 4)),
                List.of(List.of(1, 1, 1, 1), List.of(1, 1, 2), List.of(2, 2)));
        check("531 combinations for target 60", () -> {
            List<List<Integer>> result = normalize(Solution.combinationsToTarget(new int[] {2, 3, 5, 7, 11}, 60));
            boolean valid = true;
            for (List<Integer> c : result) {
                int sum = 0;
                for (int v : c) {
                    sum += v;
                    if (!List.of(2, 3, 5, 7, 11).contains(v)) valid = false;
                }
                if (sum != 60) valid = false;
            }
            return List.of(result.size(), new HashSet<>(result).size(), valid);
        }, List.of(531, 531, true));

        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
