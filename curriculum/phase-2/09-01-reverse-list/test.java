import java.util.ArrayList;
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
            String shown = String.valueOf(value);
            System.out.println("FAIL - " + name + "\n    expected: " + expected + "\n    got:      " + (shown.length() > 300 ? shown.substring(0, 300) + "..." : shown));
        }
    }

    static Solution.ListNode[] nodesOf(int... values) {
        Solution.ListNode[] nodes = new Solution.ListNode[values.length];
        for (int i = 0; i < values.length; i++) nodes[i] = new Solution.ListNode(values[i]);
        for (int i = 0; i + 1 < nodes.length; i++) nodes[i].next = nodes[i + 1];
        return nodes;
    }

    static Solution.ListNode fromArray(int... values) {
        Solution.ListNode[] nodes = nodesOf(values);
        return nodes.length == 0 ? null : nodes[0];
    }

    /** Walks at most `limit` nodes so a list that accidentally loops can't hang the test. */
    static List<Integer> toList(Solution.ListNode head, int limit) {
        List<Integer> values = new ArrayList<>();
        for (Solution.ListNode node = head; node != null && values.size() < limit; node = node.next) values.add(node.val);
        return values;
    }

    static List<Integer> toList(Solution.ListNode head) {
        return toList(head, 2000000);
    }

    public static void main(String[] args) {
        check("reverses five nodes", () -> toList(Solution.reverseList(fromArray(1, 2, 3, 4, 5))), List.of(5, 4, 3, 2, 1));
        check("reverses two nodes", () -> toList(Solution.reverseList(fromArray(1, 2))), List.of(2, 1));
        check("one node returns the same node", () -> {
            Solution.ListNode node = new Solution.ListNode(7);
            return Solution.reverseList(node) == node && node.next == null;
        }, true);
        check("empty list returns null", () -> Solution.reverseList(null) == null, true);
        check("repeated values", () -> toList(Solution.reverseList(fromArray(1, 1, 2, 3, 3))), List.of(3, 3, 2, 1, 1));
        check("reuses the original nodes and ends at the old head", () -> {
            Solution.ListNode[] nodes = nodesOf(10, 20, 30, 40);
            Solution.ListNode node = Solution.reverseList(nodes[0]);
            List<Boolean> same = new ArrayList<>();
            for (int i = 3; i >= 0; i--) {
                same.add(node == nodes[i]);
                node = node == null ? null : node.next;
            }
            same.add(node == null);
            same.add(nodes[0].next == null);
            return same;
        }, List.of(true, true, true, true, true, true));
        check("200000 nodes without recursion in O(n)", () -> {
            int n = 200000;
            int[] values = new int[n];
            List<Integer> expected = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                values[i] = i;
                expected.add(n - 1 - i);
            }
            return toList(Solution.reverseList(fromArray(values)), n + 1).equals(expected);
        }, true);
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
