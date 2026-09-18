// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export function shortestPath(n: number, edges: [number, number][], start: number, end: number): number {
  const neighbors: number[][] = Array.from({ length: n }, () => []);
  for (const [a, b] of edges) {
    neighbors[a].push(b);
    neighbors[b].push(a);
  }
  const distance = new Array<number>(n).fill(-1);
  distance[start] = 0;
  const queue = [start];
  for (let head = 0; head < queue.length; head++) {
    const node = queue[head];
    if (node === end) return distance[node];
    for (const next of neighbors[node]) {
      if (distance[next] !== -1) continue;
      distance[next] = distance[node] + 1;
      queue.push(next);
    }
  }
  return -1;
}
