# Simulate fp16 and loss scaling

Topic: 16. GPUs, performance and debugging training
Difficulty: 2 of 3

## Problem

float16 keeps only 5 exponent bits: its largest finite value is 65504 and its smallest positive (subnormal) value is about 6e-8. Tiny gradients silently become 0 and big ones blow up to infinity. Mixed-precision training multiplies the loss by a *scale* so the gradients land in the representable range. Simulate that in plain Python with the standard `struct` module (no numpy, no torch).

- `to_fp16(x)` rounds the Python float `x` to the nearest float16 and returns a tuple `(value, status)`, where `value` is a Python `float` and `status` is one of:
  - `"overflow"` — `x` is finite but too large in magnitude for float16; `value` is `math.inf` with the sign of `x`.
  - `"underflow"` — `x` is nonzero but rounds to zero in float16; `value` is `0.0` (a signed zero is fine).
  - `"ok"` — everything else, including `x = 0.0`, infinities and NaN passed in, and subnormal results. `value` is the rounded float16 number.

  Do the rounding with `struct.pack("<e", x)` and `struct.unpack("<e", ...)`. On values too large for float16, `struct.pack` raises (an `OverflowError` or a `struct.error`, depending on the value); catch that rather than comparing against 65504 yourself, because values slightly above 65504 still round down to it.
- `loss_scale_ok(grads, scale)` returns `True` when every gradient in the list `grads`, multiplied by `scale`, converts to float16 with status `"ok"` (no overflow and no nonzero gradient underflowing to zero), else `False`. An empty list is `True`. Raise `ValueError` if `scale <= 0`.

## Examples

```
to_fp16(1.0)       → (1.0, "ok")
to_fp16(0.1)       → (0.0999755859375, "ok")      only about 3 decimal digits survive
to_fp16(65519.0)   → (65504.0, "ok")              rounds down to the max
to_fp16(70000.0)   → (inf, "overflow")
to_fp16(-1e6)      → (-inf, "overflow")
to_fp16(1e-8)      → (0.0, "underflow")
to_fp16(0.0)       → (0.0, "ok")

loss_scale_ok([1e-8, 1e-3], 1.0)     → False     1e-8 vanishes
loss_scale_ok([1e-8, 1e-3], 1024.0)  → True
loss_scale_ok([1e-8, 1e-3], 1e8)     → False     1e-3 * 1e8 = 1e5 overflows
```

## Constraints

- Plain Python with `struct` and `math`.
- Lists have at most 10 000 gradients.

## Hints

1. What does `struct.pack("<e", x)` produce, and how do you get a Python float back from those 2 bytes?
2. Try `struct.pack("<e", 1e6)` in a REPL. What happens, and how do you turn that into the `"overflow"` case with the right sign?
3. How can you tell "the input was already 0" apart from "a nonzero input rounded to 0"?
4. `loss_scale_ok` should not duplicate your fp16 logic. Which function already answers "is this one number fine"?

## Explain-back

- Why does training in pure float16 without loss scaling often *look* fine (no error, no NaN) while the model stops learning?
- Loss scaling multiplies the loss, not the gradients. Why is that enough, and what must happen to the gradients before `optimizer.step()`?
- Dynamic loss scaling lowers the scale when it sees inf and raises it after a streak of clean steps. Which of your two failure cases does each move fix?
- bfloat16 has the same exponent range as float32. Why does it usually not need loss scaling, and what does it lose instead?
