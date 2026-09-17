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
            System.out.println("FAIL - " + name + "\n    expected: " + expected + "\n    got:      " + actual);
        }
    }

    static Solution.Seat seat(int row, int column) {
        return new Solution.Seat(row, column);
    }

    public static void main(String[] args) {
        check("first seat is row 1, column 1", () -> Solution.findSeat(1, 10), seat(1, 1));
        check("seat in the middle of a later row", () -> Solution.findSeat(25, 10), seat(3, 5));
        check("last seat in a row stays in that row", () -> Solution.findSeat(10, 10), seat(1, 10));
        check("seat after the last seat starts the next row", () -> Solution.findSeat(11, 10), seat(2, 1));
        check("last seat of a later row", () -> Solution.findSeat(12, 4), seat(3, 4));
        check("one seat per row", () -> Solution.findSeat(7, 1), seat(7, 1));
        check("large seat number", () -> Solution.findSeat(1000000, 999), seat(1002, 1));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
