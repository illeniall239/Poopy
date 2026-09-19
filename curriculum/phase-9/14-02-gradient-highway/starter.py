def chain_grad(derivs: list[float], residual: bool) -> float:
    """Return prod(d) for a plain chain, or prod(1 + d) for a residual chain."""
    raise NotImplementedError


def input_grad_norm(depth: int, width: int, residual: bool, seed: int) -> float:
    """Build the seeded tanh stack from the Problem and return the L2 norm of d(h.sum())/dx."""
    raise NotImplementedError
