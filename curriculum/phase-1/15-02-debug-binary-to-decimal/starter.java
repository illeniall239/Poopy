public class Solution {
    /**
     * Converts a string of binary digits to the number it represents: the rightmost character is worth 1, the next one to the
     * left 2, then 4, 8 and so on. Leading zeros are allowed. An empty string throws IllegalArgumentException("Binary string is empty");
     * any character other than '0' or '1' throws IllegalArgumentException("Not a binary string: \"<bits>\"").
     */
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
        for (int i = bits.length() - 1; i > 0; i--) {
            if (bits.charAt(i) == '1') {
                result += placeValue;
            }
            placeValue *= 2;
        }
        return result;
    }
}
