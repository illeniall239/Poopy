// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Solution {
    public static int shortestPath(int n, int[][] edges, int start, int end) {
        List<List<Integer>> neighbors = new ArrayList<>();
        for (int i = 0; i < n; i++) neighbors.add(new ArrayList<>());
        for (int[] e : edges) {
            neighbors.get(e[0]).add(e[1]);
            neighbors.get(e[1]).add(e[0]);
        }
        int[] distance = new int[n];
        Arrays.fill(distance, -1);
        distance[start] = 0;
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        queue.add(start);
        while (!queue.isEmpty()) {
            int node = queue.poll();
            if (node == end) return distance[node];
            for (int next : neighbors.get(node)) {
                if (distance[next] != -1) continue;
                distance[next] = distance[node] + 1;
                queue.add(next);
            }
        }
        return -1;
    }
}
