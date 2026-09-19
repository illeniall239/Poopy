# A tiny CNN in PyTorch

Topic: 13. Convolutional networks
Difficulty: 2 of 3

## Problem

Build a LeNet-style stack (conv → activation → pool, twice, then a linear classifier) and train it on a synthetic task: 8×8 grayscale images that contain either **vertical bars** (label `0`) or **horizontal stripes** (label `1`), with noise. You may use anything in `torch` and `torch.nn` here.

Write a class `TinyCNN(nn.Module)` with exactly these submodules as attributes, in this order:

| attribute | layer | output shape for a `(B, 1, 8, 8)` input |
|---|---|---|
| `conv1` | `nn.Conv2d(1, 4, kernel_size=3, padding=1)` | `(B, 4, 8, 8)` |
| `pool1` | `nn.MaxPool2d(2)` | `(B, 4, 4, 4)` |
| `conv2` | `nn.Conv2d(4, 8, kernel_size=3, padding=1)` | `(B, 8, 4, 4)` |
| `pool2` | `nn.MaxPool2d(2)` | `(B, 8, 2, 2)` |
| `fc` | `nn.Linear(32, 2)` | `(B, 2)` |

`forward(x)` applies `conv1`, ReLU, `pool1`, `conv2`, ReLU, `pool2`, flattens each example to 32 numbers, then `fc`. It returns raw logits of shape `(B, 2)` (no softmax). The model has exactly 402 parameters.

Also write `train_tiny_cnn(model, X, y, steps, lr)`: full-batch training with `torch.optim.Adam(model.parameters(), lr=lr)` and `nn.CrossEntropyLoss()` for `steps` steps. `X` is a float tensor `(N, 1, 8, 8)` and `y` a long tensor `(N,)`. Each step: zero the gradients, compute the loss on all of `X`, backpropagate, step. Put the model in training mode first. Return the list of the `steps` loss values (Python floats, the loss computed at each step before its update).

The tests train on 64 seeded examples for 150 steps with `lr=0.01` and require at least 95 % accuracy on the training set and on 64 fresh examples.

## Examples

```
model = TinyCNN()
model(torch.zeros(5, 1, 8, 8)).shape                   → torch.Size([5, 2])
model.pool1(torch.relu(model.conv1(x))).shape          → torch.Size([B, 4, 4, 4])
sum(p.numel() for p in model.parameters())             → 402
losses = train_tiny_cnn(model, X, y, steps=150, lr=0.01)
len(losses)                                            → 150
losses[-1] < losses[0]                                 → True
```

## Constraints

- CPU only; the whole test file runs in a few seconds.
- Use the layer sizes above exactly: the tests inspect them.

## Hints

1. With `kernel_size=3` and `padding=1`, what does the shape formula `(n + 2p − k) / s + 1` give for `n = 8`? What does a 2×2 pool with stride 2 do to it?
2. After `pool2`, how many numbers does each example hold, and which call flattens all dimensions except the batch?
3. Which of the five layers own parameters? Count them and check you get 402.
4. In the training loop, what goes wrong if you forget to zero the gradients, and in which order must `backward` and `step` run?

## Explain-back

- Why does `conv2` have 4 × 8 = 32 kernels of size 3×3, and how many biases does it have?
- A vertical bar anywhere in the image should give label 0. Which property of convolution plus pooling lets one small kernel detect it at every position?
- What is the receptive field of one unit after `pool2`, measured in input pixels?
- Why does `forward` return logits instead of probabilities when you train with `nn.CrossEntropyLoss`?
