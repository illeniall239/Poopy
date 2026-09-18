// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
public class Solution {
    public static long binaryToDecimal(String bits) {
        if (bits.length() == 0) {
            throw new IllegalArgumentException("Binary string is empty");
        }
        for (char ch : bits.toCharArray()) {
            if (ch != '0' && ch != '1') {
                throw new IllegalArgumentException("Not a binary string: \"" + bits + "\"");
            }
        }

        long result = 0;
        long placeValue = 1;
        for (int i = bits.length() - 1; i >= 0; i--) {
            if (bits.charAt(i) == '1') {
                result += placeValue;
            }
            placeValue *= 2;
        }
        return result;
    }
}
