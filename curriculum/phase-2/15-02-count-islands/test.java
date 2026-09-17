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
        check("three islands", () -> Solution.countIslands(new String[] {"11000", "11000", "00100", "00011"}), 3);
        check("empty grid", () -> Solution.countIslands(new String[] {}), 0);
        check("all water", () -> Solution.countIslands(new String[] {"000", "000"}), 0);
        check("diagonal cells are not connected", () -> Solution.countIslands(new String[] {"101", "010", "101"}), 5);
        check("an island that winds around water",
                () -> Solution.countIslands(new String[] {"10111", "10101", "11101"}), 1);
        check("single row", () -> Solution.countIslands(new String[] {"1011011"}), 3);
        check("25x25 all land is one island", () -> {
            String[] grid = new String[25];
            java.util.Arrays.fill(grid, "1".repeat(25));
            return Solution.countIslands(grid);
        }, 1);
        check("1000x1000 grid in O(rows x columns)", () -> {
            String[] grid = new String[1000];
            for (int r = 0; r < 1000; r++) {
                StringBuilder row = new StringBuilder();
                for (int c = 0; c < 1000; c++) row.append(r % 2 == 0 && c % 2 == 0 ? '1' : '0');
                grid[r] = row.toString();
            }
            return Solution.countIslands(grid);
        }, 250000);

        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
