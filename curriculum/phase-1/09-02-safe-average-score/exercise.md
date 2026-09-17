# Safe average score

Topic: 9. TypeScript types: unions, narrowing, null safety
Difficulty: 2 of 3

## Problem

A teacher's gradebook lists students. Some students haven't taken the test yet, so their score is missing:

```ts
export type Student = { name: string; score?: number | null };
```

A score is missing when the `score` property is absent, `undefined`, or `null`. A score of `0` is a real score and counts.

Write `averageScore(students)` that returns the average of all present scores, not rounded. If there are no present scores (including an empty array), return `null`.

Do not use `as`, `any`, or the non-null assertion `!`. Do not change the input.

## Examples

```
averageScore([{ name: "Ana", score: 80 }, { name: "Ben", score: 90 }])   → 85
averageScore([{ name: "Ana", score: 80 }, { name: "Ben" }])              → 80
averageScore([{ name: "Ana", score: 0 }, { name: "Ben", score: 10 }])    → 5
averageScore([{ name: "Ana", score: null }])                            → null
averageScore([])                                                         → null
```

## Constraints

- `students` has 0 to 100000 elements.
- Present scores are finite numbers from 0 to 100.

## Hints

1. By hand, for the second example, what did you divide by: the number of students, or something else?
2. What are all the possible types of `student.score`? Hover over it in your editor to check.
3. Which check tells apart "there is a number here" from "missing", without also throwing away a score of `0`?
4. After the loop, what do your accumulators look like if no scores were present, and what should you return in that case instead of dividing?

## Explain-back

- Why would `if (student.score)` give the wrong answer for the third example?
- What is the difference between a `score` property that is absent, one that is `undefined`, and one that is `null`? Does your code need to care?
- Why does the return type say `number | null`, and what must a caller do before using the result in arithmetic?
