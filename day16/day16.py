import os.path
import os
from timeit import default_timer as timer
from typing import Iterator
from itertools import cycle


def pattern(pos: int) -> Iterator[int]:
    base = cycle([0, 1, 0, -1])
    while True:
        val = next(base)
        for _ in range(pos):
            yield val


def fft(signal: list[int], num_phases: int) -> int:

    for i in range(num_phases):
        new = []
        for i in range(len(signal)):
            pat = pattern(i+1)
            next(pat)
            app = abs(sum(s*p for s, p in zip(signal, pat))) % 10
            new.append(app)
        signal = new
    return int("".join(str(s) for s in signal[:8]))


def fft2(data: str):
    offset = int(data[:7], 10)
    signal = list(map(int, data)) * 10000
    n = len(signal)

    for _ in range(100):
        # all coefficients are 1s....
        partial_sum = sum(signal[j] for j in range(offset, n))
        for j in range(offset, n):
            t = partial_sum
            partial_sum -= signal[j]
            signal[j] = t % 10

    return int("".join(str(s) for s in signal[offset:offset+8]))


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

signal = [int(x) for x in data]
print("Part 1:", fft(signal, 100))
print("Part 2:", fft2(data))

e = timer()
print(f"time: {e-s}")
