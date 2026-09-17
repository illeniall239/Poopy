import java.util.List;

public class Solution {
    public static class Player {
        public final int id;
        public final String name;
        public final int score;

        public Player(int id, String name, int score) {
            this.id = id;
            this.name = name;
            this.score = score;
        }
    }

    /** Returns a new list of the same players by score descending, then name ascending (String.compareTo), then input order. */
    public static List<Player> sortBySeveralKeys(List<Player> players) {
        throw new UnsupportedOperationException("Not implemented");
    }
}
