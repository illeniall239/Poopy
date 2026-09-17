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

    static Solution.Order order(String customer, int amountCents) {
        return new Solution.Order(customer, amountCents);
    }

    static final List<Solution.Order> orders = List.of(order("ana", 1200), order("ben", 500), order("ana", 300));

    public static void main(String[] args) {
        check("grand total adds every order", () -> Solution.grandTotal(orders), 2000);
        check("grand total of no orders is 0", () -> Solution.grandTotal(List.of()), 0);
        check("totals are grouped per customer", () -> Solution.totalsByCustomer(orders), Map.of("ana", 1500, "ben", 500));
        check("customers appear in order of first appearance", () -> {
            Map<String, Integer> result = Solution.totalsByCustomer(List.of(order("zoe", 1), order("adam", 2), order("zoe", 3)));
            return new ArrayList<>(result.keySet());
        }, List.of("zoe", "adam"));
        check("no orders gives an empty Map", () -> Solution.totalsByCustomer(List.of()), Map.of());
        check("customer names are case-sensitive and zero amounts still count",
            () -> Solution.totalsByCustomer(List.of(order("Ana", 0), order("ana", 100))),
            Map.of("Ana", 0, "ana", 100));
        check("does not change the input", () -> {
            List<Solution.Order> input = new ArrayList<>(List.of(order("ana", 1200), order("ana", 300)));
            Solution.grandTotal(input);
            Solution.totalsByCustomer(input);
            return input;
        }, List.of(order("ana", 1200), order("ana", 300)));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
