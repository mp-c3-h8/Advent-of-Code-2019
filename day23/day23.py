import os.path
import sys
import os
from timeit import default_timer as timer
from collections import deque


dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'Intcode'))
from Intcode import Computer  # noqa


class NAT(Computer):
    def __init__(self, lan: dict[int, Computer]) -> None:
        self.terminated: bool = False
        self.input_values: deque[int] = deque([])
        self.lan = lan
        self.is_idle = False

    def run(self, pause_after_output: bool = False, pause_before_input: bool = False) -> None:
        assert self.lan is not None
        last_y: list[int] = [-1]
        while not self.terminated:
            # check for idle
            lan_idle = True
            for computer in self.lan.values():
                if not computer.is_idle:
                    continue

                # computer has input values -> reactivate
                if len(computer.input_values) > 0:
                    computer.run()
                    lan_idle = False

            if not lan_idle:
                continue

            y = self.input_values.pop()
            x = self.input_values.pop()

            # part 2 check
            if y == last_y[-1]:
                print("Part 1:", last_y[1])
                print("Part 2:", y)
                # shutdown
                for computer in self.lan.values():
                    computer.terminated = True
            last_y.append(y)
            self.input_values.clear()

            # reactivate address 0 with input from NAT
            self.lan[0].input_values.extend([x, y])
            self.lan[0].run()


def network(program: list[int]) -> int:

    lan: dict[int, Computer] = dict()
    for i in range(50):
        computer = Computer(program, [i], 50)
        computer.input_default = -1
        computer.lan = lan
        lan[i] = computer

    lan[255] = NAT(lan)

    for computer in lan.values():
        computer.run()

    return 0


s = timer()


input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

program = list(map(int, data.split(",")))
network(program)

e = timer()
print(f"time: {e-s}")
