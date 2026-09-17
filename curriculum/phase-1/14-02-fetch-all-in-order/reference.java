// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.function.Function;

public class Solution {
    public static CompletableFuture<List<String>> fetchAll(List<String> urls, Function<String, CompletableFuture<String>> fetchPage) {
        List<CompletableFuture<String>> downloads = urls.stream().map(fetchPage).toList();
        return CompletableFuture.allOf(downloads.toArray(new CompletableFuture<?>[0]))
            .thenApply(done -> downloads.stream().map(CompletableFuture::join).toList());
    }

    public static CompletableFuture<List<String>> fetchOneByOne(List<String> urls, Function<String, CompletableFuture<String>> fetchPage) {
        CompletableFuture<List<String>> pages = CompletableFuture.completedFuture(new ArrayList<>());
        for (String url : urls) {
            pages = pages.thenCompose(soFar -> fetchPage.apply(url).thenApply(page -> {
                soFar.add(page);
                return soFar;
            }));
        }
        return pages;
    }
}
