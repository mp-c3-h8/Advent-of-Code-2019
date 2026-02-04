import os.path
from timeit import default_timer as timer
from typing import Iterator
from collections import Counter


# creates valid passwords for part 1 but disregards ranges
def passwords(digits: list[int] = [], double: bool = False) -> Iterator[list[int]]:
    n = len(digits)
    if n == 0:
        for i in range(1, 10):
            yield from passwords([i], False)
    elif n < 5:
        last = digits[-1]
        yield from passwords(digits + [last], True)
        for i in range(last+1, 10):
            yield from passwords(digits + [i], double)
    else:  # n == 5
        last = digits[-1]
        yield digits + [last]
        if double:
            for i in range(last+1, 10):
                yield digits + [i]


def solve(pwd_min: int, pwd_max: int) -> tuple[int, int]:

    p1, p2 = 0, 0

    for digits in passwords():
        pwd = sum(10**(5-i)*x for i, x in enumerate(digits))
        if pwd_min <= pwd <= pwd_max:
            p1 += 1
            if (2 in Counter(digits).values()):
                p2 += 1
    return p1, p2


s = timer()


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()


pwd_min, pwd_max = map(int, data.split("-"))
p1, p2 = solve(pwd_min, pwd_max)
print("Part 1:", p1)
print("Part 2:", p2)


e = timer()
print(f"time: {e-s}")
