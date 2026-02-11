import os.path
import sys
import os
from timeit import default_timer as timer
from collections import deque

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'Intcode'))
from Intcode import Computer  # noqa


type Pos = complex  # y = 1j downwards
type Dir = complex
type Grid = dict[complex, str]

DIRS: dict[str, Dir] = {"^": -1j, "v": 1j, "<": -1, ">": 1}
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


def part1(grid: Grid) -> tuple[int, str]:

    # pick robot position
    pos, facing = next(((pos, c) for pos, c in grid.items() if c in "^v<>"))
    d = DIRS[facing]

    dirs = DIRS.values()
    p1 = 0
    p2 = ""
    walked = 0

    for _ in range(10**6):
        # check for intersections
        # we visit every intersection twice -> p1 // 2 at the end
        if all((n := pos+d) in grid and grid[n] != "." for d in dirs):
            p1 += int(pos.real) * int(pos.imag)

        new_pos = pos+d
        if new_pos in grid and grid[new_pos] == "#":
            pos = new_pos
            walked += 1
            continue
        new_d = d*-1j  # left turn
        new_pos = pos + new_d
        if new_pos in grid and grid[new_pos] == "#":
            p2 = ",".join((p2, str(walked), "L"))
            walked = 1
            pos = new_pos
            d = new_d
            continue
        new_d = d*1j  # right turn
        new_pos = pos + new_d
        if new_pos in grid and grid[new_pos] == "#":
            p2 = ",".join((p2, str(walked), "R"))
            walked = 1
            pos = new_pos
            d = new_d
            continue
        # reached the end
        p2 += "," + str(walked)
        break
    else:
        raise ValueError("Reached max iterations.")

    return p1//2, p2


def part2() -> int:
    # solved by hand
    # L,10,L,8,R,8,L,8,R,6,L,10,L,8,R,8,L,8,R,6,R,6,R,8,R,8,R,6,R,6,L,8,L,10,R,6,R,8,R,8,R,6,R,6,L,8,L,10,R,6,R,8,R,8,R,6,R,6,L,8,L,10,R,6,R,8,R,8,L,10,L,8,R,8,L,8,R,6
    main = "A,A,B,C,B,C,B,C,B,A\n"
    A = "L,10,L,8,R,8,L,8,R,6\n"
    B = "R,6,R,8,R,8\n"
    C = "R,6,R,6,L,8,L,10\n"

    computer = Computer(program, [])
    computer.mem[0] = 2
    for rule in (main, A, B, C):
        for c in rule:
            computer.add_input(ord(c))
    computer.add_input(ord("n"))
    computer.add_input(ord("\n"))

    computer.run()

    return computer.output_values[-1]


s = timer()


input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

program = list(map(int, data.split(",")))
string, grid = create_grid(program)
p1, path = part1(grid)
print(string)
print(path)
print("Part 1:", p1)
print("part 2:", part2())

e = timer()
print(f"time: {e-s}")
