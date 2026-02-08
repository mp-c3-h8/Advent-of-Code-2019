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


def fewest_steps(program: list[int]) -> tuple[Grid, Pos, int]:
    global INV
    dirs = DIRS.items()
    grid: Grid = {0: "S"}
    computer = Computer(program, [])

    # (steps,pos,droid_on_pos)
    q: deque[tuple[int, Pos, Computer]] = deque([(0, 0, computer)])

    min_steps = -1
    pos_oxy = 0
    while q:
        steps, pos, computer = q.popleft()

        for command, new_pos in ((com, n) for com, d in dirs if (n := pos+d) not in grid):
            computer.add_input(command)
            status = next(computer)
            match status:
                case 0:
                    grid[new_pos] = "#"
                case 1:
                    grid[new_pos] = " "
                    q.append((steps+1, new_pos, deepcopy(computer)))
                    computer.add_input(INV[command])  # rewind
                    next(computer)
                case 2:
                    grid[new_pos] = "O"
                    pos_oxy = new_pos
                    min_steps = steps+1
                    q.append((steps+1, new_pos, deepcopy(computer)))  # keep exploring
                    computer.add_input(INV[command])  # rewind
                    next(computer)
                case _:
                    raise ValueError(f"Status code {status} unknown")
    return grid, pos_oxy, min_steps


def oxygen_fill(grid: Grid, pos_oxy: Pos) -> int:
    dirs = DIRS.values()
    # (minutes,count,pos)
    q: list[tuple[int, int, Pos]] = ([(0, 0, pos_oxy)])
    heapify(q)
    seen: set[Pos] = set({pos_oxy})

    i = 0
    minutes = -1
    while q:
        minutes, _, pos = heappop(q)

        for d in dirs:
            new_pos = pos+d
            if new_pos not in seen and grid[new_pos] == " ":
                seen.add(new_pos)
                i += 1
                heappush(q, (minutes+1, i, new_pos))
    return minutes


def print_grid(grid: Grid) -> None:
    pos = [(int(z.imag), int(z.real)) for z in grid]
    y_max, x_max = map(max, *pos)
    y_min, x_min = map(min, *pos)
    for y in range(y_min-2, y_max+3):
        for x in range(x_min-2, x_max+3):
            print(grid[x+y*1j] if x+y*1j in grid else "?", end="")
        print()


s = timer()


input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

program = list(map(int, data.split(",")))
grid, pos_oxy, steps = fewest_steps(program)
print_grid(grid)
print("Part 1:", steps)
print("Part 2:", oxygen_fill(grid, pos_oxy))

e = timer()
print(f"time: {e-s}")
