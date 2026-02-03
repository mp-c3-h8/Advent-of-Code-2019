import os.path
from timeit import default_timer as timer
from itertools import product

type Program = list[int]


def computer(program: Program) -> int | None:
    n = len(program)
    curr = 0
    while curr < n:
        op = program[curr]
        match op:
            case 1:
                program[program[curr+3]] = program[program[curr+1]] + program[program[curr+2]]
                curr += 4
            case 2:
                program[program[curr+3]] = program[program[curr+1]] * program[program[curr+2]]
                curr += 4
            case 99:
                break
            case _:
                return None
    return program[0]


def part2(program: Program) -> int:
    for noun, verb in product(range(100), repeat=2):
        altered = program[:]
        altered[1] = noun
        altered[2] = verb
        if computer(altered) == 19690720:
            break
    else:
        raise ValueError("Couldnt find proper noun and verb.")
    return 100 * noun + verb


s = timer()


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

program = [int(x) for x in data.split(",")]
program2 = program[:]
program[1] = 12
program[2] = 2
print("Part 1:", computer(program))
print("Part 2:", part2(program2))

e = timer()
print(f"time: {e-s}")
