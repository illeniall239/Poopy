import java.util.HashMap;
import java.util.List;
import java.util.Map;
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
        check("entry that calls nothing is one frame",
            () -> Solution.maxCallDepth(Map.of("main", List.of()), "main"), 1);
        check("a chain of nested calls",
            () -> Solution.maxCallDepth(Map.of("main", List.of("parse"), "parse", List.of("readFile")), "main"), 3);
        check("calls made one after another don't stack up",
            () -> Solution.maxCallDepth(Map.of("main", List.of("log", "log", "save"), "save", List.of()), "main"), 2);
        check("picks the deepest branch",
            () -> Solution.maxCallDepth(Map.of("main", List.of("a", "b"), "a", List.of(), "b", List.of("c"), "c", List.of("d")), "main"), 4);
        check("a shared helper reached twice is not recursion",
            () -> Solution.maxCallDepth(Map.of("main", List.of("a", "b"), "a", List.of("util"), "b", List.of("util"), "util", List.of()), "main"), 3);
        check("a function calling itself recurses forever",
            () -> Solution.maxCallDepth(Map.of("main", List.of("loop"), "loop", List.of("loop")), "main"), -1);
        check("mutual recursion off the deepest path recurses forever",
            () -> Solution.maxCallDepth(Map.of("main", List.of("deep", "isEven"), "deep", List.of("x"), "x", List.of("y"), "y", List.of("z"),
                "isEven", List.of("isOdd"), "isOdd", List.of("isEven")), "main"), -1);
        check("a cycle that entry never reaches doesn't matter",
            () -> Solution.maxCallDepth(Map.of("main", List.of("a"), "a", List.of(), "b", List.of("c"), "c", List.of("b")), "main"), 2);
        check("300 layers of shared helpers finish quickly", () -> {
            int layers = 300;
            Map<String, List<String>> calls = new HashMap<>();
            for (int i = 0; i < layers; i++) {
                calls.put("f" + i, List.of("a" + i, "b" + i));
                calls.put("a" + i, List.of("f" + (i + 1)));
                calls.put("b" + i, List.of("f" + (i + 1)));
            }
            return Solution.maxCallDepth(calls, "f0");
        }, 601);
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
