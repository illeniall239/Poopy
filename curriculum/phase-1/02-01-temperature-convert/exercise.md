# Temperature convert

Topic: 2. Values, types, variables and expressions
Difficulty: 1 of 3

## Problem

Write two functions:

- `celsiusToFahrenheit(celsius)` returns the temperature in Fahrenheit.
- `fahrenheitToCelsius(fahrenheit)` returns the temperature in Celsius.

The formulas are: Fahrenheit = Celsius × 9 / 5 + 32, and Celsius = (Fahrenheit − 32) × 5 / 9.

Both functions return a `number` rounded to one decimal place (the nearest tenth). A result that is exactly halfway between two tenths rounds up, the way `Math.round` does.

## Examples

```
celsiusToFahrenheit(100)   → 212
celsiusToFahrenheit(37)    → 98.6
celsiusToFahrenheit(36.6)  → 97.9
fahrenheitToCelsius(0)     → -17.8
fahrenheitToCelsius(98.6)  → 37
```

## Constraints

- Inputs are numbers from -1000 to 1000 and may have decimals.
- Return a `number`, not a string.

## Hints

1. Work out `fahrenheitToCelsius(212)` on paper, following the formula exactly. Now type the formula into your code without any brackets. Do you get the same answer? Why or why not?
2. Which operators does TypeScript apply first: `-` or `*`? How do you force a different order?
3. `Math.round` rounds to a whole number. How could you use it to round to tenths instead? What would you have to do to the number before rounding, and after?
4. Try `celsiusToFahrenheit(36.6)` without any rounding. What do you see, and why isn't it exactly `97.88`?

## Explain-back

- What does `98.6 - 32 * 5 / 9` evaluate to, and why is that different from what the formula means?
- Why doesn't `36.6 * 9 / 5 + 32` give exactly `97.88` in TypeScript, and how does your rounding deal with that?
- If you store a result in a `const`, can you give that name a new value later? What exactly does `const` stop you doing?
