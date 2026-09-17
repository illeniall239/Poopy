import java.util.Map;
import java.util.Objects;

public class SolutionTest {
    static int passed = 0, failed = 0;

    static void check(String name, Object got, Object expected) {
        if (Objects.deepEquals(got, expected)) {
            passed++;
            System.out.println("ok - " + name);
        } else {
            failed++;
            System.out.println("FAIL - " + name + "\n    expected: " + expected + "\n    got:      " + got);
        }
    }

    static Map<String, Integer> coins(int q, int d, int n, int p) {
        return Map.of("quarters", q, "dimes", d, "nickels", n, "pennies", p);
    }

    public static void main(String[] args) {
        check("one of each coin for 41", Solution.makeChange(41), coins(1, 1, 1, 1));
        check("skips coins that aren't needed", Solution.makeChange(30), coins(1, 0, 1, 0));
        check("zero cents gives no coins", Solution.makeChange(0), coins(0, 0, 0, 0));
        check("pennies only below 5", Solution.makeChange(4), coins(0, 0, 0, 4));
        check("exact multiple of 25", Solution.makeChange(100), coins(4, 0, 0, 0));
        check("two dimes, no nickel for 99", Solution.makeChange(99), coins(3, 2, 0, 4));
        check("large amount", Solution.makeChange(100000), coins(4000, 0, 0, 0));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
