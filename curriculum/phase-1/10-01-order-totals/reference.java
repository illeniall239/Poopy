// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class Solution {
    public record Order(String customer, int amountCents) {}

    public static int grandTotal(List<Order> orders) {
        return orders.stream().map(Order::amountCents).reduce(0, Integer::sum);
    }

    public static Map<String, Integer> totalsByCustomer(List<Order> orders) {
        return orders.stream().collect(
            Collectors.groupingBy(Order::customer, LinkedHashMap::new, Collectors.summingInt(Order::amountCents)));
    }
}
