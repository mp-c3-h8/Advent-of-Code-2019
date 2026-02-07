import os.path
import sys
import os
from timeit import default_timer as timer
from typing import Generator, Any


dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'Intcode'))
from Intcode import Computer  # noqa


def game_control_gen(program: list[int]) -> Generator[tuple[int, int, int], int | None, None]:
    computer = Computer(program, [])
    try:
        for _ in range(10**6):
            x = next(computer)
            y = next(computer)
            tile = next(computer)
            computer.input_default = yield (x, y, tile)
        else:
            raise ValueError("Max iterations reached.")
    except StopIteration:
        pass


def get_blocks(program: list[int]) -> int:
    game = game_control_gen(program)
    return sum(tile == 2 for (x, y, tile) in game)


def beat_game(program: list[int]) -> int:
    program[0] = 2
    game = game_control_gen(program)
    next(game)  # we miss a single pixel
    score = ball_x = bar_x = joystick = 0

    try:
        for _ in range(10**6):
            (x, y, tile) = game.send(joystick)

            if x == -1:
                score = tile
                continue

            if tile == 3:
                bar_x = x
            elif tile == 4:
                ball_x = x

            # sufficient to only "follow" in x-direction
            if ball_x < bar_x:
                joystick = -1
            elif ball_x > bar_x:
                joystick = 1
            else:
                joystick = 0
        else:
            raise ValueError("Max iterations reached.")
    except StopIteration:
        pass

    return score


s = timer()


input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

program = list(map(int, data.split(",")))

print("Part 1:", get_blocks(program))
print("Part 2:", beat_game(program))

e = timer()
print(f"time: {e-s}")
