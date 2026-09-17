// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
public class Solution {
    public static int[] daysUntilWarmer(int[] temps) {
        int[] answer = new int[temps.length];
        int[] waiting = new int[temps.length];
        int top = 0;
        for (int i = 0; i < temps.length; i++) {
            while (top > 0 && temps[waiting[top - 1]] < temps[i]) {
                int day = waiting[--top];
                answer[day] = i - day;
            }
            waiting[top++] = i;
        }
        return answer;
    }
}
