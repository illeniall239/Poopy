// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
public class Solution {
    public static String triangleKind(int a, int b, int c) {
        boolean positive = a > 0 && b > 0 && c > 0;
        boolean closes = a + b > c && a + c > b && b + c > a;
        if (!positive || !closes) return "invalid";
        if (a == b && b == c) return "equilateral";
        if (a == b || b == c || a == c) return "isosceles";
        return "scalene";
    }
}
