# LSTM cell

Topic: 18. Sequence modeling: n-gram LM → MLP LM → RNN, LSTM, GRU
Difficulty: 3 of 3

## Problem

An LSTM carries **two** states: the cell state `c`, changed only by gated addition, and the hidden state `h`, a gated read-out of `c`. Write one LSTM step in PyTorch, in the same parameter layout as `torch.nn.LSTMCell`.

`lstm_cell(x, h, c, params)` takes a batch of inputs `x` of shape `(B, D)`, the previous hidden and cell states `h` and `c`, each `(B, H)`, and a dict `params` with

- `"W_ih"`: `(4H, D)`, `"W_hh"`: `(4H, H)`, `"b_ih"`: `(4H,)`, `"b_hh"`: `(4H,)`.

The `4H` rows are four blocks of `H` rows, **in the order input gate `i`, forget gate `f`, candidate `g`, output gate `o`**. With `z = x @ W_ih.T + b_ih + h @ W_hh.T + b_hh` split into those four blocks along the last dimension:

```
i = sigmoid(z_i)    f = sigmoid(z_f)    g = tanh(z_g)    o = sigmoid(z_o)
c_new = f * c + i * g
h_new = o * tanh(c_new)
```

Return the tuple `(h_new, c_new)`, both `(B, H)`. The result must be differentiable with respect to every parameter.

Do not use `torch.nn.LSTM`, `torch.nn.LSTMCell`, `torch.lstm_cell` or any other built-in recurrent layer: the test uses `nn.LSTMCell` with the same weights to check you. `torch.sigmoid`, `torch.tanh`, matmul and `chunk`/`split` are fine.

## Examples

```
D = 1, H = 1, all weights 0, all biases 0:
  z = 0 → i = f = o = 0.5, g = 0
  lstm_cell(x=[[3.0]], h=[[0.0]], c=[[2.0]], params) → (h=[[0.5 · tanh(1.0)]], c=[[1.0]])
                                                         = ([[0.3808]], [[1.0]])

Forget gate forced open (b_ih for f = +100), input gate shut (b_ih for i = −100):
  c_new == c        the memory passes through untouched
```

## Constraints

- `B`, `D`, `H` at most 32. float32 tensors.
- PyTorch on CPU.

## Hints

1. How many pre-activation numbers does one step need per example, and why is it `4H`?
2. Once you have `z` of shape `(B, 4H)`, which tensor method cuts it into four `(B, H)` pieces, and in which order must you name them?
3. Which of the four pieces gets `tanh` and which get `sigmoid`, and why does the candidate need a range of −1 to 1 while the gates need 0 to 1?
4. Which state is updated by addition, and which one is read out from it? Which of the two do you pass to the next time step?

## Explain-back

- The LSTM returns both `h` and `c`. Are they the same thing? Which one is the long-term memory, and which one does the next layer see?
- Why does the additive update `c_new = f * c + i * g` let gradients flow over many steps better than the RNN's `tanh(Whh · h)`?
- What does the forget gate do when it is near 0, and why do many implementations initialize its bias to 1?
- A GRU merges the gates into two (update and reset) and has no separate cell state. What does it give up, and what does it save?
