import os.path
import sys
import os
from timeit import default_timer as timer
import time

type Pos = tuple[int, int]  # y downwards
type Tile = int
type Screen = dict[Pos, Tile]

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'Intcode'))
from Intcode import Computer  # noqa


def get_screen(program: list[int]) -> Screen:
    computer = Computer(program, [])
    screen = {}
    for _ in range(10**6):
        x = next(computer)
        if computer.terminated:
            break
        y = next(computer)
        tile = next(computer)
        screen[(y, x)] = tile
    else:
        raise ValueError("Max iterations reached.")

    return screen


def beat_game(program:list[int]) -> int:
    program[0] = 2
    computer = Computer(program, [])
    screen = {}
    scores = []
    for _ in range(10**6):
        x = next(computer)
        if computer.terminated:
            break
        y = next(computer)
        tile = next(computer)
        
        if x == -1:
            scores.append((x,y,tile))
        else:
            screen[(y, x)] = tile
            if _ > 900:
                os.system("cls")
                print_screen(screen)
                print(scores)
                time.sleep(0.1)
    else:
        raise ValueError("Max iterations reached.")
    return 0


def print_screen(screen: Screen) -> None:
    TILES = {
        0: " ",
        1: "█",
        2: "#",
        3: "-",
        4: "o"
    }

    y_max, x_max = map(max, *screen)
    y_min, x_min = map(min, *screen)
    for y in range(y_min, y_max+1):
        for x in range(x_min, x_max+1):
            print(TILES[screen[(y, x)]] if (y, x) in screen else " ", end="")
        print()


s = timer()


input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

program = list(map(int, data.split(",")))

screen = get_screen(program)
print("Part 1:",sum(tile == 2 for tile in screen.values()))
#beat_game(program)

e = timer()
print(f"time: {e-s}")
