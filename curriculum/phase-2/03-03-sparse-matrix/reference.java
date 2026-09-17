// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Solution {
    public static class SparseMatrix {
        private final List<Map<Integer, Integer>> cells;
        private int count = 0;

        public SparseMatrix(int rows, int cols) {
            cells = new ArrayList<>(rows);
            for (int r = 0; r < rows; r++) cells.add(new HashMap<>());
        }

        public void set(int row, int col, int value) {
            Map<Integer, Integer> rowCells = cells.get(row);
            if (value == 0) {
                if (rowCells.remove(col) != null) count--;
                return;
            }
            if (rowCells.put(col, value) == null) count++;
        }

        public int get(int row, int col) {
            return cells.get(row).getOrDefault(col, 0);
        }

        public int nonZeroCount() {
            return count;
        }

        public long[] multiplyVector(int[] vector) {
            long[] result = new long[cells.size()];
            for (int r = 0; r < result.length; r++) {
                for (Map.Entry<Integer, Integer> cell : cells.get(r).entrySet()) {
                    result[r] += (long) cell.getValue() * vector[cell.getKey()];
                }
            }
            return result;
        }
    }
}
