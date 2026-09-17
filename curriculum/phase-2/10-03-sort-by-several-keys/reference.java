// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import java.util.ArrayList;
import java.util.Comparator;
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

    public static List<Player> sortBySeveralKeys(List<Player> players) {
        List<Player> sorted = new ArrayList<>(players);
        sorted.sort(Comparator.comparingInt((Player p) -> p.score).reversed().thenComparing(p -> p.name));
        return sorted;
    }
}
