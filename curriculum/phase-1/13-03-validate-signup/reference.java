// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import java.util.ArrayList;
import java.util.List;

public class Solution {
    public record SignupForm(String username, String email, String password, String confirmPassword) {}
    public enum Field { USERNAME, EMAIL, PASSWORD, CONFIRM_PASSWORD }
    public record FieldError(Field field, String message) {}

    public sealed interface ValidationResult permits Valid, Invalid {}
    public record Valid() implements ValidationResult {}
    public record Invalid(List<FieldError> errors) implements ValidationResult {}

    private static boolean isLetter(char ch) {
        return (ch >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z');
    }

    private static boolean isDigit(char ch) {
        return ch >= '0' && ch <= '9';
    }

    /** The first broken rule's message, or null when the username is fine. */
    private static String checkUsername(String raw) {
        String username = raw.trim();
        if (username.isEmpty()) return "Username is required";
        if (username.length() < 3 || username.length() > 20) return "Username must be 3 to 20 characters";
        for (char ch : username.toCharArray()) {
            if (!isLetter(ch) && !isDigit(ch) && ch != '_') return "Username may only contain letters, digits and underscores";
        }
        return null;
    }

    private static String checkEmail(String raw) {
        String email = raw.trim();
        if (email.isEmpty()) return "Email is required";
        int at = email.indexOf('@');
        if (email.contains(" ") || at < 1 || email.indexOf('@', at + 1) != -1) return "Email is not valid";
        String domain = email.substring(at + 1);
        int dot = domain.indexOf('.', 1);
        if (dot < 1 || dot == domain.length() - 1) return "Email is not valid";
        return null;
    }

    private static String checkPassword(String password) {
        if (password.length() < 8) return "Password must be at least 8 characters";
        boolean hasDigit = false, hasLetter = false;
        for (char ch : password.toCharArray()) {
            if (isDigit(ch)) hasDigit = true;
            if (isLetter(ch)) hasLetter = true;
        }
        if (!hasDigit) return "Password must contain a digit";
        if (!hasLetter) return "Password must contain a letter";
        return null;
    }

    private static void add(List<FieldError> errors, Field field, String message) {
        if (message != null) errors.add(new FieldError(field, message));
    }

    public static ValidationResult validateSignup(SignupForm form) {
        List<FieldError> errors = new ArrayList<>();
        add(errors, Field.USERNAME, checkUsername(form.username()));
        add(errors, Field.EMAIL, checkEmail(form.email()));
        add(errors, Field.PASSWORD, checkPassword(form.password()));
        add(errors, Field.CONFIRM_PASSWORD, form.confirmPassword().equals(form.password()) ? null : "Passwords do not match");
        return errors.isEmpty() ? new Valid() : new Invalid(errors);
    }
}
