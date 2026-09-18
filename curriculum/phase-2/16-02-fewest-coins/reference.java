// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import java.util.Arrays;

public class Solution {
    public static int fewestCoins(int[] coins, int amount) {
        final int UNREACHABLE = Integer.MAX_VALUE;
        int[] fewest = new int[amount + 1];
        Arrays.fill(fewest, UNREACHABLE);
        fewest[0] = 0;
        for (int x = 1; x <= amount; x++) {
            for (int c : coins) {
                if (c <= x && fewest[x - c] != UNREACHABLE && fewest[x - c] + 1 < fewest[x]) fewest[x] = fewest[x - c] + 1;
            }
        }
        return fewest[amount] == UNREACHABLE ? -1 : fewest[amount];
    }
}
