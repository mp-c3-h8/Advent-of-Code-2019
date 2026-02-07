from itertools import zip_longest
from collections import defaultdict
from typing import Iterator

type Program = list[int]
type Memory = defaultdict[int, int]

type Value = int
type Address = int
type OpCode = int

type Parameter = int
type ParameterMode = int
type Argument = tuple[Parameter, ParameterMode]


class Computer:
    __slots__ = ["memory", "pointer", "relative_base", "terminated", "input_values", "output_values", "input_default"]

    # opcode: method,arity
    opcodes: dict[int, tuple[str, int]] = {
        1: ("add", 3),
        2: ("mul", 3),
        3: ("input", 1),
        4: ("output", 1),
        5: ("jump_if_true", 2),
        6: ("jump_if_false", 2),
        7: ("less_than", 3),
        8: ("equal", 3),
        9: ("relative_base_offset", 1),
        99: ("terminate", 0),
    }

    def __init__(self, program: Program, input_values: list[int]) -> None:
        self.load(program, input_values)

    def load(self, program: Program, input_values: list[int] = []) -> None:
        self.memory: Memory = defaultdict(int, {i: x for i, x in enumerate(program)})
        self.pointer: int = 0
        self.relative_base: int = 0
        self.terminated: bool = False
        self.input_values: list[int] = input_values
        self.input_default: int | None = None
        self.output_values: list[int] = []

    def run(self, loop: bool = False) -> None:
        while not self.terminated:
            opcode, modes = self.split(self[self.pointer])
            if opcode not in Computer.opcodes:
                raise ValueError(f"Invalid opcode {opcode}")
            method, arity = Computer.opcodes[opcode]
            params: list[Parameter] = [self[i] for i in range(self.pointer+1, self.pointer+arity+1)]
            arguments: list[Argument] = list(zip_longest(params, modes, fillvalue=0))
            execute = getattr(self, method)
            execute(*arguments)
            if opcode == 4 and loop:  # a bit hacky
                return

    # we cant have a "real pointer" for elements in our memory dict
    # solution: split write and read operations into two functions: get_address and get_value
    def get_address(self, argument: Argument) -> Address:
        # Parameters that an instruction writes to will never be in immediate mode.
        parameter, mode = argument
        match mode:
            case 0:  # position mode
                return parameter
            case 2:  # relative mode
                return self.relative_base + parameter
            case _:
                raise ValueError(f"Invalid parameter mode {mode}.")

    def get_value(self, argument: Argument) -> Value:
        parameter, mode = argument
        match mode:
            case 0:  # position mode
                return self[parameter]
            case 1:  # immediate mode
                return parameter
            case 2:  # relative mode
                return self[self.relative_base + parameter]
            case _:
                raise ValueError(f"Invalid parameter mode {mode}.")

    def split(self, value: Value) -> tuple[OpCode, list[ParameterMode]]:
        if value <= 99:
            return value, []
        else:
            val_str = str(value)
            opcode = int(val_str[-2:])
            modes = list(map(int, reversed(val_str[:-2])))
            return opcode, modes

    def add_input(self, value: Value) -> None:
        self.input_values.append(value)

    def add(self, x: Argument, y: Argument, z: Argument) -> None:
        self[self.get_address(z)] = self.get_value(x) + self.get_value(y)
        self.pointer += 4

    def mul(self, x: Argument, y: Argument, z: Argument) -> None:
        self[self.get_address(z)] = self.get_value(x) * self.get_value(y)
        self.pointer += 4

    def input(self, z: Argument) -> None:
        if len(self.input_values) > 0:
            self[self.get_address(z)] = self.input_values.pop(0)
            self.pointer += 2
        elif self.input_default is not None:
            self[self.get_address(z)] = self.input_default
            self.pointer += 2
        else:
            raise ValueError("No value provided for input instruction")

    def output(self, x: Argument) -> None:
        self.output_values.append(self.get_value(x))
        self.pointer += 2

    def terminate(self) -> None:
        self.terminated = True
        self.pointer += 1

    def jump_if_true(self, x: Argument, y: Argument) -> None:
        self.jump(self.get_value(x) != 0, self.get_value(y))

    def jump_if_false(self, x: Argument, y: Argument) -> None:
        self.jump(self.get_value(x) == 0, self.get_value(y))

    def jump(self, cond: bool, x: Value) -> None:
        if cond:
            self.pointer = x
        else:
            self.pointer += 3

    def less_than(self, x: Argument, y: Argument, z: Argument) -> None:
        self.set_to_one(self.get_value(x) < self.get_value(y), self.get_address(z))

    def equal(self, x: Argument, y: Argument, z: Argument) -> None:
        self.set_to_one(self.get_value(x) == self.get_value(y), self.get_address(z))

    def set_to_one(self, cond: bool, z: Address) -> None:
        self[z] = 1 if cond else 0
        self.pointer += 4

    def relative_base_offset(self, x: Argument) -> None:
        self.relative_base += self.get_value(x)
        self.pointer += 2

    def __getitem__(self, address: Address) -> Value:
        return self.memory[address]

    def __setitem__(self, address: Address, value: Value) -> None:
        self.memory[address] = value

    def __str__(self) -> str:
        return ",".join(str(x) for x in self.output_values)

    def __iter__(self):
        return self

    def __next__(self) -> int:
        self.run(True)
        if not self.terminated:
            return self.output_values.pop()
        else:
            raise StopIteration
