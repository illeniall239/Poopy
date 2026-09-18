// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import java.util.List;
import java.util.Optional;

public class Solution {
    public record Student(String name, Integer score) {}

    public static Optional<Double> averageScore(List<Student> students) {
        double sum = 0;
        int count = 0;
        for (Student student : students) {
            if (student.score() != null) {
                sum += student.score();
                count++;
            }
        }
        return count == 0 ? Optional.empty() : Optional.of(sum / count);
    }
}
