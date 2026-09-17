// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import java.util.List;
import java.util.Map;

public class Solution {
    private static final Map<String, Integer> SIZES = Map.of(
        "bool", 1, "i8", 1, "i16", 2, "i32", 4, "f32", 4, "i64", 8, "f64", 8, "ptr", 8);

    private static int roundUp(int offset, int multiple) {
        return (offset + multiple - 1) / multiple * multiple;
    }

    public static int recordSize(List<String> fields) {
        int offset = 0;
        int largest = 1;
        for (String field : fields) {
            int size = SIZES.get(field);
            offset = roundUp(offset, size) + size;
            largest = Math.max(largest, size);
        }
        return roundUp(offset, largest);
    }

    public static int arraySize(List<String> fields, int count) {
        return recordSize(fields) * count;
    }
}
