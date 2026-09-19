# Conv shapes and parameters

Topic: 13. Convolutional networks
Difficulty: 1 of 3

## Problem

Write two functions in plain Python (no torch).

- `conv_output_size(n, k, p, s)` returns the output width of a convolution (or pooling) along one dimension: input size `n`, kernel size `k`, zero padding `p` on **each** side, stride `s`. The window slides in steps of `s` and must fit entirely inside the padded input, so the answer is `floor((n + 2p − k) / s) + 1`. Raise `ValueError` if `n < 1`, `k < 1`, `p < 0`, `s < 1`, or the kernel is larger than the padded input (`k > n + 2p`).
- `conv_params(in_c, out_c, k, bias=True)` returns the number of learnable parameters of a 2-D convolution layer with square `k × k` kernels that maps `in_c` input channels to `out_c` output channels. Each output channel has one `k × k` kernel **per input channel**, plus one bias if `bias` is `True`. Raise `ValueError` if any of `in_c`, `out_c`, `k` is less than `1`.

All arguments are ints; both functions return ints.

## Examples

```
conv_output_size(32, 3, 1, 1)   → 32     "same" padding
conv_output_size(32, 5, 0, 1)   → 28
conv_output_size(7, 3, 0, 2)    → 3
conv_output_size(8, 3, 1, 2)    → 4      (8 + 2 − 3) / 2 = 3.5, floor 3, + 1
conv_output_size(2, 5, 0, 1)    → ValueError
conv_params(3, 16, 3)           → 448    16·3·3·3 + 16
conv_params(3, 16, 3, bias=False) → 432
conv_params(64, 128, 1)         → 8320   a 1×1 conv still mixes all 64 channels
```

## Constraints

- All sizes are at most 10 000.
- Plain Python only; tests cross-check a few answers against `torch.nn.Conv2d`.

## Hints

1. Pad the input first: how wide is it now? How many positions can a width-`k` window start at with stride 1?
2. With stride `s`, only every `s`-th of those starting positions is used. Which operator turns that count into an integer the right way?
3. Picture one output channel. How many numbers does its kernel hold when the input has `in_c` channels?
4. How many biases does a conv layer have: one per layer, per input channel, per output channel, or per output pixel?

## Explain-back

- Why does a conv layer with 3 input channels and 16 output channels have 48 two-dimensional kernels, not 16?
- How many parameters does a 2×2 max-pooling layer have, and why?
- Why does a conv layer on a 224×224 image have far fewer parameters than a dense layer on the same image? What is "parameter sharing"?
- What happens to your shape formula if you forget the padding, and how would that show up when you build a network?
