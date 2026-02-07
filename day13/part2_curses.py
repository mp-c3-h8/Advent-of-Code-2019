import curses
import os.path
import sys
from curses import wrapper
import time
from typing import Generator

'''
Windows:
get curses here: https://github.com/zephyrproject-rtos/windows-curses
as of now only supports python up to 3.13
use a dedicated powershell
'''

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


TILES = [" ", "█", "⬚", "▬", "●"]


def main(stdscr, program: list[int]):
    global TILES

    curses.curs_set(0)
    # curses.cbreak()
    stdscr.nodelay(True)
    stdscr.clear()
    stdscr.refresh()

    game = game_control_gen(program)
    next(game)  # we miss a single pixel

    ball_pos = (1, 45)
    bar_pos = (1, 45)
    score = 0
    speed = 1  # 1 to 5
    joystick = 0

    stdscr.addstr(6, 45, "Change Speed: [w] [s]")
    stdscr.addstr(8, 45, f"Speed: {speed}/5")

    i = 0
    try:
        while True:
            (x, y, tile) = game.send(joystick)

            if x == -1:
                score = tile
                stdscr.addstr(1, 45, "                ")
                stdscr.addstr(1, 45, "Score: " + str(score))
            elif tile == 0 and ((y, x) == ball_pos or (y, x) == bar_pos):  # no flicker
                pass
            elif tile == 3:
                stdscr.addstr(*bar_pos, " ")
                stdscr.addstr(y, x, TILES[tile])
                bar_pos = (y, x)
            elif tile == 4:
                stdscr.addstr(*ball_pos, " ")
                stdscr.addstr(y, x, TILES[tile])
                ball_pos = (y, x)
            else:
                stdscr.addstr(y, x, TILES[tile])

            # speed input
            try:
                key = stdscr.getkey()
            except:
                key = None

            if key is not None:
                if key == "w":
                    if speed < 5:
                        speed += 1
                        stdscr.addstr(8, 45, f"Speed: {speed}/5")
                elif key == "s":
                    if speed > 1:
                        speed -= 1
                        stdscr.addstr(8, 45, f"Speed: {speed}/5")

            stdscr.refresh()

            # determine joystick position
            if ball_pos[1] < bar_pos[1]:
                joystick = -1
            elif ball_pos[1] > bar_pos[1]:
                joystick = 1
            else:
                joystick = 0

            # speed control
            i += 1
            if i > 960 and speed != 5:
                time.sleep((5-speed)*0.001)
    except StopIteration:
        pass

    # game over
    stdscr.nodelay(False)
    stdscr.addstr(4, 7, f"Game Won! Final Score: {score}")
    stdscr.addstr(6, 7, f"[E]: Play Again.")
    stdscr.addstr(7, 7, f"[Other]: Exit.")

    key = stdscr.getkey()
    if key == "e":
        wrapper(main, program)


if __name__ == "__main__":

    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()
    program = list(map(int, data.split(",")))
    program[0] = 2

    wrapper(main, program)
