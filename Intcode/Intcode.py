from collections import deque, defaultdict

type Program = list[int]
type Memory = defaultdict[int, int]

type Value = int
type Address = int
type OpCode = int


class Computer:
    __slots__ = ["mem", "pointer", "relative_base", "terminated",
                 "input_values", "output_values", "input_default", "lan"]

    # opcode: arity
    opcodes: list = [
        0,  # 0 = dummy
        3,  # 1 = add
        3,  # 2 = mul
        1,  # 3 = input
        1,  # 4 = output
        2,  # 5 = jump if true
        2,  # 6 = jump if false
        3,  # 7 = less than
        3,  # 8 = equal
        1,  # 9 = relative base offset
    ]

    def __init__(self, program: Program, input_values: list[int]) -> None:
        self.load(program, input_values)

    def load(self, program: Program, input_values: list[int]) -> None:
        self.mem: Memory = defaultdict(int, ((i, p) for i, p in enumerate(program)))
        self.pointer: int = 0
        self.relative_base: int = 0
        self.terminated: bool = False
        self.input_values: deque[int] = deque(input_values)
        self.output_values: list[int] = []
        self.input_default: int | None = None
        self.lan: list[Computer] | None = None

    def run(self, loop: bool = False, stop_before_input: bool = False) -> None:
        temp: list[int] = []
        while not self.terminated:
            op = self.mem[self.pointer]
            opcode = op % 100
            if opcode == 99:
                self.terminated = True
                self.pointer += 1
                return
            arity = Computer.opcodes[opcode]
            addrs, vals = self.process_code(op, arity)
            if opcode == 1:  # add
                self.mem[addrs[2]] = vals[0] + vals[1]
                self.pointer += 4
            elif opcode == 2:  # mul
                self.mem[addrs[2]] = vals[0] * vals[1]
                self.pointer += 4
            elif opcode == 3:  # input
                if stop_before_input:
                    return
                self.input(addrs[0])
            elif opcode == 4:  # output
                if self.lan is not None:
                    temp.append(vals[0])
                    if len(temp) == 3:
                        print(temp)
                        if temp[0] == 255:
                            print(temp)
                            for comp in self.lan:
                                comp.terminated = True
                        self.lan[temp[0]].input_values.extend(temp[1:])
                        temp = []
                    self.pointer += 2
                else:
                    self.output_values.append(vals[0])
                    self.pointer += 2
                if loop:  # a bit hacky
                    return
            elif opcode == 5:  # jump if true
                self.pointer = vals[1] if vals[0] != 0 else self.pointer + 3
            elif opcode == 6:  # jump if false
                self.pointer = vals[1] if vals[0] == 0 else self.pointer + 3
            elif opcode == 7:  # less than
                self.mem[addrs[2]] = 1 if vals[0] < vals[1] else 0
                self.pointer += 4
            elif opcode == 8:  # equal
                self.mem[addrs[2]] = 1 if vals[0] == vals[1] else 0
                self.pointer += 4
            elif opcode == 9:  # relative base offset
                self.relative_base += vals[0]
                self.pointer += 2
            else:
                raise ValueError(f"Opcode {opcode} unknown.")

    # def receive(self, vals: list[int]) -> None:
    #     with self._lock:
    #         self.input_values.extend(vals)

    def process_code(self, op: int, arity: int) -> tuple[list[int], list[int]]:
        addrs = []
        vals = []
        for i in range(arity):
            mode = (op // (10 ** (2 + i))) % 10
            param = self.mem[self.pointer+1+i]
            addr = param if mode == 0 else self.relative_base + param
            val = self.mem[param] if mode == 0 else param if mode == 1 else self.mem[self.relative_base + param]
            addrs.append(addr)
            vals.append(val)
        return addrs, vals

    def add_input(self, value: Value) -> None:
        self.input_values.append(value)

    def input(self, z: Address) -> None:
        if len(self.input_values) > 0:
            self.mem[z] = self.input_values.popleft()
            self.pointer += 2
        elif self.input_default is not None:
            self.mem[z] = self.input_default
            self.pointer += 2
        else:
            raise ValueError("No value provided for input instruction")

    def __str__(self) -> str:
        return ",".join(str(x) for x in self.output_values)

    def __iter__(self):
        return self

    def __next__(self) -> int:
        self.run(True)
        if len(self.output_values) > 0:
            return self.output_values.pop()
        else:
            raise StopIteration
