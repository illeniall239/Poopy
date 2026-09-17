import java.util.List;
import java.util.Optional;

public class Solution {
    /** A student's score is null when they haven't taken the test yet. A score of 0 is a real score. */
    public record Student(String name, Integer score) {}

    /** Average of all present (non-null) scores, not rounded; empty when there are no present scores. Does not change the input. */
    public static Optional<Double> averageScore(List<Student> students) {
        throw new UnsupportedOperationException("Not implemented");
    }
}
