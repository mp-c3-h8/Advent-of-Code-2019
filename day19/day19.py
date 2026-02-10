import os.path
import os
from timeit import default_timer as timer
from typing import Iterator
from collections import defaultdict, deque
from heapq import heapify, heappop, heappush

type Pos = tuple[int, int]  # (y,x)  y downwards
type Dir = tuple[int, int]
type Grid = dict[Pos, str]
type Node = int
type Graph = defaultdict[Node, list[Node]]
type Edges = dict[tuple[Node, Node], int]  # edge weights

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def neighbors(grid: Grid, pos: Pos) -> Iterator[tuple[Pos, Dir]]:
    global DIRS
    for d in DIRS:
        if (new_pos := (pos[0]+d[0], pos[1]+d[1])) in grid:
            yield new_pos, d


def create_graph(data: str) -> tuple[Graph, Edges, Node, Node]:
    grid = {(y, x): c for y, row in enumerate(data.splitlines()) for x, c in enumerate(row)}
    letters_to_node: dict[str, Node] = {}
    edges: Edges = {}
    graph: Graph = defaultdict(list)
    vertices: dict[Node, Pos] = {}

    # first pass: identify nodes, relabel to ints
    node: Node = 0
    for pos, letter in grid.items():
        if letter in ". #":
            continue

        hood = [(new_pos, d) for new_pos, d in neighbors(grid, pos)]
        try:
            node_pos = next(new_pos for new_pos, d in hood if grid[new_pos] == ".")
            second = next((grid[new_pos], new_pos, d) for new_pos, d in hood if grid[new_pos].isalpha())
            second_letter, second_letter_pos, second_letter_dir = second
        except StopIteration:
            continue

        # second letter direction matters...
        # FQ != QF
        if second_letter_dir in ((1, 0), (0, 1)):
            letters = letter + second_letter
        else:
            letters = second_letter + letter

        node += 1
        if letters in letters_to_node:
            # we've seen the teleporter "letters" already
            other_node = letters_to_node[letters]
            graph[node].append(other_node)
            graph[other_node].append(node)
            edges[(node, other_node)] = 1
            edges[(other_node, node)] = 1
        else:
            letters_to_node[letters] = node

        vertices[node] = node_pos
        grid[second_letter_pos] = "#"
        grid[pos] = "#"
        grid[node_pos] = str(node)

    # second pass: # flood fill/bfs for node
    for node, start_pos in vertices.items():
        q: deque[tuple[Pos, int]] = deque([(start_pos, 0)])
        seen: set[Pos] = set({start_pos})
        while q:
            pos, steps = q.popleft()
            for new_pos, d in neighbors(grid, pos):
                if new_pos in seen:
                    continue
                seen.add(new_pos)
                if grid[new_pos].isdigit():
                    other_node = int(grid[new_pos])
                    if ((node, other_node) in edges):
                        continue
                    graph[node].append(other_node)
                    graph[other_node].append(node)
                    edges[(node, other_node)] = steps+1
                    edges[(other_node, node)] = steps+1
                elif grid[new_pos] == ".":  # unvisited free space
                    q.append((new_pos, steps+1))

    start = letters_to_node["AA"]
    end = letters_to_node["ZZ"]
    return graph, edges, start, end


def print_grid(grid: Grid) -> None:
    y_max, x_max = map(max, *grid)
    y_min, x_min = map(min, *grid)
    for y in range(y_min, y_max+1):
        for x in range(x_min, x_max+1):
            if (y, x) in grid:
                if grid[(y, x)].isdigit():
                    c = grid[(y, x)].zfill(2)
                elif grid[(y, x)] == "#":
                    c = "██"
                else:
                    c = "  "
            else:
                c = "  "
            print(c, end="")
        print()


def shortest_path(graph: Graph, edges: Edges, start: Node, end: Node) -> int:
    q: list[tuple[int, Node, tuple[Node, ...]]] = [(0, start, (start,))]
    heapify(q)
    shortest_paths: dict[Node, int] = {}  # node: steps
    done: set[Node] = set()

    while q:
        steps, node, path = heappop(q)

        if node == end:
            print(f"path: {path}")
            return steps

        if node in done:
            continue
        done.add(node)

        for new_node in graph[node]:
            add_steps = edges[(node, new_node)]
            new_steps = steps + add_steps

            if new_node in done:
                continue
            if new_node in shortest_paths and shortest_paths[new_node] <= new_steps:
                continue

            shortest_paths[new_node] = new_steps
            heappush(q, (new_steps, new_node, path + (new_node,)))
    else:
        raise ValueError(f"Could not find a path to {end}")


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

graph, edges, start, end = create_graph(data)
p1 = shortest_path(graph, edges, start, end)
print("Part 1:", p1)


e = timer()
print(f"time: {e-s}")
