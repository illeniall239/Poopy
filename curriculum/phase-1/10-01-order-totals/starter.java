import java.util.List;
import java.util.Map;

public class Solution {
    public record Order(String customer, int amountCents) {}

    /** Sum of every amountCents, using a stream reduction instead of a loop; no orders total 0. */
    public static int grandTotal(List<Order> orders) {
        throw new UnsupportedOperationException("Not implemented");
    }

    /** Each customer (case-sensitive) mapped to the sum of their orders, keys in order of first appearance; no orders give an empty map. Uses streams, not loops. */
    public static Map<String, Integer> totalsByCustomer(List<Order> orders) {
        throw new UnsupportedOperationException("Not implemented");
    }
}
