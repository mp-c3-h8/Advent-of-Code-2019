import os.path
import os
from timeit import default_timer as timer
import numpy as np
from scipy.ndimage import convolve
from itertools import product


def conway(bugs: np.ndarray) -> int:
    biodiversities: set[int] = set()
    power_two = np.array([2**i for i in range(25)], dtype=int).reshape((5, 5))
    kernel = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=int)

    for k in range(1, 10**6):
        bio = (power_two * bugs).sum()
        if bio in biodiversities:
            return bio
        biodiversities.add(bio)
        neighbors = convolve(bugs, kernel, mode="constant")
        new_bugs = bugs.copy()
        new_bugs[(bugs == 1) & (neighbors != 1)] = 0
        new_bugs[(bugs == 0) & ((neighbors == 1) | (neighbors == 2))] = 1
        bugs = new_bugs

    else:
        raise ValueError("Max iterations reached.")


def recursive_conway(bugs: np.ndarray) -> int:
    A = bugs.reshape((1, 5, 5))
    A = np.pad(A, ((1, 1), (0, 0), (0, 0)))

    for k in range(200):
        pad = (0, 1) if k % 2 == 1 else (1, 0)
        A = np.pad(A, (pad, (0, 0), (0, 0)))
        new_A = A.copy()
        neighbors = np.zeros_like(A)

        for z, y, x in product(range(1, k+3), range(5), range(5)):

            n = A[z-1, 1, 2] if y == 0 else A[z, y-1, x]
            s = A[z-1, 3, 2] if y == 4 else A[z, y+1, x]
            e = A[z-1, 2, 3] if x == 4 else A[z, y, x+1]
            w = A[z-1, 2, 1] if x == 0 else A[z, y, x-1]

            neighbors[z, y, x] = n + s + w + e

            # inner grid
            if (y, x) == (1, 2):  # N - row 0
                neighbors[z, y, x] += A[z+1, 0, :].sum()
            elif (y, x) == (2, 3):  # E - column 4
                neighbors[z, y, x] += A[z+1, :, 4].sum()
            elif (y, x) == (3, 2):  # S - row 4
                neighbors[z, y, x] += A[z+1, 4, :].sum()
            elif (y, x) == (2, 1):  # W - column 0
                neighbors[z, y, x] += A[z+1, :, 0].sum()

        # conway rules
        new_A[(A == 1) & (neighbors != 1)] = 0
        new_A[(A == 0) & ((neighbors == 1) | (neighbors == 2))] = 1
        A = new_A

        # set center to zero
        A[:, 2, 2] = 0

    return A.sum()


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

bugs = np.array([[1 if c == "#" else 0 for c in row] for row in data.splitlines()], dtype=int)
print("Part 1:", conway(bugs.copy()))
print("Part 2:", recursive_conway(bugs))

e = timer()
print(f"time: {e-s}")
