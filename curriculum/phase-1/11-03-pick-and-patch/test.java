import java.util.Collections;
import java.util.List;
import java.util.Map;
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

    static Map<String, Object> makeProfile() {
        return Map.of("id", 7, "name", "Ana", "email", "ana@example.com", "theme", "dark");
    }

    public static void main(String[] args) {
        check("pick keeps only the listed keys", () -> Solution.pick(makeProfile(), List.of("name", "theme")), Map.of("name", "Ana", "theme", "dark"));
        check("pick with no keys gives an empty map", () -> Solution.pick(makeProfile(), List.of()), Map.of());
        check("pick with a repeated key includes it once", () -> Solution.pick(makeProfile(), List.of("id", "id")), Map.of("id", 7));
        check("pick keeps falsy values", () -> {
            Map<String, Object> obj = Map.of("count", 0, "on", false, "label", "");
            return Solution.pick(obj, List.of("count", "on", "label"));
        }, Map.of("count", 0, "on", false, "label", ""));
        check("pick does not change the map", () -> {
            Map<String, Object> profile = makeProfile();
            Solution.pick(profile, List.of("name"));
            return profile;
        }, makeProfile());
        check("applyPatch replaces patched keys", () -> {
            Map<String, Object> patch = Map.of("theme", "light", "name", "Ana B");
            return Solution.applyPatch(makeProfile(), patch);
        }, Map.of("id", 7, "name", "Ana B", "email", "ana@example.com", "theme", "light"));
        check("applyPatch ignores null values", () -> {
            Map<String, Object> patch = Collections.singletonMap("name", null);
            return Solution.applyPatch(makeProfile(), patch);
        }, makeProfile());
        check("applyPatch keeps falsy patch values that are not null", () -> {
            Map<String, Object> original = Map.of("count", 5, "on", true);
            Map<String, Object> patch = Map.of("count", 0, "on", false);
            return Solution.applyPatch(original, patch);
        }, Map.of("count", 0, "on", false));
        check("applyPatch returns a new map and changes neither input", () -> {
            Map<String, Object> profile = makeProfile();
            Map<String, Object> patch = Map.of("theme", "light");
            Map<String, Object> result = Solution.applyPatch(profile, patch);
            return List.of(result != profile, profile.equals(makeProfile()), patch.equals(Map.of("theme", "light")));
        }, List.of(true, true, true));
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
