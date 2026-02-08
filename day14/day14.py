import os.path
from timeit import default_timer as timer
from collections import defaultdict
from math import ceil

type Material = str
type Quantity = int
type Part = tuple[Material, Quantity]

# (output_mat) : (output_quant, [ (input1_mat,input1_quant) , ...    ] 
type Factory = dict[Material, tuple[Quantity, list[Part]]]


def parse_part(part_str: str) -> Part:
    quantity, material = part_str.split(" ")
    return (material, int(quantity))


def create_factory(data: str) -> Factory:
    factory = {}
    for reaction in data.splitlines():
        inputs_str, output_str = reaction.split(" => ")
        output_material, output_quantity = parse_part(output_str)
        inputs = [parse_part(inp) for inp in inputs_str.split(", ")]
        factory[output_material] = (output_quantity, inputs)
    return factory


def ore_per_fuel(factory: Factory, amount: int = 1) -> int:
    q: list[Part] = [("FUEL", amount)]
    ore = 0
    leftovers: defaultdict[Material, Quantity] = defaultdict(int)

    while q:
        need_mat, need_quant = q.pop()

        if need_mat == "ORE":
            ore += need_quant
            continue

        # enough leftovers to skip reaction entirely?
        leftover_quant = leftovers[need_mat]
        if leftover_quant >= need_quant:
            leftovers[need_mat] -= need_quant
            continue

        # use up leftovers
        need_quant -= leftover_quant # cant get negative
        leftovers[need_mat] = 0

        # reactions needed
        react_quantitiy, parts = factory[need_mat]
        multiple = ceil(need_quant / react_quantitiy)  # multiple of reactions needed

        # new leftover
        leftovers[need_mat] += (multiple*react_quantitiy) - need_quant

        # q needed reactions
        for part in parts:
            mat, quant = part
            # BETTER: use "schedule generator" to combine common reactions
            q.append((mat, quant*multiple))
    return ore


def max_fuel(factory: Factory, ore_per_one_fuel: int) -> int:
    ORE_STORAGE = 1_000_000_000_000

    # function ore_per_fuel is monotonic
    fuel_low = ORE_STORAGE // ore_per_one_fuel

    # find upper bound
    fuel_high = fuel_low
    while (ore_per_fuel(factory, fuel_high) < ORE_STORAGE):
        fuel_high = round(fuel_high*1.2)

    # bisect
    while fuel_high - fuel_low != 1:
        fuel_mid = (fuel_low + fuel_high) // 2
        ore_mid = ore_per_fuel(factory, fuel_mid)
        if ore_mid > ORE_STORAGE:
            fuel_high = fuel_mid
        else:
            fuel_low = fuel_mid
    return (fuel_low + fuel_high) // 2


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

factory = create_factory(data)
ore_per_one_fuel = ore_per_fuel(factory)
print("Part 1:", ore_per_one_fuel)
print("Part 2:", max_fuel(factory, ore_per_one_fuel))

e = timer()
print(f"time: {e-s}")
