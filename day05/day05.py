import os.path
import sys
from timeit import default_timer as timer

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'Intcode'))
from Intcode import Computer  # noqa

s = timer()


input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

program = list(map(int, data.split(",")))
computer = Computer(program, [1])
computer.run()
print("Part 1:", computer.outputs[-1])

computer.load(program, [5])
computer.run()
print("Part 2:", computer.outputs[-1])

e = timer()
print(f"time: {e-s}")
