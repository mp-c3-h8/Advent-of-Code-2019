import curses
import os.path
import sys
from curses import wrapper
import time

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'Intcode'))
from Intcode import Computer  # noqa

TILES = [" ", "█", "⬚", "▬", "●"]


def main(stdscr):
    global TILES

    curses.curs_set(0)
    # curses.cbreak()
    stdscr.nodelay(True)
    stdscr.clear()
    stdscr.refresh()

    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()
    program = list(map(int, data.split(",")))
    program[0] = 2
    computer = Computer(program, [])
    computer.input_default = 0

    ball_pos = (1, 45)
    bar_pos = (1, 45)
    score = 0
    speed = 1  # 1 to 5

    stdscr.addstr(6, 45, "Change Speed: [w] [s]")
    stdscr.addstr(8, 45, f"Speed: {speed}/5")

    i = 0
    while True:

        x = next(computer)
        if computer.terminated:
            break
        y = next(computer)
        tile = next(computer)

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

        # send input to computer
        if ball_pos[1] < bar_pos[1]:
            computer.input_values = [-1]
        elif ball_pos[1] > bar_pos[1]:
            computer.input_values = [1]
        else:
            computer.input_values = [0]

        # speed control
        i += 1
        if i > 960 and speed != 5:
            time.sleep((5-speed)*0.001)

    # game over
    stdscr.nodelay(False)
    stdscr.addstr(4, 7, f"Game Won! Final Score: {score}")
    stdscr.addstr(6, 7, f"[E]: Play Again.")
    stdscr.addstr(7, 7, f"[Other]: Exit.")

    key = stdscr.getkey()
    if key == "e":
        wrapper(main)


wrapper(main)
