// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
public class Solution {
    public record Seat(int row, int column) {}

    public static Seat findSeat(int seatNumber, int seatsPerRow) {
        int index = seatNumber - 1;
        return new Seat(index / seatsPerRow + 1, index % seatsPerRow + 1);
    }
}
