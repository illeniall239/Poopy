import java.util.List;
import java.util.Objects;
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

    public static void main(String[] args) {
        check("padding before a larger field", () -> Solution.recordSize(List.of("i8", "i32")), 8);
        check("padding at the end rounds to the largest field",
            () -> List.of(Solution.recordSize(List.of("i32", "i8")), Solution.recordSize(List.of("bool", "i16"))), List.of(8, 4));
        check("field order changes the size",
            () -> List.of(Solution.recordSize(List.of("i8", "i64", "i8")), Solution.recordSize(List.of("i64", "i8", "i8"))), List.of(24, 16));
        check("one-byte fields need no padding", () -> Solution.recordSize(List.of("i8", "bool", "i8")), 3);
        check("empty record has size 0", () -> Solution.recordSize(List.of()), 0);
        check("mixed field types",
            () -> List.of(Solution.recordSize(List.of("ptr", "f32", "f64", "i16")), Solution.recordSize(List.of("i16", "i8", "i32", "i8"))),
            List.of(32, 12));
        check("array of records includes each record's padding",
            () -> List.of(Solution.arraySize(List.of("i32", "i8"), 1000), Solution.arraySize(List.of("i8", "i16", "i8"), 3)),
            List.of(8000, 18));
        check("empty arrays and empty records use no bytes",
            () -> List.of(Solution.arraySize(List.of("i64"), 0), Solution.arraySize(List.of(), 5), Solution.arraySize(List.of("f64", "i8"), 10000000)),
            List.of(0, 0, 160000000));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
