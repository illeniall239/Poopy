// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import java.util.Map;

public class Solution {
    public static Map<String, Integer> makeChange(int cents) {
        int quarters = cents / 25;
        cents %= 25;
        int dimes = cents / 10;
        cents %= 10;
        int nickels = cents / 5;
        int pennies = cents % 5;
        return Map.of("quarters", quarters, "dimes", dimes, "nickels", nickels, "pennies", pennies);
    }
}
