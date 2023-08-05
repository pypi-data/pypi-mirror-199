import numpy as np
import pytest


@pytest.fixture
def small_network():
    # Network structure:
    # => A, A <=> B, B <=> C, A => C, C <=>

    S = np.array(
        [
            [1, -1, 0, -1, 0],
            [0, 1, -1, 0, 0],
            [0, 0, 1, 1, -1],
        ]
    )
    rev = [0, 1, 1, 0, 1]
    reactions = ["r1", "r2", "r3", "r4", "r5"]
    metabolites = ["A", "B", "C"]

    return (S, rev, reactions, metabolites)


@pytest.fixture
def blocked_network():
    # Network structure:
    # => A, => A

    S = np.array([[1, 1]])
    rev = [0, 0]
    reactions = ["r1", "r2"]
    metabolites = ["A"]

    return (S, rev, reactions, metabolites)
