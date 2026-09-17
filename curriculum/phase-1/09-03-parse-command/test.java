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

    /** True when every input parses to a ParseError with a non-empty message. */
    static boolean allErrors(String... inputs) {
        for (String input : inputs) {
            Solution.ParseResult result = Solution.parseCommand(input);
            if (!(result instanceof Solution.ParseError error) || error.message().isEmpty()) {
                System.out.println("    expected an error with a message for \"" + input + "\", got " + result);
                return false;
            }
        }
        return true;
    }

    public static void main(String[] args) {
        check("move command", () -> Solution.parseCommand("move up 3"), new Solution.Move(Solution.Direction.UP, 3));
        check("extra spaces and mixed case",
            () -> List.of(Solution.parseCommand("  MOVE   Left 10 "), Solution.parseCommand("Move DOWN 007")),
            List.of(new Solution.Move(Solution.Direction.LEFT, 10), new Solution.Move(Solution.Direction.DOWN, 7)));
        check("say joins words with single spaces and keeps their case",
            () -> List.of(Solution.parseCommand("say Hello   there"), Solution.parseCommand(" SAY move up 3 ")),
            List.of(new Solution.Say("Hello there"), new Solution.Say("move up 3")));
        check("quit",
            () -> List.of(Solution.parseCommand("quit"), Solution.parseCommand("  QUIT ")),
            List.of(new Solution.Quit(), new Solution.Quit()));
        check("bad direction is an error", () -> allErrors("move north 2", "move Upward 2"), true);
        check("steps must be whole digits and at least 1",
            () -> allErrors("move up 0", "move up -1", "move up 2.5", "move up two", "move up 3x"), true);
        check("wrong number of words is an error", () -> allErrors("move up", "move up 2 3", "say", "say   ", "quit now"), true);
        check("empty and unknown input is an error", () -> allErrors("", "    ", "jump 3"), true);
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
