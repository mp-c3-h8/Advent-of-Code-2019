import os.path
import sys
import os
from timeit import default_timer as timer
from typing import Iterator

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'Intcode'))
from Intcode import Computer  # noqa


type Pos = tuple[int, int]  # y  downwards
type Grid = dict[Pos, str]


def part1(program: list[int]) -> int:
    computer = Computer(program, [])
    res = 0
    try:
        for y in range(50):
            for x in range(50):
                computer.load(program, [x, y])
                res += next(computer)
    except StopIteration:
        raise ValueError("Program error.")
    return res


def border() -> Iterator[Pos]:
    yield (1, 0)
    yield (0, 1)
    for dy in range(1, 5):
        for dx in range(5):
            yield (dy, dx)


def part2(program: list[int], w: int) -> int:
    computer = Computer(program, [])

    bottom_xy: dict[int, int] = {}
    bottom_yx: dict[int, int] = {}
    top_x, top_y = 0, 0
    bottom_x, bottom_y = 0, 0
    try:
        for _ in range(10**6):
            # top border of the beam
            for dx, dy in border():  # dy and dx switched!
                computer.load(program, [top_x + dx, top_y + dy])
                if next(computer) == 1:
                    top_y += dy
                    top_x += dx
                    break

            # bottom border of the beam
            for dy, dx in border():
                computer.load(program, [bottom_x + dx, bottom_y + dy])
                if next(computer) == 1:
                    bottom_y += dy
                    bottom_x += dx
                    bottom_xy[bottom_x] = bottom_y
                    if bottom_y in bottom_yx:
                        pass
                    else:
                        bottom_yx[bottom_y] = bottom_x
                    break

            if top_x <= int(w*1.5):
                continue
            if top_x - bottom_yx[top_y] < w-1:
                continue
            check_x = top_x-(w-1)
            if bottom_xy[check_x] - top_y < w-1:
                continue

            # found
            return check_x * 10_000 + top_y
        else:
            raise ValueError("Max iterations reached.")

    except StopIteration:
        raise ValueError("Program error.")


def print_grid(grid: Grid) -> None:
    y_max, x_max = map(max, *grid)
    y_min, x_min = map(min, *grid)
    for y in range(y_min, y_max+1):
        for x in range(x_min, x_max+1):
            print(grid[y, x] if (y, x) in grid else " ", end="")
        print()


s = timer()


input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

program = list(map(int, data.split(",")))

print("Part 1:", part1(program))
print("Part 2:", part2(program, 100))


e = timer()
print(f"time: {e-s}")
