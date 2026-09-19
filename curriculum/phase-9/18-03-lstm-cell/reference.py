# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import torch


def lstm_cell(
    x: torch.Tensor, h: torch.Tensor, c: torch.Tensor, params: dict[str, torch.Tensor]
) -> tuple[torch.Tensor, torch.Tensor]:
    z = x @ params["W_ih"].T + params["b_ih"] + h @ params["W_hh"].T + params["b_hh"]
    zi, zf, zg, zo = z.chunk(4, dim=-1)
    i, f, g, o = torch.sigmoid(zi), torch.sigmoid(zf), torch.tanh(zg), torch.sigmoid(zo)
    c_new = f * c + i * g
    h_new = o * torch.tanh(c_new)
    return h_new, c_new
