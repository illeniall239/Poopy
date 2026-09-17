# Deepest call stack

Topic: 1. How computers run code
Difficulty: 2 of 3

## Problem

Every function call pushes a frame onto the call stack, and the frame is popped when the function returns. A program that nests calls too deeply overflows the stack.

You are given a tiny program as a map from each function name to the list of functions it calls, in order: `calls: Record<string, string[]>`. When a function runs, it calls each function in its list one after another, and each call returns before the next one starts. A function that is not a key in `calls` calls nothing. The functions have no conditions, so a function that is called while it is already on the stack will recurse forever.

Write `maxCallDepth(calls, entry)`. The program starts by calling `entry`, which is one frame. Return the largest number of frames that are ever on the stack at the same time. If running from `entry` ever calls a function that is already on the stack, return `-1` (the program recurses forever), even if that happens away from the deepest path. Functions that `entry` never reaches don't matter.

## Examples

```
maxCallDepth({ main: ["parse"], parse: ["readFile"] }, "main")   → 3
maxCallDepth({ main: ["log", "log", "save"] }, "main")           → 2
maxCallDepth({ main: ["a", "b"], a: ["util"], b: ["util"] }, "main") → 3
maxCallDepth({ main: ["isEven"], isEven: ["isOdd"], isOdd: ["isEven"] }, "main") → -1
```

## Constraints

- Up to 1000 functions and 2000 listed calls in total.
- Names are non-empty strings of letters and digits.
- Time: O(functions + calls). Programs can share helpers so heavily that simulating every call one by one would take longer than the age of the universe.

## Hints

1. Draw the stack for the second example as it runs. When `log` returns and the next `log` starts, how many frames are there?
2. The depth reached below a function doesn't depend on who called it. How could you avoid working it out more than once?
3. When you meet a function name again, how do you tell "this is already on the stack right now" apart from "I finished this one earlier"? Do you need one set or two?
4. Once you know the deepest stack below each function a function calls, how do you get the deepest stack starting at that function itself?

## Explain-back

- Why don't calls made one after another add up, while nested calls do?
- In the third example `util` is reached twice. Why is that not infinite recursion, and what would a single "visited" set wrongly report?
- What is the time and space complexity of your solution, including the space used by your own recursion stack?
- A real recursive function with a base case can still crash with a stack overflow. Is that because the computer ran out of memory in general? What exactly runs out?
