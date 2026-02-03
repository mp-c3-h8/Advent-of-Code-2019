import os.path
from timeit import default_timer as timer


s = timer()


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read().splitlines()

p1 = 0
p2 = 0

for line in data:
    num = int(line)
    fuel = num // 3 - 2
    p1 += fuel
    while fuel > 0:
        p2 += fuel
        fuel = fuel // 3 - 2

print("Part 1:", p1)
print("Part 2:", p2)


e = timer()
print(f"time: {e-s}")
