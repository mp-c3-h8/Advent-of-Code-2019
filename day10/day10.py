import os.path
from timeit import default_timer as timer
from math import gcd
from math import atan2

type Pos = tuple[int, int]  # y downwards
type Map = set[Pos]


# approach similar to "Sieve of Eratosthenes"
def detectable_asteroids(space_map: Map, station: Pos, dimy: int, dimx: int) -> list[Pos]:
    # sort by manhatten distant to chosen station
    asteroids = sorted(space_map - {station}, key=lambda z: abs(z[0]-station[0]) + abs(z[1]-station[1]))
    blocked: set[Pos] = set()
    detectable: list[Pos] = []

    for asteroid in asteroids:
        if asteroid in blocked:
            continue

        detectable.append(asteroid)
        # asteroid is detectable because it is not "marked" (see Sieve)
        # now we calc what it blocks ("mark multiples")
        dy, dx = asteroid[0]-station[0], asteroid[1]-station[1]
        slope_gcd = gcd(dy, dx)
        dy //= slope_gcd
        dx //= slope_gcd  # dy and dx are now coprime
        ray_y, ray_x = asteroid  # the ray we cast

        while 0 <= ray_y < dimy and 0 <= ray_x < dimx:
            ray_x += dx
            ray_y += dy
            if (ray_y, ray_x) in space_map:
                blocked.add((ray_y, ray_x))
    return detectable


def best_place(space_map: Map, dimy: int, dimx: int) -> tuple[list[Pos], Pos]:
    asteroids, station = max(((detectable_asteroids(space_map, station, dimy, dimx), station)
                             for station in space_map), key=lambda x: len(x[0]))
    return asteroids, station


# faster with angles/slopes
def best_place2(space_map: Map) -> tuple[set[Pos], Pos]:
    slopes, station = max(((get_slopes(space_map, station), station) for station in space_map), key=lambda x: len(x[0]))
    return slopes, station


def get_slopes(space_map: Map, station: Pos) -> set[Pos]:
    slopes: set[Pos] = set()
    for asteroid in space_map:
        if station == asteroid:
            continue
        dy, dx = asteroid[0]-station[0], asteroid[1]-station[1]
        slope_gcd = gcd(dy, dx)
        dy //= slope_gcd
        dx //= slope_gcd  # dy and dx are now coprime
        slopes.add((dy, dx))
    return slopes


def vaporization(space_map: Map, slopes: set[Pos], station: Pos) -> int:
    # sort by angles
    sort = sorted(slopes, key=lambda x: atan2(x[1], x[0]), reverse=True)

    # no full rotation needed, just pick by index
    slope_200 = sort[199]
    vap_200 = (station[0]+slope_200[0], station[1]+slope_200[1])
    while (vap_200 not in space_map):
        vap_200 = (vap_200[0]+slope_200[0], vap_200[1]+slope_200[1])

    return vap_200[0] + vap_200[1]*100


s = timer()


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read().splitlines()

space_map: Map = {(y, x) for y, row in enumerate(data) for x, c in enumerate(row) if c == "#"}
dimy, dimx = len(data), len(data[0])
asteroids, station = best_place(space_map, dimy, dimx)
print("Part 1 (old):", len(asteroids))

e = timer()
print(f"time: {e-s}")


asteroids, station = best_place2(space_map)
print("Part 1:", len(asteroids))
print("Part 2:", vaporization(space_map, asteroids, station))

s = timer()
print(f"time: {s-e}")
