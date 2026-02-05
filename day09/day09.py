import os.path
import sys
from timeit import default_timer as timer

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'Intcode'))
from Intcode import Computer  # noqa


def boost(program: list[int], inp: int) -> int:
    computer = Computer(program, [inp])
    computer.run()
    if len(computer.output_values) != 1:
        raise ValueError("Computer broken :(")
    return computer.output_values.pop()


s = timer()


input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

program = list(map(int, data.split(",")))
print("Part 1:", boost(program, 1))
print("Part 2:", boost(program, 2))


e = timer()
print(f"time: {e-s}")
