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
        check("first character is unique", () -> Solution.firstUniqueIndex("leetcode"), 0);
        check("unique character in the middle", () -> Solution.firstUniqueIndex("loveleetcode"), 2);
        check("no unique character", () -> Solution.firstUniqueIndex("aabb"), -1);
        check("empty string", () -> Solution.firstUniqueIndex(""), -1);
        check("case-sensitive (aA)", () -> Solution.firstUniqueIndex("aA"), 0);
        check("case-sensitive (aAa)", () -> Solution.firstUniqueIndex("aAa"), 1);
        check("a character that repeats later is not unique", () -> Solution.firstUniqueIndex("abcabd"), 2);
        check("unique character at the end", () -> Solution.firstUniqueIndex("xyxyz"), 4);
        check("spaces count as characters", () -> Solution.firstUniqueIndex("aa bb"), 2);
        check("long string is handled quickly", () -> {
            StringBuilder text = new StringBuilder();
            for (int i = 0; i < 50000; i++) text.append("ab");
            return Solution.firstUniqueIndex(text.append("c").toString());
        }, 100000);
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
