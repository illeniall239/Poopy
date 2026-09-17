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
        check("one queen on a 1x1 board", () -> Solution.countQueens(1), 1);
        check("no placement on a 2x2 board", () -> Solution.countQueens(2), 0);
        check("no placement on a 3x3 board", () -> Solution.countQueens(3), 0);
        check("two placements on a 4x4 board", () -> Solution.countQueens(4), 2);
        check("four placements on a 6x6 board", () -> Solution.countQueens(6), 4);
        check("92 placements on an 8x8 board", () -> Solution.countQueens(8), 92);
        check("12x12 board needs pruning", () -> Solution.countQueens(12), 14200);

        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
