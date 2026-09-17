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
        check("all sides equal is equilateral, not isosceles", () -> Solution.triangleKind(3, 3, 3), "equilateral");
        check("two equal sides first is isosceles", () -> Solution.triangleKind(3, 3, 5), "isosceles");
        check("two equal sides last is isosceles", () -> Solution.triangleKind(5, 3, 3), "isosceles");
        check("two equal sides apart is isosceles", () -> Solution.triangleKind(3, 5, 3), "isosceles");
        check("no equal sides is scalene", () -> Solution.triangleKind(3, 4, 5), "scalene");
        check("no equal sides in another order is scalene", () -> Solution.triangleKind(5, 3, 4), "scalene");
        check("flat triangle is invalid", () -> Solution.triangleKind(1, 2, 3), "invalid");
        check("flat triangle in another order is invalid", () -> Solution.triangleKind(3, 1, 2), "invalid");
        check("two equal sides that are too short is invalid, not isosceles", () -> Solution.triangleKind(1, 1, 5), "invalid");
        check("long side first with two short equal sides is invalid", () -> Solution.triangleKind(5, 1, 1), "invalid");
        check("all sides zero is invalid, not equilateral", () -> Solution.triangleKind(0, 0, 0), "invalid");
        check("one negative side is invalid", () -> Solution.triangleKind(-3, 4, 5), "invalid");
        check("all negative equal sides is invalid", () -> Solution.triangleKind(-2, -2, -2), "invalid");
        check("just valid when two sides add up to one more than the third", () -> Solution.triangleKind(2, 3, 4), "scalene");
        check("smallest equilateral", () -> Solution.triangleKind(1, 1, 1), "equilateral");
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
