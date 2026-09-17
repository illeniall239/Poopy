// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import java.util.ArrayDeque;

public class Solution {
    public static int countIslands(String[] grid) {
        int rows = grid.length;
        if (rows == 0) return 0;
        int cols = grid[0].length();
        boolean[] visited = new boolean[rows * cols];
        int[][] steps = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
        int islands = 0;
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (grid[r].charAt(c) != '1' || visited[r * cols + c]) continue;
                islands++;
                visited[r * cols + c] = true;
                stack.push(r * cols + c);
                while (!stack.isEmpty()) {
                    int cell = stack.pop();
                    int cr = cell / cols, cc = cell % cols;
                    for (int[] s : steps) {
                        int nr = cr + s[0], nc = cc + s[1];
                        if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                        if (grid[nr].charAt(nc) != '1' || visited[nr * cols + nc]) continue;
                        visited[nr * cols + nc] = true;
                        stack.push(nr * cols + nc);
                    }
                }
            }
        }
        return islands;
    }
}
