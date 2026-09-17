# Pick and patch

Topic: 11. Generics and utility types
Difficulty: 3 of 3

## Problem

A settings screen loads a user profile, shows only some fields, and saves partial edits. Write two generic helpers:

- `pick<T, K extends keyof T>(obj: T, keys: K[]): Pick<T, K>` returns a new object with only the listed keys and their values from `obj`. A key listed twice appears once. `obj` is not changed.
- `applyPatch<T>(original: T, patch: Partial<T>): T` returns a new object: a copy of `original` with every key present in `patch` replaced by the patch's value. Keys whose value in `patch` is `undefined` are ignored (the original value stays). `original` and `patch` are not changed.

Don't use `any`. You may use `as` exactly once, in `pick`, when creating the empty result object: TypeScript can't know the loop will fill in every key.

## Examples

```
const profile = { id: 7, name: "Ana", email: "ana@example.com", theme: "dark" };

pick(profile, ["name", "theme"])
  → { name: "Ana", theme: "dark" }

applyPatch(profile, { theme: "light" })
  → { id: 7, name: "Ana", email: "ana@example.com", theme: "light" }

applyPatch(profile, { name: undefined })
  → { id: 7, name: "Ana", email: "ana@example.com", theme: "dark" }

pick(profile, ["nmae"])   → type error in your editor: "nmae" is not a key of profile
```

## Constraints

- Objects are flat: values are strings, numbers or booleans.
- Only plain objects are passed in.

## Hints

1. What does `K extends keyof T` allow the caller to pass, and what does it forbid? Try `pick(profile, ["nmae"])` in your editor.
2. For `pick`, what do you need to loop over: the keys of `obj` or the `keys` argument? Which one does the result's shape come from?
3. For `applyPatch`, how can spread (Topic 8) give you a copy of `original`? What does spreading `patch` over it do with a key whose value is `undefined`?
4. The "ignore `undefined`" rule means a plain `{ ...original, ...patch }` isn't enough. How can you copy only the patch keys whose values are defined?

## Explain-back

- Why is `Partial<T>` the right type for `patch`? What would go wrong for callers if it were `T`?
- Your copy is shallow. For these flat objects that's fine; describe an object where it wouldn't be.
- Why does `pick` return `Pick<T, K>` instead of `Partial<T>`? What does the caller get from the more precise type?
- Your one `as` is a promise to the compiler. What promise is it, and what would break it?
