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
type Level = int
type LevelChange = int  # -1 or 0 or 1
type Edges = dict[tuple[Node, Node], tuple[int, LevelChange]]
type State = tuple[Node, Level]


DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def neighbors(grid: Grid, pos: Pos) -> Iterator[tuple[Pos, Dir]]:
    global DIRS
    for d in DIRS:
        if (new_pos := (pos[0]+d[0], pos[1]+d[1])) in grid:
            yield new_pos, d


def create_graph(data: str) -> tuple[Graph, Edges, Node, Node]:
    split = data.splitlines()
    dims = (len(split), len(split[0]))
    grid = {(y, x): c for y, row in enumerate(split) for x, c in enumerate(row)}
    letters_to_node: dict[str, Node] = {}
    edges: Edges = {}
    graph: Graph = defaultdict(list)
    vertices: dict[Node, Pos] = {}

    # first pass: identify portals, relabel to ints
    node: Node = 0
    for pos, first_letter in grid.items():
        if first_letter in "#. ":
            continue

        hood = [*neighbors(grid, pos)]
        try:
            node_pos = next(new_pos for new_pos, d in hood if grid[new_pos] == ".")
            second = next((grid[new_pos], new_pos, d) for new_pos, d in hood if grid[new_pos].isalpha())
            second_letter, second_letter_pos, second_letter_dir = second
        except StopIteration:
            continue

        # FQ != QF
        if second_letter_dir in ((1, 0), (0, 1)):
            letters = first_letter + second_letter
        else:
            letters = second_letter + first_letter

        # inner or outer portal?
        if all(0 <= coord+delta < dim for delta in (-3, 3) for dim, coord in zip(dims, node_pos)):
            # inner
            levelchange = -1
        else:
            # outer
            levelchange = 1

        node += 1
        if letters in letters_to_node:
            # we've seen the counterpart teleporter "letters" already
            other_node = letters_to_node[letters]
            graph[node].append(other_node)
            graph[other_node].append(node)
            edges[(node, other_node)] = (1, levelchange)
            edges[(other_node, node)] = (1, -levelchange)
        else:
            letters_to_node[letters] = node

        vertices[node] = node_pos
        grid[second_letter_pos] = "#"
        grid[pos] = "#"
        grid[node_pos] = str(node)

    # second pass: # flood fill/bfs for every node
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
                    edges[(node, other_node)] = (steps+1, 0)
                    edges[(other_node, node)] = (steps+1, 0)
                elif grid[new_pos] == ".":  # unvisited free space
                    q.append((new_pos, steps+1))

    start = letters_to_node["AA"]
    end = letters_to_node["ZZ"]
    return graph, edges, start, end


def print_grid(grid: Grid) -> None:
    y_max, x_max = map(max, *grid)
    y_min, x_min = map(min, *grid)
    for y in range(y_min-2, y_max+3):
        for x in range(x_min-2, x_max+3):
            print(grid[(y, x)] if (y, x) in grid else "?", end="")
        print()


def shortest_path(graph: Graph, edges: Edges, start: Node, end: Node, recursive: bool = False) -> int:
    q: list[tuple[int, int, State]] = [(0, 0, (start, 0))]
    heapify(q)
    shortest_paths: dict[State, int] = {}  # state: steps
    done: set[State] = set()

    while q:
        prio, steps, state = heappop(q)
        node, level = state

        if node == end and level == 0:
            return steps

        if state in done:
            continue
        done.add(state)

        for new_node in graph[node]:
            add_steps, levelchange = edges[(node, new_node)]
            new_steps = steps + add_steps
            new_level = level + levelchange

            if recursive:
                # can only climb if level < 0
                if level == 0 and levelchange == 1:
                    continue
            else:
                new_level = 0

            new_state = (new_node, new_level)
            if new_state in done:
                continue
            if new_state in shortest_paths and shortest_paths[new_state] <= new_steps:
                continue

            shortest_paths[new_state] = new_steps
            heappush(q, (new_steps+abs(new_level)*2, new_steps, new_state))
    else:
        raise ValueError(f"Could not find a path to {end}")


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

graph, edges, start, end = create_graph(data)
print("Part 1:", shortest_path(graph, edges, start, end))
print("Part 2:", shortest_path(graph, edges, start, end, True))


e = timer()
print(f"time: {e-s}")
