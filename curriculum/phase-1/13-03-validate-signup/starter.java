import java.util.List;

public class Solution {
    public record SignupForm(String username, String email, String password, String confirmPassword) {}
    public enum Field { USERNAME, EMAIL, PASSWORD, CONFIRM_PASSWORD }
    public record FieldError(Field field, String message) {}

    /** Valid when there are no problems; otherwise Invalid with at most one error per field, in field order. */
    public sealed interface ValidationResult permits Valid, Invalid {}
    public record Valid() implements ValidationResult {}
    public record Invalid(List<FieldError> errors) implements ValidationResult {}

    /**
     * Checks every field and collects the first broken rule of each (rules and messages in exercise.md):
     * username (trimmed): required; 3 to 20 characters; only English letters, digits and '_'.
     * email (trimmed): required; valid (no spaces, exactly one '@', something before it, a '.' after it that is neither first nor last).
     * password (not trimmed): at least 8 characters; a digit; an English letter.
     * confirmPassword: exactly equal to password. Never throws.
     */
    public static ValidationResult validateSignup(SignupForm form) {
        throw new UnsupportedOperationException("Not implemented");
    }
}
