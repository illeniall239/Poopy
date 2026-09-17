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
        check("pairs side by side", () -> Solution.isBalanced("()[]{}"), true);
        check("pairs nested inside each other", () -> Solution.isBalanced("{[()]}"), true);
        check("wrong kind of closing bracket", () -> Solution.isBalanced("(]"), false);
        check("pairs that cross instead of nesting", () -> Solution.isBalanced("([)]"), false);
        check("opening brackets never closed", () -> Solution.isBalanced("(("), false);
        check("closing bracket with nothing open", () -> List.of(Solution.isBalanced("())"), Solution.isBalanced(")")), List.of(false, false));
        check("other characters are ignored", () -> List.of(Solution.isBalanced("f(a[0]) { x; }"), Solution.isBalanced("abc")), List.of(true, true));
        check("empty string is balanced", () -> Solution.isBalanced(""), true);
        check("200000 levels deep in O(n)", () -> {
            int n = 200000;
            String deep = "([{".repeat(n / 2).substring(0, n);
            StringBuilder close = new StringBuilder();
            for (int i = n - 1; i >= 0; i--) {
                char c = deep.charAt(i);
                close.append(c == '(' ? ')' : c == '[' ? ']' : '}');
            }
            return List.of(Solution.isBalanced(deep + close), Solution.isBalanced(deep + close.substring(1)));
        }, List.of(true, false));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
