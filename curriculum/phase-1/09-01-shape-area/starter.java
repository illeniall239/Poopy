public class Solution {
    /** A shape is exactly one of these kinds, each carrying only the fields that make sense for it. */
    public sealed interface Shape permits Circle, Rectangle, Triangle {}
    public record Circle(double radius) implements Shape {}
    public record Rectangle(double width, double height) implements Shape {}
    public record Triangle(double base, double height) implements Shape {}

    /** Area of the shape: circle Math.PI * r * r, rectangle width * height, triangle base * height / 2. Not rounded. */
    public static double area(Shape shape) {
        throw new UnsupportedOperationException("Not implemented");
    }
}
