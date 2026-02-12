import os.path
import sys
import os
from timeit import default_timer as timer


dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'Intcode'))
from Intcode import Computer  # noqa


def play_game(program: list[int]) -> None:
    computer = Computer(program, [])

    while not computer.terminated:
        computer.run(False, True)
        out_ascii = "".join(chr(x) for x in computer.output_values)
        print(out_ascii)
        com = input(">>")
        for c in com:
            computer.add_input(ord(c))
        computer.add_input(ord("\n"))
        computer.run(True)

    play_game(program)


s = timer()


input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

program = list(map(int, data.split(",")))
play_game(program)

e = timer()
print(f"time: {e-s}")
