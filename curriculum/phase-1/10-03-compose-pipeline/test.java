import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.function.IntUnaryOperator;
import java.util.function.Supplier;

public class SolutionTest {
    static int passed = 0, failed = 0;

    static void check(String name, Supplier<Object> got, Object expected) {
        Object value;
        try {
            value = got.get();
        } catch (Throwable t) {
            failed++;
            System.out.println("FAIL - " + name + "\n    threw:    " + t);
            return;
        }
        if (Objects.deepEquals(value, expected)) {
            passed++;
            System.out.println("ok - " + name);
        } else {
            failed++;
            System.out.println("FAIL - " + name + "\n    expected: " + expected + "\n    got:      " + value);
        }
    }

    static final IntUnaryOperator addOne = n -> n + 1;
    static final IntUnaryOperator twice = n -> n * 2;

    public static void main(String[] args) {
        check("runs steps left to right",
            () -> List.of(Solution.pipeline(List.of(addOne, twice)).applyAsInt(3), Solution.pipeline(List.of(twice, addOne)).applyAsInt(3)),
            List.of(8, 7));
        check("no steps returns the input unchanged", () -> Solution.pipeline(List.of()).applyAsInt(42), 42);
        check("each step runs exactly once per call", () -> {
            int[] calls = { 0 };
            IntUnaryOperator counted = n -> {
                calls[0]++;
                return n;
            };
            Solution.pipeline(List.of(counted, addOne, counted)).applyAsInt(0);
            return calls[0];
        }, 2);
        check("the returned step can be reused", () -> {
            IntUnaryOperator run = Solution.pipeline(List.of(addOne, twice));
            return List.of(run.applyAsInt(1), run.applyAsInt(1), run.applyAsInt(10));
        }, List.of(4, 4, 22));
        check("changing the steps list afterwards has no effect", () -> {
            List<IntUnaryOperator> steps = new ArrayList<>(List.of(addOne));
            IntUnaryOperator run = Solution.pipeline(steps);
            steps.add(twice);
            return run.applyAsInt(5);
        }, 6);
        check("when runs the step only if the predicate holds", () -> {
            IntUnaryOperator halveEvens = Solution.when(n -> n % 2 == 0, n -> n / 2);
            return List.of(halveEvens.applyAsInt(10), halveEvens.applyAsInt(7));
        }, List.of(5, 7));
        check("pipelines and when combine", () -> {
            IntUnaryOperator halveEvens = Solution.when(n -> n % 2 == 0, n -> n / 2);
            return List.of(
                Solution.pipeline(List.of(addOne, halveEvens, twice)).applyAsInt(5),
                Solution.pipeline(List.of(Solution.pipeline(List.of(addOne, addOne)), twice)).applyAsInt(1));
        }, List.of(6, 6));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
