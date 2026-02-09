import os.path
import os
from timeit import default_timer as timer
from collections import defaultdict, deque
from heapq import heapify, heappop, heappush
from itertools import product

type Pos = tuple[int, int]  # (y,x)  y downwards
type Entity = str  # key or door or player
type EntityMap = dict[Entity, Pos]
type Grid = dict[Pos, str]
type Graph = defaultdict[Entity, list[Entity]]
type Edges = dict[tuple[Entity, Entity], int]  # edge weights
type State = tuple[Entity, str]  # (node,(collected_keys))


def init_data(data: str) -> tuple[Grid, EntityMap]:
    grid = {(y, x): c for y, row in enumerate(data.splitlines()) for x, c in enumerate(row)}
    entity_map = {c: pos for pos, c in grid.items() if c not in ".#"}
    return grid, entity_map


# create a graph from the grid
# gets rid of the corridors and saves their lenghts as weights
def create_graph(grid: Grid, entity_map: EntityMap) -> tuple[Graph, Edges]:
    DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))
    graph: Graph = defaultdict(list)
    edges: Edges = {}

    # flood fill/bfs for every entitiy
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
    return graph, edges


def part2_graphs(data: str, pos_player: Pos) -> list[tuple[Graph, Edges]]:
    pos_y, pos_x = pos_player
    arr = [[c for c in row] for row in data.splitlines()]
    for dy, dx in product((1, 0, -1), repeat=2):
        arr[pos_y+dy][pos_x+dx] = "#"
    for dy, dx in product((1, -1), repeat=2):
        arr[pos_y+dy][pos_x+dx] = "@"

    top, bottom = arr[:pos_y+1], arr[pos_y:]
    transposed = [[list(r) for r in zip(*half)] for half in (top, bottom)]
    # cursed
    quarters = [[list(c) for c in zip(*tr[:pos_x+1])] for tr in transposed] + \
        [[list(c) for c in zip(*tr[pos_x:])] for tr in transposed]
    strings = ["\n".join("".join(row) for row in quart) for quart in quarters]

    graphs_edges = [create_graph(*init_data(string)) for string in strings]

    return graphs_edges


def part1(data: str) -> tuple[int, int, Pos]:
    grid, entity_map = init_data(data)
    num_keys = sum(e.islower() for e in entity_map)
    pos_player = next(pos for e, pos in entity_map.items() if e == "@")
    graph, edges = create_graph(grid, entity_map)

    # state = (node,(collected_keys))
    # collected_keys must be sorted
    init = (0, 0, ("@", ""))  # (prio,steps,state)
    q: list[tuple[int, int, State]] = [init]
    heapify(q)
    seen: dict[State, int] = {}  # state: steps

    while q:
        prio, steps, state = heappop(q)
        node, keys = state

        if len(keys) == num_keys:
            return steps, num_keys, pos_player

        if state in seen and seen[state] < steps:
            continue

        for new_node in graph[node]:
            new_keys = None

            # key
            if new_node.islower():
                # add key to keyring if its a new one
                new_keys = keys if new_node in keys else ''.join(sorted(keys+new_node))
            # door
            elif new_node.isupper():
                # do we have a key?
                if new_node.lower() in keys:
                    new_keys = keys
            # start position
            else:
                new_keys = keys

            if new_keys is not None:
                new_steps = steps + edges[(node, new_node)]
                new_prio = new_steps + (num_keys-len(new_keys))
                new_state = (new_node, new_keys)
                if new_state in seen and seen[new_state] <= new_steps:
                    continue
                seen[new_state] = new_steps
                heappush(q, (new_prio, new_steps, new_state))
    else:
        raise ValueError("Could not find all keys :(")


def part2(data: str, pos_player: Pos, num_keys: int) -> int:
    graphs_edges = part2_graphs(data, pos_player)

    # state = (node,(collected_keys))
    # collected_keys must be sorted
    init = (0, 0, tuple(("@", "") for _ in range(4)))  # (prio,steps, 4 x state )
    q: list[tuple[int, int, tuple[State, ...]]] = [init]
    heapify(q)
    seen: dict[tuple[State, ...], int] = {}  # 4 x state: steps

    j = k = 0
    # state is now a tuple of 4
    while q:
        prio, steps, state = heappop(q)
        j += 1

        all_keys = "".join(keys for node, keys in state)
        if len(all_keys) == num_keys:
            print(f"i={j}, k={k}, seen={len(seen)}")
            return steps

        if state in seen and seen[state] < steps:
            continue
        k += 1

        for i, (node, keys) in enumerate(state):
            for new_node in graphs_edges[i][0][node]:
                new_keys = None

                # key
                if new_node.islower():
                    # add key to keyring if its a new one
                    new_keys = keys if new_node in keys else ''.join(sorted(keys+new_node))
                # door
                elif new_node.isupper():
                    # do we have a key?
                    # need to check globally
                    if new_node.lower() in all_keys:
                        new_keys = keys
                # start position
                else:
                    new_keys = keys

                if new_keys is not None:
                    new_steps = steps + graphs_edges[i][1][(node, new_node)]
                    new_prio = new_steps  #+ (num_keys-len(all_keys))*80
                    new_state = state[:i] + ((new_node, new_keys), ) + state[i+1:]
                    if new_state in seen and seen[new_state] <= new_steps:
                        continue
                    seen[new_state] = new_steps
                    heappush(q, (new_prio, new_steps, new_state))
    else:
        raise ValueError("Could not find all keys :(")


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()


steps, num_keys, pos_player = part1(data)
print("Part 1:", steps)
print("Part 2", part2(data, pos_player, num_keys))

e = timer()
print(f"time: {e-s}")
