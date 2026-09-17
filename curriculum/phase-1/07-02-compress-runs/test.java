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
        check("mixed runs", () -> Solution.compressRuns("aaabcc"), "a3bc2");
        check("no repeats stays the same", () -> Solution.compressRuns("abc"), "abc");
        check("same character in separate runs", () -> Solution.compressRuns("aabbaa"), "a2b2a2");
        check("case-sensitive", () -> Solution.compressRuns("aAA"), "aA2");
        check("empty string", () -> Solution.compressRuns(""), "");
        check("single character", () -> Solution.compressRuns("z"), "z");
        check("last run is included", () -> Solution.compressRuns("abcccc"), "abc4");
        check("run length of two or more digits", () -> Solution.compressRuns("xxxxxxxxxxxxy"), "x12y");
        check("spaces and punctuation are characters too", () -> Solution.compressRuns("hi!!  ok"), "hi!2 2ok");
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
