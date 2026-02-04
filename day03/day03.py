import os.path
from timeit import default_timer as timer

type Pos = tuple[int, int]  # (y,x) y downwards
type Dir = tuple[int, int]
type Steps = int
type Wire = dict[Pos, Steps]

DIRS: dict[str, Dir] = {"U": (-1, 0), "R": (0, 1), "D": (1, 0), "L": (0, -1)}


def create_wire(wire_str: str) -> Wire:
    global DIRS
    pos: Pos = (0, 0)
    wire: Wire = {}
    steps: Steps = 0
    for path in wire_str.split(","):
        d_str, num_str = path[0], path[1:]
        d = DIRS[d_str]
        num = int(num_str)
        for i in range(1, num+1):
            pos = (pos[0]+d[0], pos[1]+d[1])
            steps += 1
            if pos not in wire:
                wire[pos] = steps
    return wire


def solve(data: str) -> tuple[int, int]:
    wire1, wire2 = map(create_wire, data.split("\n"))
    crossings = set(wire1).intersection(wire2)
    p1 = min(abs(y)+abs(x) for y, x in crossings)
    p2 = min(wire1[pos] + wire2[pos] for pos in crossings)

    return p1, p2


s = timer()


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

p1, p2 = solve(data)
print("Part 1:", p1)
print("Part 2:", p2)


e = timer()
print(f"time: {e-s}")
