import os.path
import sys
import os
from timeit import default_timer as timer
from heapq import heapify, heappop, heappush
from copy import deepcopy
from collections import deque

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'Intcode'))
from Intcode import Computer  # noqa


type Pos = complex  # y = 1j downwards
type Dir = complex
type Grid = dict[complex, str]

DIRS: dict[int, Dir] = {1: -1j, 2: 1j, 3: -1, 4: 1}
INV: dict[int, int] = {1: 2, 2: 1, 3: 4, 4: 3}


def create_grid(program: list[int]) -> tuple[str, Grid]:
    computer = Computer(program, [])
    string = ""
    try:
        for _ in range(10**6):
            string += chr(next(computer))
        else:
            raise ValueError("Max iterations reached.")
    except StopIteration:
        pass
    grid = {x+y*1j: c for y, row in enumerate(string.strip().splitlines()) for x, c in enumerate(row)}
    return string, grid


def alignment_parameters(grid: Grid) -> int:

    # pick any scaffold starting position
    start = next((pos for pos, c in grid.items() if c != "."))

    dirs = DIRS.values()
    seen: set[Pos] = set({start})
    res = 0
    q: deque[Pos] = deque([start])

    # flood fill
    while q:
        pos = q.popleft()

        if all((n := pos+d) in grid and grid[n] != "." for d in dirs):
            res += int(pos.real) * int(pos.imag)

        for d in dirs:
            new_pos = pos+d
            if new_pos in grid and new_pos not in seen and grid[new_pos] != ".":
                seen.add(new_pos)
                q.append(new_pos)

    return res


s = timer()


input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

program = list(map(int, data.split(",")))
string, grid = create_grid(program)
print(string)
print("Part 1:", alignment_parameters(grid))

e = timer()
print(f"time: {e-s}")
