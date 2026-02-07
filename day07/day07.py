import os.path
import sys
from timeit import default_timer as timer
from itertools import permutations

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'Intcode'))
from Intcode import Computer  # noqa


def sim(program: list[int], phase_setting: tuple[int, ...]) -> int:
    inp = 0
    computer = Computer(program, [])
    for phase in phase_setting:
        computer.load(program, [phase, inp])
        computer.run()
        inp = computer.output_values[-1]
    return inp


def max_thrusters(program: list[int]) -> int:
    # brute force
    return max(sim(program, phase_setting) for phase_setting in permutations(range(5)))


def feedback(program: list[int], phase_setting: tuple[int, ...]) -> int:
    computers: list[Computer] = [Computer(program, [phase]) for phase in phase_setting]
    inp = 0
    output = 0
    while inp is not None:
        for computer in computers:
            computer.add_input(inp)
            try:
                inp = next(computer)
            except StopIteration:
                inp = None
                break
            output = inp
    return output


def max_feedback(program: list[int]) -> int:
    # brute force
    return max(feedback(program, phase_setting) for phase_setting in permutations(range(5, 10)))


s = timer()


input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

program = list(map(int, data.split(",")))
print("Part 1:", max_thrusters(program))
print("Part 2:", max_feedback(program))

e = timer()
print(f"time: {e-s}")
