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
        check("boiling point to Fahrenheit", () -> Solution.celsiusToFahrenheit(100), 212.0);
        check("freezing point to Fahrenheit", () -> Solution.celsiusToFahrenheit(0), 32.0);
        check("body temperature to Fahrenheit", () -> Solution.celsiusToFahrenheit(37), 98.6);
        check("floating-point noise is rounded to one decimal place", () -> Solution.celsiusToFahrenheit(36.6), 97.9);
        check("-40 is the same on both scales (C to F)", () -> Solution.celsiusToFahrenheit(-40), -40.0);
        check("-40 is the same on both scales (F to C)", () -> Solution.fahrenheitToCelsius(-40), -40.0);
        check("subtracts 32 before multiplying", () -> Solution.fahrenheitToCelsius(212), 100.0);
        check("body temperature to Celsius", () -> Solution.fahrenheitToCelsius(98.6), 37.0);
        check("negative result rounds to one decimal place", () -> Solution.fahrenheitToCelsius(0), -17.8);
        check("returns a plain number", () -> Solution.fahrenheitToCelsius(50), 10.0);
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
