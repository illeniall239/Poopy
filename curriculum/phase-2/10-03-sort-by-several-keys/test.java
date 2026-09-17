import java.util.ArrayList;
import java.util.HashSet;
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

    static Solution.Player player(int id, String name, int score) {
        return new Solution.Player(id, name, score);
    }

    static List<Integer> idsOf(List<Solution.Player> players) {
        List<Integer> ids = new ArrayList<>();
        for (Solution.Player p : players) ids.add(p.id);
        return ids;
    }

    static List<Integer> sortedIds(Solution.Player... players) {
        return idsOf(Solution.sortBySeveralKeys(List.of(players)));
    }

    public static void main(String[] args) {
        check("score descending, then name ascending",
            () -> sortedIds(player(1, "cara", 50), player(2, "alex", 80), player(3, "bea", 50)), List.of(2, 3, 1));
        check("names only matter within equal scores",
            () -> sortedIds(player(1, "zed", 90), player(2, "amy", 70), player(3, "bob", 90), player(4, "cat", 70)), List.of(3, 1, 2, 4));
        check("fully equal keys keep their input order", () -> {
            List<Integer> a = sortedIds(player(1, "sam", 10), player(2, "sam", 10), player(3, "sam", 10));
            List<Integer> b = sortedIds(player(5, "kim", 10), player(6, "kim", 20), player(7, "kim", 10));
            return a + "" + b;
        }, "[1, 2, 3][6, 5, 7]");
        check("names compare by character code, upper case first",
            () -> sortedIds(player(1, "alice", 5), player(2, "Bob", 5), player(3, "aaron", 5)), List.of(2, 3, 1));
        check("negative and large scores",
            () -> sortedIds(player(1, "a", -1000000000), player(2, "b", 1000000000), player(3, "c", 0)), List.of(2, 3, 1));
        check("empty and single-element lists", () -> sortedIds() + "" + sortedIds(player(9, "solo", 1)), "[][9]");
        check("returns the same objects in a new list and leaves the input untouched", () -> {
            List<Solution.Player> players = new ArrayList<>(List.of(player(1, "b", 1), player(2, "a", 2)));
            List<Solution.Player> result = Solution.sortBySeveralKeys(players);
            return result != players && result.get(0) == players.get(1) && result.get(1) == players.get(0) && idsOf(players).equals(List.of(1, 2));
        }, true);
        check("200000 records in O(n log n)", () -> {
            int n = 200000;
            List<Solution.Player> players = new ArrayList<>();
            for (int i = 0; i < n; i++) players.add(player(i, "p" + ((i * 7919) % 1000), (int) (((long) i * 104729) % 500)));
            List<Solution.Player> result = Solution.sortBySeveralKeys(players);
            if (result.size() != n || new HashSet<>(idsOf(result)).size() != n) return "wrong size or duplicate ids";
            for (int i = 1; i < n; i++) {
                Solution.Player a = result.get(i - 1), b = result.get(i);
                int byName = a.name.compareTo(b.name);
                boolean ordered = a.score > b.score || (a.score == b.score && (byName < 0 || (byName == 0 && a.id < b.id)));
                if (!ordered) return "records " + (i - 1) + " and " + i + " are out of order";
            }
            return "ok";
        }, "ok");
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
