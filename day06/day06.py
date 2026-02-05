import os.path
from timeit import default_timer as timer
from collections import defaultdict, deque
from copy import deepcopy

type Node = str
type Graph = defaultdict[Node, list[Node]]


def create_graph(data: str) -> Graph:
    graph = defaultdict(list)
    for line in data.splitlines():
        node_from, node_to = line.split(")")
        graph[node_from].append(node_to)
    return graph


def part1(graph: Graph) -> int:

    # graph is a DAG
    # the sums are eventually empty
    def pathlengths(curr: Node, length: int) -> int:
        return length + sum(pathlengths(n, length+1) for n in graph[curr])

    return pathlengths("COM", 0)


def part2(graph: Graph) -> int:
    # add reverse edges
    for node_from, node_to in deepcopy(graph).items():
        for node in node_to:
            graph[node].append(node_from)

    q: deque[tuple[Node, int]] = deque([("YOU", 0)])
    seen: set[Node] = set()
    while q:
        node, length = q.pop()
        seen.add(node)
        # path is unique
        if node == "SAN":
            return length-2
        for n in graph[node]:
            if n not in seen:
                q.append((n, length+1))
    else:
        raise ValueError("Path to Santa not found :(")


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()


graph = create_graph(data)
print("Part 1:", part1(graph))
print("Part 2:", part2(graph))

e = timer()
print(f"time: {e-s}")
