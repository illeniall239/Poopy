// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import java.util.Arrays;
import java.util.Optional;

public class Solution {
    public enum Direction { UP, DOWN, LEFT, RIGHT }

    public sealed interface ParseResult permits Move, Say, Quit, ParseError {}
    public record Move(Direction direction, int steps) implements ParseResult {}
    public record Say(String message) implements ParseResult {}
    public record Quit() implements ParseResult {}
    public record ParseError(String message) implements ParseResult {}

    private static Optional<Direction> toDirection(String word) {
        return switch (word.toLowerCase()) {
            case "up" -> Optional.of(Direction.UP);
            case "down" -> Optional.of(Direction.DOWN);
            case "left" -> Optional.of(Direction.LEFT);
            case "right" -> Optional.of(Direction.RIGHT);
            default -> Optional.empty();
        };
    }

    private static Optional<Integer> toSteps(String word) {
        for (char ch : word.toCharArray()) {
            if (ch < '0' || ch > '9') return Optional.empty();
        }
        int steps = Integer.parseInt(word);
        return steps >= 1 ? Optional.of(steps) : Optional.empty();
    }

    public static ParseResult parseCommand(String input) {
        if (input.isBlank()) return new ParseError("Empty command");
        String[] words = input.trim().split(" +");

        String name = words[0].toLowerCase();
        if (name.equals("quit")) {
            return words.length == 1 ? new Quit() : new ParseError("quit takes no arguments");
        }
        if (name.equals("say")) {
            if (words.length < 2) return new ParseError("say needs a message");
            return new Say(String.join(" ", Arrays.copyOfRange(words, 1, words.length)));
        }
        if (name.equals("move")) {
            if (words.length != 3) return new ParseError("Usage: move <direction> <steps>");
            Optional<Direction> direction = toDirection(words[1]);
            if (direction.isEmpty()) return new ParseError("Unknown direction \"" + words[1] + "\"");
            Optional<Integer> steps = toSteps(words[2]);
            if (steps.isEmpty()) return new ParseError("Steps must be a whole number of at least 1, got \"" + words[2] + "\"");
            return new Move(direction.get(), steps.get());
        }
        return new ParseError("Unknown command \"" + words[0] + "\"");
    }
}
