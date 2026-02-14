import os.path
import sys
import os
from timeit import default_timer as timer

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'Intcode'))
from Intcode import Computer  # noqa


def solve(program: list[int], part2: bool = False) -> int:
    computer = Computer(program, [])
    if not part2:
        script = [
            "NOT A T",
            "NOT A J",
            "NOT C T",
            "AND D T",
            "OR T J",
            "NOT A T",
            "OR T J",
            "WALK"
        ]
    else:
        script = [
            "NOT C J",
            "AND D J",
            "AND H J",
            "NOT B T",
            "AND D T",
            "OR T J",
            "NOT A T",
            "OR T J",
            "RUN"
        ]

    next(computer)  # prompt

    for string in script:
        for c in string:
            computer.add_input(ord(c))
        computer.add_input(ord("\n"))

    computer.run()

    return computer.output_values[-1]


s = timer()


input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

program = list(map(int, data.split(",")))
print("Part 1:", solve(program,False))
print("Part 2:", solve(program,True))


e = timer()
print(f"time: {e-s}")
