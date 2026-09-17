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
        check("unit circle", () -> Solution.area(new Solution.Circle(1)), Math.PI);
        check("circle area grows with the square of the radius",
            () -> List.of(Solution.area(new Solution.Circle(2)), Solution.area(new Solution.Circle(0.5))),
            List.of(4 * Math.PI, Math.PI / 4));
        check("rectangle", () -> Solution.area(new Solution.Rectangle(3, 4)), 12.0);
        check("triangle is half of base times height", () -> Solution.area(new Solution.Triangle(5, 3)), 7.5);
        check("rectangle and triangle with the same numbers differ",
            () -> List.of(Solution.area(new Solution.Rectangle(4, 5)), Solution.area(new Solution.Triangle(4, 5))),
            List.of(20.0, 10.0));
        check("zero-sized shapes have zero area",
            () -> List.of(
                Solution.area(new Solution.Circle(0)),
                Solution.area(new Solution.Rectangle(0, 9)),
                Solution.area(new Solution.Triangle(7, 0))),
            List.of(0.0, 0.0, 0.0));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
