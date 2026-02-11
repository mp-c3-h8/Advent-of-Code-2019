import os.path
import sys
import os
from timeit import default_timer as timer
from concurrent.futures import ThreadPoolExecutor


dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'Intcode'))
from Intcode import Computer  # noqa


def network(program: list[int]) -> int:

    lan: list[Computer] = []
    for i in range(50):
        computer = Computer(program, [i])
        computer.input_default = -1
        computer.lan = lan
        lan.append(computer)

    with ThreadPoolExecutor(max_workers=50) as executor:
        for computer in lan:
            executor.submit(computer.run)

    return 0


s = timer()


input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

program = list(map(int, data.split(",")))
network(program)

e = timer()
print(f"time: {e-s}")
