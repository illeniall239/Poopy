// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
public class Solution {
    public sealed interface Shape permits Circle, Rectangle, Triangle {}
    public record Circle(double radius) implements Shape {}
    public record Rectangle(double width, double height) implements Shape {}
    public record Triangle(double base, double height) implements Shape {}

    public static double area(Shape shape) {
        if (shape instanceof Circle circle) return Math.PI * circle.radius() * circle.radius();
        if (shape instanceof Rectangle rectangle) return rectangle.width() * rectangle.height();
        if (shape instanceof Triangle triangle) return triangle.base() * triangle.height() / 2;
        throw new IllegalArgumentException("Unknown shape: " + shape);
    }
}
