// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
public class Solution {
    public static double celsiusToFahrenheit(double celsius) {
        return Math.round((celsius * 9 / 5 + 32) * 10) / 10.0;
    }

    public static double fahrenheitToCelsius(double fahrenheit) {
        return Math.round((fahrenheit - 32) * 5 / 9 * 10) / 10.0;
    }
}
