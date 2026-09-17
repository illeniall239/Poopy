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
        check("small primes (2)", () -> Solution.isPrime(2), true);
        check("small primes (3)", () -> Solution.isPrime(3), true);
        check("small primes (7)", () -> Solution.isPrime(7), true);
        check("numbers below 2 are not prime (1)", () -> Solution.isPrime(1), false);
        check("numbers below 2 are not prime (0)", () -> Solution.isPrime(0), false);
        check("numbers below 2 are not prime (-7)", () -> Solution.isPrime(-7), false);
        check("even numbers above 2 are not prime (4)", () -> Solution.isPrime(4), false);
        check("even numbers above 2 are not prime (100)", () -> Solution.isPrime(100), false);
        check("squares of primes are not prime (9)", () -> Solution.isPrime(9), false);
        check("squares of primes are not prime (25)", () -> Solution.isPrime(25), false);
        check("squares of primes are not prime (49)", () -> Solution.isPrime(49), false);
        check("larger primes (97)", () -> Solution.isPrime(97), true);
        check("larger primes (7919)", () -> Solution.isPrime(7919), true);
        check("larger primes (1000003)", () -> Solution.isPrime(1000003), true);
        check("next prime is strictly greater (13)", () -> Solution.nextPrime(13), 17);
        check("next prime is strictly greater (2)", () -> Solution.nextPrime(2), 3);
        check("next prime is strictly greater (14)", () -> Solution.nextPrime(14), 17);
        check("next prime from zero is 2", () -> Solution.nextPrime(0), 2);
        check("next prime from one is 2", () -> Solution.nextPrime(1), 2);
        check("next prime from a negative is 2", () -> Solution.nextPrime(-10), 2);
        check("next prime for a large number", () -> Solution.nextPrime(1000000), 1000003);
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
