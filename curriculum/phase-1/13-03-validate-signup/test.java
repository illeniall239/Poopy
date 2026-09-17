import java.util.ArrayList;
import java.util.Arrays;
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

    static final Solution.SignupForm good = new Solution.SignupForm("ada_99", "ada@example.com", "s3cretpass", "s3cretpass");

    static Solution.SignupForm form(String username, String email, String password, String confirmPassword) {
        return new Solution.SignupForm(username, email, password, confirmPassword);
    }

    static Solution.FieldError err(Solution.Field field, String message) {
        return new Solution.FieldError(field, message);
    }

    static Solution.Invalid invalid(Solution.FieldError... errors) {
        return new Solution.Invalid(List.of(errors));
    }

    /** The first error message of the form, or null when it is valid. */
    static String messageFor(Solution.SignupForm form) {
        Solution.ValidationResult result = Solution.validateSignup(form);
        return result instanceof Solution.Invalid invalid ? invalid.errors().get(0).message() : null;
    }

    /** All errors of the form, or an empty list when it is valid. */
    static List<Solution.FieldError> errorsFor(String password, String confirmPassword) {
        Solution.ValidationResult result = Solution.validateSignup(form(good.username(), good.email(), password, confirmPassword));
        return result instanceof Solution.Invalid invalid ? invalid.errors() : List.of();
    }

    public static void main(String[] args) {
        check("a correct form is valid", () -> Solution.validateSignup(good), new Solution.Valid());
        check("surrounding spaces in username and email are ignored",
            () -> Solution.validateSignup(form("  ada ", " ada@example.com  ", good.password(), good.confirmPassword())),
            new Solution.Valid());
        check("reports every broken field at once, in field order",
            () -> Solution.validateSignup(form("  ", "ada@example", "short1", "short2")),
            invalid(
                err(Solution.Field.USERNAME, "Username is required"),
                err(Solution.Field.EMAIL, "Email is not valid"),
                err(Solution.Field.PASSWORD, "Password must be at least 8 characters"),
                err(Solution.Field.CONFIRM_PASSWORD, "Passwords do not match")));
        check("only the first broken rule per field is reported",
            () -> Solution.validateSignup(form("a!", good.email(), "abc", "abc")),
            invalid(
                err(Solution.Field.USERNAME, "Username must be 3 to 20 characters"),
                err(Solution.Field.PASSWORD, "Password must be at least 8 characters")));
        check("username rules", () -> {
            List<String> got = new ArrayList<>();
            for (String username : List.of("ab", "a".repeat(21), "a".repeat(20), "ada lovelace", "adé")) {
                got.add(messageFor(form(username, good.email(), good.password(), good.confirmPassword())));
            }
            return got;
        }, Arrays.asList(
            "Username must be 3 to 20 characters",
            "Username must be 3 to 20 characters",
            null,
            "Username may only contain letters, digits and underscores",
            "Username may only contain letters, digits and underscores"));
        check("email rules", () -> {
            List<String> got = new ArrayList<>();
            for (String email : List.of("", "a@b.co", "@a.com", "a@b.", "a@.com", "a@@b.com", "a@b@c.com", "a b@c.com", "abc.com", "a@bcom")) {
                got.add(messageFor(form(good.username(), email, good.password(), good.confirmPassword())));
            }
            return got;
        }, Arrays.asList(
            "Email is required",
            null,
            "Email is not valid",
            "Email is not valid",
            "Email is not valid",
            "Email is not valid",
            "Email is not valid",
            "Email is not valid",
            "Email is not valid",
            "Email is not valid"));
        check("password rules, and confirm is checked against the password as typed",
            () -> List.of(
                errorsFor("abcdefgh", "abcdefgh"),
                errorsFor("12345678", "12345678"),
                errorsFor("pass word1", "pass word1"),
                errorsFor("s3cretpass", "s3cretpass ")),
            List.of(
                List.of(err(Solution.Field.PASSWORD, "Password must contain a digit")),
                List.of(err(Solution.Field.PASSWORD, "Password must contain a letter")),
                List.of(),
                List.of(err(Solution.Field.CONFIRM_PASSWORD, "Passwords do not match"))));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
