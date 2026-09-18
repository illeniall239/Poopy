// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import java.util.PriorityQueue;

public class Solution {
    public static int[] mergeKSorted(int[][] arrays) {
        int total = 0;
        // Each entry is {value, array index, element index}.
        PriorityQueue<int[]> heap = new PriorityQueue<>((x, y) -> Integer.compare(x[0], y[0]));
        for (int a = 0; a < arrays.length; a++) {
            total += arrays[a].length;
            if (arrays[a].length > 0) heap.add(new int[] {arrays[a][0], a, 0});
        }
        int[] out = new int[total];
        int n = 0;
        while (!heap.isEmpty()) {
            int[] e = heap.poll();
            out[n++] = e[0];
            int next = e[2] + 1;
            if (next < arrays[e[1]].length) heap.add(new int[] {arrays[e[1]][next], e[1], next});
        }
        return out;
    }
}
