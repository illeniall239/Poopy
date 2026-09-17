import java.util.List;
import java.util.Objects;
import java.util.OptionalDouble;
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
        check("empty array gives empty", () -> Solution.average(new int[] {}), OptionalDouble.empty());
        check("all zeros average to 0", () -> Solution.average(new int[] { 0, 0, 0 }), OptionalDouble.of(0));
        check("single value is its own average", () -> Solution.average(new int[] { 5 }), OptionalDouble.of(5));
        check("whole-number average", () -> Solution.average(new int[] { 2, 4, 6 }), OptionalDouble.of(4));
        check("average is not rounded",
            () -> List.of(Solution.average(new int[] { 1, 2 }), Solution.average(new int[] { 1, 1, 2 })),
            List.of(OptionalDouble.of(1.5), OptionalDouble.of(4.0 / 3)));
        check("negative numbers", () -> Solution.average(new int[] { -1, -2 }), OptionalDouble.of(-1.5));
        check("first element counts", () -> Solution.average(new int[] { 100, 0, 0, 0 }), OptionalDouble.of(25));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
