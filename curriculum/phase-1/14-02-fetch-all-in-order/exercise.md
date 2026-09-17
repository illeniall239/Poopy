# Fetch all in order

Topic: 14. Promises, async/await and the event loop
Difficulty: 2 of 3

## Problem

You need to download several pages. Downloading is done by a function you're given, `fetchPage(url)`, which returns a `Promise<string>` with the page's text. (In the tests it's a fake that waits a few milliseconds; no real network is used.)

Write two functions that take a list of `urls` and `fetchPage`, and resolve with the page texts **in the same order as `urls`**, no matter which download finishes first:

- `fetchAll(urls, fetchPage)` downloads in parallel: it starts every download straight away, before any of them has finished. If any download rejects, `fetchAll` rejects with the error of the first download to reject. That failure does not cancel the other downloads; they keep running to completion in the background.
- `fetchOneByOne(urls, fetchPage)` downloads sequentially: it starts each download only after the previous one has resolved. If a download rejects, `fetchOneByOne` rejects with that error and doesn't start any of the remaining downloads.

Both resolve with `[]` for an empty list, without calling `fetchPage`.

## Examples

```
// fakeFetch("a") takes 30ms, fakeFetch("b") 10ms, fakeFetch("c") 20ms, each resolving "page a" etc.

await fetchAll(["a", "b", "c"], fakeFetch)
  → ["page a", "page b", "page c"]     (takes about 30ms; "b" finished first)

await fetchOneByOne(["a", "b", "c"], fakeFetch)
  → ["page a", "page b", "page c"]     (takes about 60ms)

Order of events:
  fetchAll:      start a, start b, start c, end b, end c, end a
  fetchOneByOne: start a, end a, start b, end b, start c, end c
```

## Constraints

- `urls` has 0 to 100 items.
- `fetchAll` may use `Promise.all`. `fetchOneByOne` must not use `forEach`.

## Hints

1. When you call `fetchPage(url)`, does the download start at that moment or when you `await` the promise? What does that tell you about where the parallel version should call it?
2. For `fetchAll`, if you have an array of promises in `urls` order, which built-in turns it into one promise of an array, still in that order?
3. For `fetchOneByOne`, what does `await` inside a `for...of` loop do to the next iteration? What happens instead if you `await` inside a `forEach` callback?
4. When one download in `fetchOneByOne` rejects inside the loop, and you don't catch it, what happens to the rest of the loop and to the promise the function returns?

## Explain-back

- Predict the order of the "start" and "end" events for both functions with the example delays, and explain why each happens in that order.
- `fetchAll` rejected because one download failed. Are the other downloads still running? What does `Promise.all` actually stop?
- Why doesn't `urls.forEach(async (url) => results.push(await fetchPage(url)))` give sequential downloads or results in order?
