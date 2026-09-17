import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
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

    static Solution.Student s(String name, Integer score) {
        return new Solution.Student(name, score);
    }

    public static void main(String[] args) {
        check("all scores present", () -> Solution.averageScore(List.of(s("Ana", 80), s("Ben", 90))), Optional.of(85.0));
        check("absent score is skipped, not counted as zero", () -> Solution.averageScore(List.of(s("Ana", 80), s("Ben", null))), Optional.of(80.0));
        check("a score of 0 counts", () -> Solution.averageScore(List.of(s("Ana", 0), s("Ben", 10))), Optional.of(5.0));
        check("null scores are skipped",
            () -> Solution.averageScore(List.of(s("Ana", null), s("Ben", 40), s("Cy", null), s("Di", 60))),
            Optional.of(50.0));
        check("no present scores gives empty", () -> Solution.averageScore(List.of(s("Ana", null), s("Ben", null))), Optional.empty());
        check("empty list gives empty", () -> Solution.averageScore(List.of()), Optional.empty());
        check("result is not rounded", () -> Solution.averageScore(List.of(s("Ana", 1), s("Ben", 2))), Optional.of(1.5));
        check("all zeros averages to 0, not empty", () -> Solution.averageScore(List.of(s("Ana", 0))), Optional.of(0.0));
        check("does not modify the input", () -> {
            List<Solution.Student> students = new ArrayList<>(List.of(s("Ana", 70), s("Ben", null)));
            Solution.averageScore(students);
            return students;
        }, List.of(s("Ana", 70), s("Ben", null)));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
