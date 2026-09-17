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

    public static void main(String[] args) {
        check("takes the shorter way round a cycle",
                () -> Solution.shortestPath(5, new int[][] {{0, 1}, {1, 2}, {2, 3}, {3, 4}, {0, 4}}, 0, 3), 2);
        check("start equals end", () -> Solution.shortestPath(3, new int[][] {{0, 1}}, 2, 2), 0);
        check("unreachable node gives -1", () -> Solution.shortestPath(4, new int[][] {{0, 1}, {2, 3}}, 0, 3), -1);
        check("node with no edges gives -1", () -> Solution.shortestPath(3, new int[][] {}, 0, 2), -1);
        check("edges work in both directions", () -> Solution.shortestPath(3, new int[][] {{1, 0}, {2, 1}}, 0, 2), 2);
        check("cycles and repeated edges do not loop forever",
                () -> Solution.shortestPath(4, new int[][] {{0, 1}, {1, 2}, {2, 0}, {0, 1}, {2, 3}}, 0, 3), 2);
        check("several routes of different lengths",
                () -> Solution.shortestPath(6, new int[][] {{0, 1}, {0, 2}, {1, 3}, {2, 3}, {3, 4}, {4, 5}, {1, 5}}, 0, 5), 2);
        check("path of 200 000 nodes in O(n + edges)", () -> {
            int n = 200000;
            int[][] edges = new int[n - 1][];
            for (int i = 0; i < n - 1; i++) {
                int p = (int) ((i * 7919L) % (n - 1));
                edges[i] = i % 2 == 0 ? new int[] {p, p + 1} : new int[] {p + 1, p};
            }
            return Solution.shortestPath(n, edges, 0, n - 1);
        }, 199999);

        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
