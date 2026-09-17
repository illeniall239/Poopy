public class Solution {
    public enum Direction { UP, DOWN, LEFT, RIGHT }

    /** The result of parsing: exactly one of the three commands, or a ParseError with a non-empty message. */
    public sealed interface ParseResult permits Move, Say, Quit, ParseError {}
    public record Move(Direction direction, int steps) implements ParseResult {}
    public record Say(String message) implements ParseResult {}
    public record Quit() implements ParseResult {}
    public record ParseError(String message) implements ParseResult {}

    /** Parses "move <direction> <steps>", "say <words...>" or "quit" (keywords case-insensitive, extra spaces ignored); anything else is a ParseError. */
    public static ParseResult parseCommand(String input) {
        throw new UnsupportedOperationException("Not implemented");
    }
}
