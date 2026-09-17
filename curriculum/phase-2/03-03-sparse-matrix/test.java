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
        check("a new matrix is all zeros", () -> {
            Solution.SparseMatrix m = new Solution.SparseMatrix(3, 4);
            return List.of(m.get(0, 0), m.get(2, 3), m.nonZeroCount());
        }, List.of(0, 0, 0));
        check("set and get keep rows and columns apart", () -> {
            Solution.SparseMatrix m = new Solution.SparseMatrix(2, 2);
            m.set(0, 1, 5);
            m.set(1, 0, -7);
            return List.of(m.get(0, 0), m.get(0, 1), m.get(1, 0), m.get(1, 1), m.nonZeroCount());
        }, List.of(0, 5, -7, 0, 2));
        check("overwriting a cell doesn't add to the count", () -> {
            Solution.SparseMatrix m = new Solution.SparseMatrix(1, 1);
            m.set(0, 0, 3);
            m.set(0, 0, 4);
            return List.of(m.get(0, 0), m.nonZeroCount());
        }, List.of(4, 1));
        check("setting 0 removes a stored cell and ignores an empty one", () -> {
            Solution.SparseMatrix m = new Solution.SparseMatrix(2, 2);
            m.set(1, 1, 9);
            m.set(1, 1, 0);
            m.set(0, 0, 0);
            return List.of(m.get(1, 1), m.nonZeroCount());
        }, List.of(0, 0));
        check("multiplies by a vector", () -> {
            Solution.SparseMatrix m = new Solution.SparseMatrix(2, 3);
            m.set(0, 0, 1);
            m.set(0, 2, 2);
            m.set(1, 1, 3);
            return Arrays.toString(m.multiplyVector(new int[] { 4, 5, 6 }));
        }, "[16, 15]");
        check("empty rows give 0 and removed cells don't contribute", () -> {
            Solution.SparseMatrix m = new Solution.SparseMatrix(3, 2);
            m.set(1, 0, -1);
            m.set(1, 1, 2);
            m.set(2, 0, 8);
            m.set(2, 0, 0);
            return Arrays.toString(m.multiplyVector(new int[] { 3, 4 }));
        }, "[0, 5, 0]");
        check("a matrix with no cells gives a zero vector of length rows",
            () -> Arrays.toString(new Solution.SparseMatrix(4, 1).multiplyVector(new int[] { 7 })), "[0, 0, 0, 0]");
        check("200000 x 200000 matrix with 400000 cells in O(rows + non-zeros)", () -> {
            int n = 200000;
            Solution.SparseMatrix m = new Solution.SparseMatrix(n, n);
            for (int i = 0; i < n; i++) {
                m.set(i, i, 2);
                m.set(i, (i + 1) % n, 1);
            }
            int[] vector = new int[n];
            for (int i = 0; i < n; i++) vector[i] = i % 1000;
            long[] result = m.multiplyVector(vector);
            int wrong = 0;
            for (int i = 0; i < n; i++) if (result[i] != 2 * (i % 1000) + ((i + 1) % n) % 1000) wrong++;
            return List.of(m.nonZeroCount(), result.length, wrong);
        }, List.of(400000, 200000, 0));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
