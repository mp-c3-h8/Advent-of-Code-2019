import os.path
import sys
from timeit import default_timer as timer

type Pos = complex  # y downwards
type Dir = complex
type Color = int

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'Intcode'))
from Intcode import Computer  # noqa


# 0 = black, 1 = white
def paint_hull(program: list[int], start_color: int) -> tuple[int, set[Pos]]:
    computer = Computer(program, [])
    pos: Pos = 0
    d: Dir = -1j
    visited: set[Pos] = set({pos})
    white_panels: set[Pos] = set()
    curr_color: Color = start_color

    for _ in range(10**6):
        computer.add_input(curr_color)
        to_paint = next(computer)
        if computer.terminated:
            break
        if to_paint == 0:  # black
            white_panels -= {pos}
        elif to_paint == 1:  # white
            white_panels |= {pos}
        else:
            raise ValueError(f"Colorcode {to_paint} unknown.")

        turn = next(computer)
        if turn == 0:  # left 90 degrees
            d *= -1j
        elif turn == 1:  # right 90 degrees
            d *= 1j
        else:
            raise ValueError(f"Turn instruction {turn} unknown.")
        pos += d
        visited.add(pos)
        curr_color = 1 if pos in white_panels else 0
    else:
        raise ValueError("Max iterations reached.")

    return len(visited), white_panels


def print_hull(white_panels: set[Pos]) -> None:
    panels = [(int(z.imag), int(z.real)) for z in white_panels]
    y_max, x_max = map(max, *panels)
    y_min, x_min = map(min, *panels)
    for y in range(y_min, y_max+1):
        for x in range(x_min, x_max+1):
            print("█" if x+y*1j in white_panels else " ", end="")
        print()


s = timer()


input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

program = list(map(int, data.split(",")))

num_visited, white_panels = paint_hull(program, 0)
print("Part 1:", num_visited)

num_visited, white_panels = paint_hull(program, 1)
print("Part 2:")
print_hull(white_panels)


e = timer()
print(f"time: {e-s}")
