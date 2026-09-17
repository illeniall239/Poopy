// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import java.util.OptionalDouble;

public class Solution {
    public static OptionalDouble average(int[] numbers) {
        if (numbers.length == 0) {
            return OptionalDouble.empty();
        }
        double total = 0;
        for (int i = 0; i < numbers.length; i++) {
            total += numbers[i];
        }
        return OptionalDouble.of(total / numbers.length);
    }
}
