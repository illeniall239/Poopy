# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def conv2d(image: list[list[float]], kernel: list[list[float]], stride: int = 1, padding: int = 0) -> list[list[float]]:
    if stride < 1 or padding < 0:
        raise ValueError("need stride >= 1 and padding >= 0")
    h, w = len(image), len(image[0])
    kh, kw = len(kernel), len(kernel[0])
    ph, pw = h + 2 * padding, w + 2 * padding
    if kh > ph or kw > pw:
        raise ValueError("kernel is larger than the padded image")
    padded = [[0.0] * pw for _ in range(padding)]
    padded += [[0.0] * padding + [float(v) for v in row] + [0.0] * padding for row in image]
    padded += [[0.0] * pw for _ in range(padding)]
    out_h, out_w = (ph - kh) // stride + 1, (pw - kw) // stride + 1
    return [
        [
            float(sum(kernel[a][b] * padded[i * stride + a][j * stride + b] for a in range(kh) for b in range(kw)))
            for j in range(out_w)
        ]
        for i in range(out_h)
    ]


def maxpool2d(image: list[list[float]], size: int, stride: int | None = None) -> list[list[float]]:
    stride = size if stride is None else stride
    h, w = len(image), len(image[0])
    if size < 1 or size > h or size > w or stride < 1:
        raise ValueError("bad pooling size or stride")
    out_h, out_w = (h - size) // stride + 1, (w - size) // stride + 1
    return [
        [
            float(max(image[i * stride + a][j * stride + b] for a in range(size) for b in range(size)))
            for j in range(out_w)
        ]
        for i in range(out_h)
    ]
