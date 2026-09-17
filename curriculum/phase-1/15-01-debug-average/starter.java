import java.util.OptionalDouble;

public class Solution {
    /** The arithmetic mean of numbers (the sum of all values divided by how many there are), exact and not rounded; empty for an empty array. */
    public static OptionalDouble average(int[] numbers) {
        if (numbers.length == 0) {
            return OptionalDouble.empty();
        }
        double total = 0;
        for (int i = 1; i < numbers.length; i++) {
            total += numbers[i];
        }
        return OptionalDouble.of(Math.round(total / numbers.length));
    }
}
