# Forward and backward over a graph

Topic: 3. Computational graphs and backprop by hand
Difficulty: 3 of 3

## Problem

Write `graph_backward(nodes, leaves, output)` in plain Python (no numpy, no torch, no `graphlib`). It evaluates a computational graph and then backpropagates through it.

- `leaves` maps each input name to its float value, e.g. `{"x": 2.0, "w": -1.0}`.
- `nodes` maps each operation node's name to an `(op, inputs)` record, where `inputs` is a list of names (leaves or other nodes). The ops are:
  - `"add"`: exactly two inputs, value `in0 + in1`
  - `"mul"`: exactly two inputs, value `in0 * in1`
  - `"tanh"`: exactly one input, value `tanh(in0)`

  The same name may appear twice in one `inputs` list (`("mul", ["x", "x"])` is `x²`), and a name may feed several nodes. The dict is in **no particular order**: a node can be listed before the nodes it reads.
- `output` is the name (node or leaf) whose gradient you want.

Return a tuple `(values, grads)` of two dicts, each with one float entry for **every** leaf and node name:
- `values[name]`: the forward value.
- `grads[name]`: `∂output/∂name`. `grads[output]` is `1.0`; names that `output` does not depend on get `0.0`.

Do it as a real engine does: order the nodes topologically (write that inside this file; you may copy your `topo_sort` from the previous exercise), compute every value in that order, then visit the nodes in **reverse** order, adding `upstream × local derivative` into each input's gradient.

Raise `ValueError` if an op is unknown, a node has the wrong number of inputs, an input name is neither a leaf nor a node, a name is both a leaf and a node, `output` is unknown, or the nodes form a cycle.

## Examples

```
graph_backward({"sq": ("mul", ["x", "x"])}, {"x": 3.0}, "sq")
    → ({"x": 3.0, "sq": 9.0}, {"x": 6.0, "sq": 1.0})        both uses of x contribute 3.0

graph_backward(
    {"L": ("mul", ["d", "f"]), "d": ("add", ["e", "c"]), "e": ("mul", ["a", "b"])},
    {"a": 2.0, "b": -3.0, "c": 10.0, "f": -2.0},
    "L",
)
    → values {"a": 2.0, "b": -3.0, "c": 10.0, "f": -2.0, "e": -6.0, "d": 4.0, "L": -8.0}
      grads  {"a": 6.0, "b": -4.0, "c": -2.0, "f": 4.0, "e": -2.0, "d": -2.0, "L": 1.0}
```

## Constraints

- At most 300 nodes; all values stay finite.
- Leaf gradients are checked against central-difference numeric derivatives within `1e-6`.

## Hints

1. Which edges does this graph have, and in which direction do they point, if "a node must come after everything it reads"?
2. Once you have that order, what does the forward pass look like? What does the backward pass start from?
3. For each op, what is the local derivative with respect to each of its inputs? Which of them need the forward values you stored?
4. `("mul", ["x", "x"])` and a name that feeds two nodes both reach the same gradient slot more than once. Should the second contribution replace the first, or be added to it? When is a node's own gradient complete and safe to pass on?

## Explain-back

- Why must the backward pass run in reverse topological order? Give a tiny graph where any other order sends on an incomplete gradient.
- Why is the gradient summed where a node fans out? Tie it to the multivariable chain rule.
- One reverse pass gave you the derivative of `output` with respect to every leaf at once. How many passes would forward-mode differentiation need here, and why does this make reverse mode the right choice for a scalar loss?
- `grads` tells you how the output would change. What still has to happen for a network to learn?
