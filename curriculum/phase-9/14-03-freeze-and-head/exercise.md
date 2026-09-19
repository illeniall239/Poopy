# Freeze the backbone, replace the head

Topic: 14. Modern CNN ideas: residual connections and transfer learning
Difficulty: 2 of 3

## Problem

Fine-tuning a pretrained model on a small dataset usually starts like this: keep the pretrained **backbone** fixed, throw away the old classification **head**, and train a fresh head for the new classes. Write two PyTorch functions for a model that is an `nn.Sequential` whose **last** module is the `nn.Linear` head and everything before it is the backbone.

- `freeze_backbone(model)` sets `requires_grad = False` on every parameter of every module except the last one, and `requires_grad = True` on the head's parameters. It changes the model in place and returns the same model object.
- `replace_head(model, n_classes)` replaces the last module with a new `nn.Linear` that has the same `in_features` as the old head and `n_classes` outputs. The new head's parameters are trainable. It changes the model in place and returns the same model object; the backbone's modules and their `requires_grad` flags are untouched.

Both raise `ValueError` if `model` is not an `nn.Sequential` or its last module is not an `nn.Linear`; `replace_head` also raises `ValueError` if `n_classes < 1`.

After `replace_head(freeze_backbone(model), k)`, the only trainable parameters are the new head's weight and bias. Training with an optimizer built over **all** of `model.parameters()` must leave every backbone weight exactly unchanged. The tests pretrain a tiny MLP on one synthetic task, then fine-tune only a new 3-class head on 48 examples of a related task and require at least 80 % accuracy on fresh examples.

## Examples

```
model = nn.Sequential(nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 16), nn.ReLU(), nn.Linear(16, 2))
freeze_backbone(model) is model                                → True
[n for n, p in model.named_parameters() if p.requires_grad]    → ["4.weight", "4.bias"]
replace_head(model, 3)[-1]                                     → Linear(in_features=16, out_features=3, bias=True)
replace_head(nn.Sequential(nn.Linear(4, 2), nn.ReLU()), 3)     → ValueError   last module is not a Linear
```

## Constraints

- CPU only, tiny models; the test file runs in a few seconds.
- Use `torch.nn` only; nothing is downloaded. "Pretrained" means trained inside the test.

## Hints

1. Which attribute of a parameter decides whether autograd computes a gradient for it, and what does an optimizer do with a parameter whose `.grad` stays `None`?
2. How do you index the last module of an `nn.Sequential`, and all modules except the last?
3. How do you read the old head's input width so the new head plugs into the backbone's output?
4. Is `requires_grad` on a freshly constructed `nn.Linear` `True` or `False`, and does that matter if you replace the head after freezing?

## Explain-back

- Why freeze the backbone and not the head? What would training do if you froze the new, randomly initialized head instead?
- Why is fine-tuning a pretrained model usually a better default than training from scratch on a small dataset?
- What are discriminative learning rates, and why would you give the backbone a smaller learning rate than the head once you unfreeze it?
- Your new task has 3 classes and the old head had 2. Why can't you keep the old head's weights?
