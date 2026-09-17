import java.util.Arrays;
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
            System.out.println("FAIL - " + name + "\n    expected: " + show(expected) + "\n    got:      " + show(actual));
        }
    }

    static String show(Object o) {
        if (o instanceof double[]) return Arrays.toString((double[]) o);
        if (o instanceof int[]) return Arrays.toString((int[]) o);
        if (o instanceof Object[]) return Arrays.deepToString((Object[]) o);
        return String.valueOf(o);
    }

    public static void main(String[] args) {
        check("light parcel", () -> Solution.shippingCost(2000, 0.5, false), 499);
        check("light parcel, exactly 1 kg", () -> Solution.shippingCost(2000, 1, false), 499);
        check("middle tier", () -> Solution.shippingCost(2000, 1.5, false), 899);
        check("middle tier, exactly 5 kg", () -> Solution.shippingCost(2000, 5, false), 899);
        check("heavy tier just over 5 kg", () -> Solution.shippingCost(2000, 5.1, false), 1499);
        check("4999 cents is not free", () -> Solution.shippingCost(4999, 3, false), 899);
        check("free shipping starts at exactly 5000 cents", () -> Solution.shippingCost(5000, 3, false), 0);
        check("express adds 1000", () -> Solution.shippingCost(2000, 1, true), 1499);
        check("express is never free", () -> Solution.shippingCost(6000, 3, true), 1899);
        check("free shipping applies up to and including 20 kg", () -> Solution.shippingCost(6000, 20, false), 0);
        check("free shipping does not apply over 20 kg", () -> Solution.shippingCost(6000, 25, false), 1499);
        check("over 30 kg can't ship, even with free shipping", () -> Solution.shippingCost(9000, 31, false), -1);
        check("over 30 kg can't ship, even with express", () -> Solution.shippingCost(100, 30.5, true), -1);
        check("exactly 30 kg can still ship", () -> Solution.shippingCost(100, 30, true), 2499);
        check("zero subtotal is not free", () -> Solution.shippingCost(0, 2, false), 899);
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
