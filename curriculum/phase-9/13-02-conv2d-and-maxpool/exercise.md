# Conv2d and max pooling by hand

Topic: 13. Convolutional networks
Difficulty: 2 of 3

## Problem

Write two single-channel functions in plain Python on lists of lists (no numpy, no torch). An image is a list of `H` rows, each a list of `W` numbers.

- `conv2d(image, kernel, stride=1, padding=0)` computes what deep-learning libraries call convolution, which is really **cross-correlation**: the kernel is **not** flipped. First surround the image with `padding` rows/columns of zeros on every side. Then, for each output position `(i, j)`, place the kernel's top-left corner at padded position `(i·stride, j·stride)` and sum the elementwise products of the kernel and the patch under it. The kernel is `kh × kw` (it need not be square). The output is `out_h × out_w` with `out_h = floor((H + 2·padding − kh) / stride) + 1`, and likewise for the width. Raise `ValueError` if the kernel is larger than the padded image in either dimension, `stride < 1`, or `padding < 0`.
- `maxpool2d(image, size, stride=None)` slides a `size × size` window (no padding) with the given stride, which defaults to `size` when `None`, and takes the maximum of each window. Output size uses the same floor formula with padding 0. Raise `ValueError` if `size` is less than 1 or larger than the image, or `stride < 1`.

Both return new lists of lists of floats. Tests compare your results with `torch.nn.functional.conv2d` and `max_pool2d` on random inputs (tolerance `1e-9`); you may not use them.

## Examples

```
image = [[0, 0, 1, 1],        vertical edge between columns 1 and 2
         [0, 0, 1, 1],
         [0, 0, 1, 1],
         [0, 0, 1, 1]]
sobel_x = [[-1, 0, 1],
           [-2, 0, 2],
           [-1, 0, 1]]
conv2d(image, sobel_x)             → [[4.0, 4.0], [4.0, 4.0]]
conv2d(image, [[1, -1]])           → [[0.0, -1.0, 0.0]] × 4 rows    not flipped: left minus right
conv2d([[1, 2], [3, 4]], [[1]], padding=1) → [[0,0,0,0],[0,1,2,0],[0,3,4,0],[0,0,0,0]] (as floats)
conv2d(image, sobel_x, stride=2, padding=1) → [[0.0, 3.0], [0.0, 4.0]]

maxpool2d([[1, 2, 5, 0],
           [3, 4, 1, 1],
           [0, 0, 9, 8],
           [7, 0, 6, 2]], 2)       → [[4.0, 5.0], [7.0, 9.0]]
maxpool2d([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2, stride=1) → [[5.0, 6.0], [8.0, 9.0]]
```

## Constraints

- Images and kernels are at most 32 × 32.
- Plain Python only: no `torch.nn.functional`, no `scipy`, no numpy.

## Hints

1. Before touching the kernel: how do you build the zero-padded image, and how big is it?
2. How many output rows are there, and at which padded row does output row `i` start once stride is involved?
3. With the kernel `[[1, -1]]` and a step from 0 to 1 going left to right, what sign should a true convolution (flipped kernel) give, and what sign does cross-correlation give?
4. Max pooling is the same sliding loop as convolution. What replaces "multiply and sum", and what is missing compared with a conv layer?

## Explain-back

- Deep-learning "convolution" does not flip the kernel. Does it matter for a layer whose kernel is learned? Why or why not?
- Shift the edge in the input one column to the right. What happens to the output, and what is that property called?
- How many learnable parameters does max pooling have? What does it do to the receptive field of the next layer?
- A real conv layer takes `in_c` channels to `out_c` channels. How would your single-channel `conv2d` be used to build it, and where does the bias go?
