// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
public class Solution {
    public static int shippingCost(int subtotalCents, double weightKg, boolean express) {
        if (weightKg > 30) return -1;
        if (subtotalCents >= 5000 && !express && weightKg <= 20) return 0;

        int cost;
        if (weightKg <= 1) cost = 499;
        else if (weightKg <= 5) cost = 899;
        else cost = 1499;

        return express ? cost + 1000 : cost;
    }
}
