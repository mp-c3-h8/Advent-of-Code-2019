from itertools import zip_longest


type Program = list[int]
type Value = int
type Address = int
type OpCode = int
type Modes = list[int]


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

    def __init__(self, program: Program = [], input_value: int = 0) -> None:
        self.load(program, input_value)
        self.terminated: bool = False
        self.input_value: int = input_value

    def load(self, program: Program, input_value: int = 0) -> None:
        self.memory = {i: x for i, x in enumerate(program)}
        self.size: int = len(self.memory)
        self.pointer: int = 0
        self.outputs: list[int] = []
        self.terminated: bool = False
        self.input_value: int = input_value

    def run(self) -> None:
        while not self.terminated:
            opcode, modes = self.split(self[self.pointer])
            if opcode not in Computer.opcodes:
                raise ValueError(f"Opcode {opcode} unknown.")
            arity = Computer.opcodes[opcode]
            params = [self[i] for i in range(self.pointer+1, self.pointer+arity+1)]
            values = [self[p] if mode == 0 else p for p, mode in zip_longest(params, modes, fillvalue=0)]
            match opcode:
                case 1:  # add
                    self.add(params[-1], *values[:2])
                case 2:  # mul
                    self.mul(params[-1], *values[:2])
                case 3:  # input
                    self.input(params[-1], self.input_value)
                case 4:  # output
                    self.output(*values)
                case 5:  # jump if true
                    self.jump(values[1], values[0] != 0)
                case 6:  # jump if false
                    self.jump(values[1], values[0] == 0)
                case 7:  # less than
                    self.set_to_one(params[-1], values[0] < values[1])
                case 8:  # equal
                    self.set_to_one(params[-1], values[0] == values[1])
                case 99:  # terminate
                    self.terminate()
                case _:  # unknown
                    raise ValueError(f"Opcode {opcode} not implemented.")
            if self.pointer >= self.size:
                self.terminate()

    def split(self, value: Value) -> tuple[OpCode, Modes]:
        if value <= 99:
            return value, []
        else:
            val_str = str(value)
            opcode = int(val_str[-2:])
            modes = list(map(int, reversed(val_str[:-2])))
            return opcode, modes

    def add(self, z: Address, x: Value, y: Value) -> None:
        self[z] = x + y
        self.pointer += 4

    def mul(self, z: Address, x: Value, y: Value) -> None:
        self[z] = x * y
        self.pointer += 4

    def input(self, z: Address, x: Value) -> None:
        self[z] = x
        self.pointer += 2

    def output(self, x: Value) -> None:
        self.outputs.append(x)
        self.pointer += 2

    def terminate(self) -> None:
        self.terminated = True
        self.pointer += 1

    def jump(self, x: Value, cond: bool) -> None:
        if cond:
            self.pointer = x
        else:
            self.pointer += 3

    def set_to_one(self, z: Address, cond: bool) -> None:
        self[z] = 1 if cond else 0
        self.pointer += 4

    def __getitem__(self, address: Address) -> Value:
        if address >= self.size:
            raise ValueError(f"Memory address {address} invalid for memory of size {self.size}.")
        return self.memory[address]

    def __setitem__(self, address: Address, value: Value) -> None:
        if address >= self.size:
            raise ValueError(f"Memory address {address} invalid for memory of size {self.size}.")
        self.memory[address] = value

    def __str__(self) -> str:
        return ",".join(str(x) for x in self.memory.values())
