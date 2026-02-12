import os.path
import os
from timeit import default_timer as timer
import numpy as np
from scipy.ndimage import convolve


def conway(bugs: np.ndarray) -> int:
    biodiversities: set[int] = set()
    power_two = np.array([2**i for i in range(25)], dtype=int).reshape((5, 5))
    kernel = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=np.int8)

    for k in range(1, 10**6):
        bio = (power_two * bugs).sum()
        if bio in biodiversities:
            return bio
        biodiversities.add(bio)
        neighbors = convolve(bugs, kernel, mode="constant")
        bugs = (bugs & (neighbors == 1)) | (~bugs & ((neighbors == 1) | (neighbors == 2)))

    else:
        raise ValueError("Max iterations reached.")


def recursive_conway(A: np.ndarray) -> int:
    A = A.reshape((1, 5, 5))
    A = np.pad(A, ((1, 1), (0, 0), (0, 0)))
    kernel = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=np.int8)

    for k in range(200):
        # alternate between adding an inner or outer grid
        pad = (0, 1) if k % 2 == 1 else (1, 0)
        A = np.pad(A, (pad, (0, 0), (0, 0)))

        # outer and inner grid neighbors are treated as 0
        neighbors = convolve(A, kernel, mode="constant", axes=(1, 2))

        # skips outermost and innermost grid
        # neighbors towards outer grid
        neighbors[:-1, 1, 2] += A[1:, 0, :].sum(axis=1)  # N
        neighbors[:-1, 2, 3] += A[1:, :, 4].sum(axis=1)  # E
        neighbors[:-1, 3, 2] += A[1:, 4, :].sum(axis=1)  # S
        neighbors[:-1, 2, 1] += A[1:, :, 0].sum(axis=1)  # W

        # neighbors towards inner grid (around (2,2))
        neighbors[1:, 0, :] += A[:-1, 1, 2, None]  # N
        neighbors[1:, 4, :] += A[:-1, 3, 2, None]  # S
        neighbors[1:, :, 4] += A[:-1, 2, 3, None]  # E
        neighbors[1:, :, 0] += A[:-1, 2, 1, None]  # W

        # old version: loop is way slower
        # skips outermost and innermost grid
        # for z in range(1, k+3):
        #     # towards outer grid
        #     neighbors[z, 0, :] += A[z-1, 1, 2]  # N
        #     neighbors[z, 4, :] += A[z-1, 3, 2]  # S
        #     neighbors[z, :, 4] += A[z-1, 2, 3]  # E
        #     neighbors[z, :, 0] += A[z-1, 2, 1]  # W

        #     # towards inner grid (around (2,2))
        #     neighbors[z, 1, 2] += A[z+1, 0, :].sum()  # N
        #     neighbors[z, 2, 3] += A[z+1, :, 4].sum()  # E
        #     neighbors[z, 3, 2] += A[z+1, 4, :].sum()  # S
        #     neighbors[z, 2, 1] += A[z+1, :, 0].sum()  # W

        A = (A & (neighbors == 1)) | (~A & ((neighbors == 1) | (neighbors == 2)))

        # set center to zero
        A[:, 2, 2] = 0

    return A.sum()


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

bugs = np.array([[1 if c == "#" else 0 for c in row] for row in data.splitlines()], dtype=np.int8)
print("Part 1:", conway(bugs.copy()))
print("Part 2:", recursive_conway(bugs))

e = timer()
print(f"time: {e-s}")
