import java.util.ArrayList;
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

    record Person(String name, String team) {}

    public static void main(String[] args) {
        check("groups numbers by parity",
            () -> Solution.groupBy(List.of(1, 2, 3, 4, 5), n -> n % 2 == 0 ? "even" : "odd"),
            Map.of("odd", List.of(1, 3, 5), "even", List.of(2, 4)));
        check("groups objects and keeps input order within each group", () -> {
            List<Person> people = List.of(new Person("Ana", "red"), new Person("Bo", "blue"), new Person("Cy", "red"));
            return Solution.groupBy(people, Person::team);
        }, Map.of(
            "red", List.of(new Person("Ana", "red"), new Person("Cy", "red")),
            "blue", List.of(new Person("Bo", "blue"))));
        check("groups hold the original objects, not copies", () -> {
            Person ana = new Person("Ana", "red");
            Map<String, List<Person>> result = Solution.groupBy(List.of(ana), Person::team);
            return result.get("red").get(0) == ana;
        }, true);
        check("empty input gives an empty map", () -> Solution.groupBy(List.<String>of(), s -> s), Map.of());
        check("every item in one group", () -> Solution.groupBy(List.of("x", "y"), s -> "all"), Map.of("all", List.of("x", "y")));
        check("keyOf is called once per item", () -> {
            int[] calls = { 0 };
            Solution.groupBy(List.of(1, 2, 3), n -> {
                calls[0]++;
                return String.valueOf(n);
            });
            return calls[0];
        }, 3);
        check("does not change the input", () -> {
            List<Integer> items = new ArrayList<>(List.of(3, 1, 2));
            Solution.groupBy(items, n -> String.valueOf(n % 2));
            return items;
        }, List.of(3, 1, 2));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
