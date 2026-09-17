import java.util.Arrays;
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
            System.out.println("FAIL - " + name + "\n    expected: " + Arrays.deepToString(new Object[] {expected})
                    + "\n    got:      " + Arrays.deepToString(new Object[] {value}));
        }
    }

    /** Returns "valid", or what is wrong: every course exactly once, each required course before the course needing it. */
    static String validate(int numCourses, int[][] prerequisites, int[] order) {
        if (order.length != numCourses) return "order has " + order.length + " courses, expected " + numCourses;
        int[] position = new int[numCourses];
        Arrays.fill(position, -1);
        for (int i = 0; i < order.length; i++) {
            if (order[i] < 0 || order[i] >= numCourses) return "not a course: " + order[i];
            if (position[order[i]] != -1) return "course " + order[i] + " appears twice";
            position[order[i]] = i;
        }
        for (int[] p : prerequisites) {
            if (position[p[1]] >= position[p[0]]) return p[1] + " must come before " + p[0];
        }
        return "valid";
    }

    public static void main(String[] args) {
        check("one prerequisite", () -> {
            int[][] pre = {{1, 0}};
            return validate(2, pre, Solution.courseOrder(2, pre));
        }, "valid");
        check("two paths to the same course", () -> {
            int[][] pre = {{1, 0}, {2, 0}, {3, 1}, {3, 2}};
            return validate(4, pre, Solution.courseOrder(4, pre));
        }, "valid");
        check("no prerequisites", () -> validate(3, new int[][] {}, Solution.courseOrder(3, new int[][] {})), "valid");
        check("single course", () -> Solution.courseOrder(1, new int[][] {}), new int[] {0});
        check("two courses requiring each other", () -> Solution.courseOrder(2, new int[][] {{0, 1}, {1, 0}}), new int[] {});
        check("cycle that does not include every course",
                () -> Solution.courseOrder(4, new int[][] {{1, 0}, {2, 1}, {3, 2}, {1, 3}}), new int[] {});
        check("repeated pair", () -> {
            int[][] pre = {{1, 0}, {1, 0}, {2, 1}};
            return validate(3, pre, Solution.courseOrder(3, pre));
        }, "valid");
        check("chain of 100 000 courses in O(V + E)", () -> {
            int n = 100000;
            int[][] pre = new int[n - 1][];
            for (int i = 0; i < n - 1; i++) pre[i] = new int[] {i, i + 1};
            return validate(n, pre, Solution.courseOrder(n, pre));
        }, "valid");

        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
