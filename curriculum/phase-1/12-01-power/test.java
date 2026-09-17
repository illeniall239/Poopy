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
        check("even exponent", () -> Solution.power(2, 10), 1024.0);
        check("odd exponent", () -> List.of(Solution.power(3, 5), Solution.power(3, 13)), List.of(243.0, 1594323.0));
        check("exponent 0 gives 1, even for base 0", () -> List.of(Solution.power(5, 0), Solution.power(0, 0)), List.of(1.0, 1.0));
        check("exponent 1 gives the base", () -> Solution.power(7, 1), 7.0);
        check("negative base keeps the right sign", () -> List.of(Solution.power(-2, 3), Solution.power(-2, 4)), List.of(-8.0, 16.0));
        check("decimal base", () -> Solution.power(0.5, 3), 0.125);
        check("huge exponent finishes without overflowing the stack",
            () -> List.of(Solution.power(1, 1000000000), Solution.power(-1, 999999999), Solution.power(2, 1023)),
            List.of(1.0, -1.0, Math.pow(2, 1023)));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
