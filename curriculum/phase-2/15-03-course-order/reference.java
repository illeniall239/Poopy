// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import java.util.ArrayList;
import java.util.List;

public class Solution {
    public static int[] courseOrder(int numCourses, int[][] prerequisites) {
        List<List<Integer>> unlocks = new ArrayList<>();
        for (int i = 0; i < numCourses; i++) unlocks.add(new ArrayList<>());
        int[] inDegree = new int[numCourses];
        for (int[] p : prerequisites) {
            unlocks.get(p[1]).add(p[0]);
            inDegree[p[0]]++;
        }
        int[] order = new int[numCourses];
        int size = 0;
        for (int c = 0; c < numCourses; c++) if (inDegree[c] == 0) order[size++] = c;
        for (int head = 0; head < size; head++) {
            for (int next : unlocks.get(order[head])) {
                if (--inDegree[next] == 0) order[size++] = next;
            }
        }
        return size == numCourses ? order : new int[0];
    }
}
