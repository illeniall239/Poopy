// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
public class Solution {
    public record Split(int shareCents, int peopleWithExtraCent) {}

    public static Split splitBill(double totalDollars, int people) {
        int totalCents = (int) Math.round(totalDollars * 100);
        return new Split(totalCents / people, totalCents % people);
    }
}
