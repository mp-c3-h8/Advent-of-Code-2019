import os.path
from timeit import default_timer as timer
import numpy as np
import re
from math import lcm


def part1(pos: np.ndarray, steps: int) -> int:
    vel = np.zeros_like(pos)
    for _ in range(steps):
        vel += np.sum(np.sign(pos - pos[:, np.newaxis]), axis=1)
        pos += vel

    pot = np.sum(abs(pos), axis=1)
    kin = np.sum(abs(vel), axis=1)
    energy = pot @ kin
    return energy


# dimensions are independent
# we find cycles for x,y,z independently and return the lcm
# the system is reversible: its sufficent to check for initial state
def part2(pos: np.ndarray) -> int:
    cycles = []
    for dim in pos.T:  # dim = x or y or z
        initial = dim.copy()
        vel = np.zeros_like(dim)
        for k in range(1, 10**7):
            vel += np.sum(np.sign(dim - dim[:, np.newaxis]), axis=1)
            dim += vel
            # this is faster than (dim == inital).all()
            # because numpy equivalency check does NOT shortcircuit
            for i in range(4):
                if dim[i] != initial[i] or vel[i] != 0:
                    break
            else:
                cycles.append(k)
                break
        else:
            raise ValueError("Max iterations reached.")
    return lcm(*cycles)


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

pos = np.array([int(c) for c in re.findall(r"-?\d+", data)], dtype=np.int16)
pos = np.reshape(pos, (-1, 3))

print("Part 1:", part1(pos.copy(), 1000))
print("Part 2:", part2(pos))

e = timer()
print(f"time: {e-s}")
