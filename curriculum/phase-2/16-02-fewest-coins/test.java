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
        check("three coins make 11", () -> Solution.fewestCoins(new int[] {1, 2, 5}, 11), 3);
        check("largest-first would not be fewest", () -> Solution.fewestCoins(new int[] {1, 3, 4}, 6), 2);
        check("impossible amount gives -1", () -> Solution.fewestCoins(new int[] {2}, 3), -1);
        check("amount 0 needs no coins", () -> Solution.fewestCoins(new int[] {1}, 0), 0);
        check("unsorted coins", () -> Solution.fewestCoins(new int[] {7, 3}, 23), 5);
        check("amount 700 from 3, 7 and 11", () -> Solution.fewestCoins(new int[] {3, 7, 11}, 700), 64);
        check("odd amount 699 from even coins is impossible", () -> Solution.fewestCoins(new int[] {4, 6}, 699), -1);

        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
