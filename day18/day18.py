import os.path
import os
from timeit import default_timer as timer
from collections import defaultdict, deque
from heapq import heapify, heappop, heappush
from itertools import product

type Pos = tuple[int, int]  # (y,x)  y downwards
type Grid = dict[Pos, str]
type Node = str  # key or door or player
type Graph = defaultdict[Node, list[Node]]
type Edges = dict[tuple[Node, Node], int]  # edge weights
type State = tuple[tuple[Node, ...], frozenset[Node]]  # (nodes,(collected_keys))

ROBOTS = ("@", "%", "$", "§")


# create a graph from the grid
# gets rid of the corridors and saves their lenghts as weights
def create_graph(data: str) -> tuple[Graph, Edges, int, Pos]:
    DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))
    grid = {(y, x): c for y, row in enumerate(data.splitlines()) for x, c in enumerate(row)}
    entity_map = {c: pos for pos, c in grid.items() if c not in ".#"}
    num_keys = sum(e.islower() for e in entity_map)
    pos_player = next(pos for e, pos in entity_map.items() if e == "@")
    graph: Graph = defaultdict(list)
    edges: Edges = {}

    # flood fill/bfs for every entity
    for entity, start in entity_map.items():
        q: deque[tuple[Pos, int]] = deque([(start, 0)])
        seen: set[Pos] = set({start})
        while q:
            pos, steps = q.popleft()

            for d in DIRS:
                new_pos = (pos[0]+d[0], pos[1]+d[1])
                if new_pos in grid and grid[new_pos] != "#" and new_pos not in seen:
                    seen.add(new_pos)
                    if grid[new_pos] in entity_map:
                        other_entity = grid[new_pos]
                        graph[entity].append(other_entity)
                        edges[(entity, other_entity)] = steps+1
                        edges[(other_entity, entity)] = steps+1
                    else:  # unvisited free space
                        q.append((new_pos, steps+1))
    return graph, edges, num_keys, pos_player


def part2_data(data: str, pos_player: Pos):
    pos_y, pos_x = pos_player
    arr = [[c for c in row] for row in data.splitlines()]
    for dy, dx in product((1, 0, -1), repeat=2):
        arr[pos_y+dy][pos_x+dx] = "#"
    for (dy, dx), c in zip(product((1, -1), repeat=2), ROBOTS):
        arr[pos_y+dy][pos_x+dx] = c
    data = "\n".join("".join(row) for row in arr)

    return data


def fewest_steps(graph: Graph, edges: Edges, start: tuple[Node, ...], num_keys: int) -> int:
    # state = (nodes,(collected_keys))
    q: list[tuple[int, State]] = [(0, (start, frozenset()))]
    heapify(q)
    shortest_paths: dict[State, int] = {}  # state: steps
    done: set[State] = set()
    search_keys_memo: dict[tuple[Node, frozenset[Node]], list[tuple[Node, int]]] = {}

    while q:
        steps, state = heappop(q)
        nodes, keys = state  # nodes = current positions

        if state in done:
            continue
        done.add(state)

        if len(keys) == num_keys:
            return steps

        for i, node in enumerate(nodes):
            # memo
            if (node, keys) in search_keys_memo:
                next_nodes = search_keys_memo[(node, keys)]
            else:
                next_nodes = search_keys(graph, edges, node, keys)
                search_keys_memo[(node, keys)] = next_nodes

            # new_node is always a new key
            for new_node, add_steps in next_nodes:
                new_keys = keys | {new_node}
                new_steps = steps + add_steps
                new_nodes = nodes[:i] + (new_node,) + nodes[i+1:]
                new_state = (new_nodes, new_keys)
                
                if new_state in done:
                    continue
                if new_state in shortest_paths and shortest_paths[new_state] <= new_steps:
                    continue
                
                shortest_paths[new_state] = new_steps
                heappush(q, (new_steps, new_state))
    else:
        raise ValueError("Could not find all keys :(")


# get newly reachable nodes (keys) for a given start and keyring
def search_keys(graph: Graph, edges: Edges, start: Node, keys: frozenset[Node]) -> list[tuple[Node, int]]:
    init = (0, start)  # (steps=prio,node)
    q: list[tuple[int, Node]] = [init]
    heapify(q)
    shortest_paths: dict[Node, int] = {}
    new_keys: set[Node] = set()
    done: set[Node] = set()

    while q:
        steps, node = heappop(q)

        if node in done:
            continue
        done.add(node)

        if node.islower() and node not in keys:
            new_keys.add(node)
            continue

        for new_node in graph[node]:
            if new_node in done:
                continue
            
            # cant open the door
            if new_node.isupper() and new_node.lower() not in keys:
                continue

            new_steps = steps + edges[(node, new_node)]
            if new_node in shortest_paths and shortest_paths[new_node] <= new_steps:
                continue

            shortest_paths[new_node] = new_steps
            heappush(q, (new_steps, new_node))
    return [(key, shortest_paths[key]) for key in new_keys]


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

graph, edges, num_keys, pos_player = create_graph(data)
print("Part 1:", fewest_steps(graph, edges, ("@",), num_keys))

data = part2_data(data, pos_player)
graph, edges, num_keys, pos_player = create_graph(data)
print("Part 2", fewest_steps(graph, edges, ROBOTS, num_keys))

e = timer()
print(f"time: {e-s}")
