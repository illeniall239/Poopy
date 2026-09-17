# Parse a command

Topic: 9. TypeScript types: unions, narrowing, null safety
Difficulty: 3 of 3

## Problem

A text adventure game reads commands typed by the player. Turn the raw text into a typed value the game can trust:

```ts
export type Direction = "up" | "down" | "left" | "right";

export type Command =
  | { type: "move"; direction: Direction; steps: number }
  | { type: "say"; message: string }
  | { type: "quit" };

export type ParseError = { type: "error"; message: string };
```

Write `parseCommand(input)` that returns a `Command`, or a `ParseError` if the input is invalid.

Splitting into words:
- Leading and trailing spaces are ignored. Words are separated by one or more spaces.

Valid commands (the first word and the direction are case-insensitive):
- `move <direction> <steps>`: exactly three words. `<direction>` is `up`, `down`, `left` or `right` and is returned in lowercase. `<steps>` is made only of the digits `0`–`9` and its value is at least 1.
- `say <words...>`: `say` followed by at least one word. `message` is the words after `say`, joined with single spaces, with their case unchanged.
- `quit`: exactly one word.

Anything else (empty input, an unknown first word, the wrong number of words, a bad direction, or bad steps) returns `{ type: "error", message }` where `message` is a non-empty string describing the problem. The exact wording is up to you.

The returned objects must have exactly the fields shown in the types, nothing extra. Do not use `as` or `any`.

## Examples

```
parseCommand("move up 3")          → { type: "move", direction: "up", steps: 3 }
parseCommand("  MOVE   Left 10 ")  → { type: "move", direction: "left", steps: 10 }
parseCommand("say Hello   there")  → { type: "say", message: "Hello there" }
parseCommand("quit")               → { type: "quit" }
parseCommand("move north 2")       → { type: "error", message: "..." }
parseCommand("move up 0")          → { type: "error", message: "..." }
parseCommand("")                   → { type: "error", message: "..." }
```

## Constraints

- `input` has 0 to 1000 characters and contains no tabs or newlines.

## Hints

1. Before you parse anything, what list of words do you want to have for `"  MOVE   Left 10 "`? What gets in the way if you split on a single space?
2. Once you have the words, which one decides what kind of command you're parsing, and what should every branch check first?
3. `"left"` is a `string`, but `direction` needs the type `Direction`. What check lets TypeScript narrow a `string` down to one of four literal values without `as`?
4. Which inputs for steps should be rejected even though `Number(...)` turns them into a number? Try `""`, `"2.5"`, `"-1"` and `"0"` by hand against the rules.

## Explain-back

- How does code that receives the result of `parseCommand` find out whether it got a `move`, a `say`, or an error, and what can it access after that check?
- Why is returning a `ParseError` value safer than returning `undefined` for bad input?
- What would go wrong if you wrote `words[1] as Direction` instead of checking the value?
