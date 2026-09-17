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

    /** Builds linked nodes holding 1..count; if loopTo >= 0, the last node points back to nodes[loopTo]. */
    static Solution.ListNode[] nodesOf(int count, int loopTo) {
        Solution.ListNode[] nodes = new Solution.ListNode[count];
        for (int i = 0; i < count; i++) nodes[i] = new Solution.ListNode(i + 1);
        for (int i = 0; i + 1 < count; i++) nodes[i].next = nodes[i + 1];
        if (loopTo >= 0) nodes[count - 1].next = nodes[loopTo];
        return nodes;
    }

    public static void main(String[] args) {
        check("middle of an odd-length list", () -> {
            Solution.ListNode[] nodes = nodesOf(5, -1);
            return Solution.middleNode(nodes[0]) == nodes[2];
        }, true);
        check("middle of an even-length list is the second middle node", () -> {
            Solution.ListNode[] nodes = nodesOf(6, -1);
            Solution.ListNode[] two = nodesOf(2, -1);
            return List.of(Solution.middleNode(nodes[0]) == nodes[3], Solution.middleNode(two[0]) == two[1]);
        }, List.of(true, true));
        check("middle of one node and of an empty list", () -> {
            Solution.ListNode[] one = nodesOf(1, -1);
            return List.of(Solution.middleNode(one[0]) == one[0], Solution.middleNode(null) == null);
        }, List.of(true, true));
        check("list ending in null has no cycle", () -> List.of(
            Solution.hasCycle(nodesOf(4, -1)[0]), Solution.hasCycle(nodesOf(1, -1)[0]), Solution.hasCycle(null)),
            List.of(false, false, false));
        check("last node pointing back into the list is a cycle", () -> List.of(
            Solution.hasCycle(nodesOf(4, 1)[0]), Solution.hasCycle(nodesOf(4, 0)[0]), Solution.hasCycle(nodesOf(2, 1)[0])),
            List.of(true, true, true));
        check("a node pointing to itself is a cycle", () -> Solution.hasCycle(nodesOf(1, 0)[0]), true);
        check("neither function changes the nodes", () -> {
            Solution.ListNode[] nodes = nodesOf(4, 2);
            Solution.hasCycle(nodes[0]);
            Solution.ListNode[] plain = nodesOf(3, -1);
            Solution.middleNode(plain[0]);
            return List.of(
                nodes[0].val == 1 && nodes[1].val == 2 && nodes[2].val == 3 && nodes[3].val == 4,
                nodes[0].next == nodes[1] && nodes[1].next == nodes[2] && nodes[2].next == nodes[3] && nodes[3].next == nodes[2],
                plain[0].val == 1 && plain[1].val == 2 && plain[2].val == 3,
                plain[0].next == plain[1] && plain[1].next == plain[2] && plain[2].next == null);
        }, List.of(true, true, true, true));
        check("1000000 nodes in O(n)", () -> {
            int n = 1000000;
            Solution.ListNode[] nodes = nodesOf(n, -1);
            boolean middle = Solution.middleNode(nodes[0]) == nodes[n / 2];
            boolean noCycle = Solution.hasCycle(nodes[0]);
            nodes[n - 1].next = nodes[n / 2];
            return List.of(middle, noCycle, Solution.hasCycle(nodes[0]));
        }, List.of(true, false, true));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
