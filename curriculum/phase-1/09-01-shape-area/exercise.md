# Shape area

Topic: 9. TypeScript types: unions, narrowing, null safety
Difficulty: 1 of 3

## Problem

A drawing app stores shapes as objects. Every shape has a `kind` field that says which shape it is, and only the fields that make sense for that kind:

```ts
export type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number }
  | { kind: "triangle"; base: number; height: number };
```

Write `area(shape)` that returns the area of the shape:

- circle: `Math.PI` × radius × radius
- rectangle: width × height
- triangle: base × height ÷ 2

Do not round the result. Do not use `as` or `any`.

## Examples

```
area({ kind: "circle", radius: 1 })                    → 3.141592653589793
area({ kind: "rectangle", width: 3, height: 4 })       → 12
area({ kind: "triangle", base: 5, height: 3 })         → 7.5
```

## Constraints

- All measurements are finite numbers from 0 to 10000.
- `shape` is always one of the three kinds above.

## Hints

1. Inside `area`, before you check anything, which fields can TypeScript promise exist on `shape`? Try typing `shape.radius` and read the error.
2. Which single field do all three shapes share, and what are its possible values?
3. After you check that field against one of its values, hover over `shape` inside that branch. What type does TypeScript say it has now?
4. If someone later adds a fourth kind of shape, how could you make TypeScript point at `area` as a place that needs updating?

## Explain-back

- Why is `shape.radius` an error at the top of the function but fine inside your circle branch?
- A rectangle and a triangle both have `height`. Why doesn't that make `{ kind: "circle", radius: 1, height: 2 }` a valid `Shape`?
- What could go wrong if you wrote `(shape as any).radius` to silence the error instead?
