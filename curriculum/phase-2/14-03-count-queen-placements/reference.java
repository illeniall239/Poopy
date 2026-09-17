// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
public class Solution {
    public static int countQueens(int n) {
        return place(n, 0, new boolean[n], new boolean[2 * n], new boolean[2 * n]);
    }

    private static int place(int n, int row, boolean[] cols, boolean[] down, boolean[] up) {
        if (row == n) return 1;
        int count = 0;
        for (int col = 0; col < n; col++) {
            int d = row - col + n, u = row + col;
            if (cols[col] || down[d] || up[u]) continue;
            cols[col] = down[d] = up[u] = true;
            count += place(n, row + 1, cols, down, up);
            cols[col] = down[d] = up[u] = false;
        }
        return count;
    }
}
