// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
public class Solution {
    private static String repeat(String symbol, int times) {
        String result = "";
        for (int i = 0; i < times; i++) result += symbol;
        return result;
    }

    private static String digitToRoman(int digit, String one, String five, String ten) {
        if (digit == 9) return one + ten;
        if (digit >= 5) return five + repeat(one, digit - 5);
        if (digit == 4) return one + five;
        return repeat(one, digit);
    }

    public static String toRoman(double n) {
        if (Math.floor(n) != n || n < 1 || n > 3999) return "";
        int whole = (int) n;
        return repeat("M", whole / 1000)
            + digitToRoman(whole / 100 % 10, "C", "D", "M")
            + digitToRoman(whole / 10 % 10, "X", "L", "C")
            + digitToRoman(whole % 10, "I", "V", "X");
    }
}
