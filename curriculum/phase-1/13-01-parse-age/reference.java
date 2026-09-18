// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
public class Solution {
    public static int parseAge(String input) {
        String text = input.trim();
        if (text.isEmpty()) throw new IllegalArgumentException("Age is empty");
        for (char ch : text.toCharArray()) {
            if (ch < '0' || ch > '9') throw new NumberFormatException("Age must be a whole number, got \"" + input + "\"");
        }
        int age = Integer.parseInt(text);
        if (age > 150) throw new IllegalArgumentException("Age must be between 0 and 150, got " + age);
        return age;
    }
}
