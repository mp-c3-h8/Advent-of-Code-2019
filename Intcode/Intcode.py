from itertools import zip_longest
from collections import defaultdict

type Program = list[int]
type Memory = defaultdict[int, int]

type Value = int
type Address = int
type OpCode = int

type Parameter = int
type ParamterMode = int
type Argument = tuple[Parameter, ParamterMode]


class Computer:
    # opcode: arity
    opcodes: dict[int, int] = {
        1: 3,  # add
        2: 3,  # mul
        3: 1,  # input
        4: 1,  # output
        5: 2,  # jump if true
        6: 2,  # jump if false
        7: 3,  # less than
        8: 3,  # equal
        99: 0,  # terminate
    }

    def __init__(self, program: Program, input_values: list[int]) -> None:
        self.load(program, input_values)

    def load(self, program: Program, input_values: list[int] = []) -> None:
        self.memory: Memory = defaultdict(int, {i: x for i, x in enumerate(program)})
        self.pointer: int = 0
        self.relative_base: int = 0
        self.terminated: bool = False
        self.input_values: list[int] = input_values
        self.output_values: list[int] = []

    def run(self, loop: bool = False) -> None:
        while not self.terminated:
            opcode, modes = self.split(self[self.pointer])
            arity = Computer.opcodes[opcode]
            params: list[Parameter] = [self[i] for i in range(self.pointer+1, self.pointer+arity+1)]
            arguments: list[Argument] = list(zip_longest(params, modes, fillvalue=0))
            # values = [self[p] if mode == 0 else p for p, mode in zip_longest(params, modes, fillvalue=0)]
            self.execute(opcode, arguments)
            if opcode == 4 and loop:  # a bit hacky
                return

    def execute(self, opcode: OpCode, arguments: list[Argument]) -> None:
        match opcode:
            case 1:  # add
                self.add(*arguments)
            case 2:  # mul
                self.mul(*arguments)
            case 3:  # input
                self.input(*arguments)
            case 4:  # output
                self.output(*arguments)
            case 5:  # jump if true
                self.jump_if_true(*arguments)
            case 6:  # jump if false
                self.jump_if_false(*arguments)
            case 7:  # less than
                self.less_than(*arguments)
            case 8:  # equal
                self.equal(*arguments)
            case 99:  # terminate
                self.terminate()
            case _:  # unknown
                raise ValueError(f"Opcode {opcode} not implemented.")

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

    def split(self, value: Value) -> tuple[OpCode, list[ParamterMode]]:
        if value <= 99:
            return value, []
        else:
            val_str = str(value)
            opcode = int(val_str[-2:])
            modes = list(map(int, reversed(val_str[:-2])))
            return opcode, modes

    def set_input(self, value: Value) -> None:
        self.input_values.append(value)

    def add(self, x: Argument, y: Argument, z: Argument) -> None:
        self[self.get_address(z)] = self.get_value(x) + self.get_value(y)
        self.pointer += 4

    def mul(self, x: Argument, y: Argument, z: Argument) -> None:
        self[self.get_address(z)] = self.get_value(x) * self.get_value(y)
        self.pointer += 4

    def input(self, z: Argument) -> None:
        if len(self.input_values) == 0:
            raise ValueError("No value provided for input instruction")
        self[self.get_address(z)] = self.input_values.pop(0)
        self.pointer += 2

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

    def __getitem__(self, address: Address) -> Value:
        return self.memory[address]

    def __setitem__(self, address: Address, value: Value) -> None:
        self.memory[address] = value

    def __str__(self) -> str:
        return ",".join(str(x) for x in self.memory.values())

    def __iter__(self):
        return self

    def __next__(self) -> int | None:
        self.run(True)
        return self.output_values.pop() if self.output_values else None
