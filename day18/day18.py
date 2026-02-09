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
type State = tuple[Entity, frozenset[Entity]]  # (node,(collected_keys))


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


def part2_graphs(data: str, pos_player: Pos):
    pos_y, pos_x = pos_player
    arr = [[c for c in row] for row in data.splitlines()]
    for dy, dx in product((1, 0, -1), repeat=2):
        arr[pos_y+dy][pos_x+dx] = "#"
    for (dy, dx),c in zip(product((1, -1), repeat=2),["@","%","$","§"]):
        arr[pos_y+dy][pos_x+dx] = c
        
    tt = "\n".join("".join(row) for row in arr)
    return create_graph(*init_data(tt))

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
    init = (0, 0, ("@", frozenset()))  # (prio,steps,state)
    q: list[tuple[int, int, State]] = [init]
    heapify(q)
    seen: dict[State, int] = {}  # state: steps
    search_keys_memo: dict[State, list[tuple[Entity, int]]] = {}

    j = k = 0
    while q:
        prio, steps, state = heappop(q)
        node, keys = state
        j += 1
        if len(keys) == num_keys:
            #print(f"i={j}, k={k}, seen={len(seen)}, memo={len(search_keys_memo)}")
            return steps, num_keys, pos_player

        if state in seen and seen[state] < steps:
            continue
        k += 1

        if state in search_keys_memo:
            print("YES")
            next_nodes = search_keys_memo[state]
        else:
            next_nodes = search_keys(graph, edges, node, keys)
            search_keys_memo[state] = next_nodes

        # new_node is always a key
        for new_node, add_steps in next_nodes:
            # print(state,steps,new_node)
            new_keys = keys | {new_node}
            new_steps = steps + add_steps
            new_prio = new_steps + (num_keys-len(new_keys))
            new_state = (new_node, new_keys)
            if new_state in seen and seen[new_state] <= new_steps:
                continue
            seen[new_state] = new_steps
            heappush(q, (new_prio, new_steps, new_state))
    else:
        raise ValueError("Could not find all keys :(")


def part2(data: str, pos_player: Pos, num_keys: int) -> int:
    graph,edges = part2_graphs(data, pos_player)

    # state = (node,(collected_keys))
    # collected_keys must be sorted
    init = (0, 0, ("@","%","$","§"), frozenset())  # (prio,steps, 4 x state )
    q: list[tuple[int, int, tuple[str, ...], frozenset[str]]] = [init]
    heapify(q)
    seen: dict[tuple[tuple[str, ...], frozenset[str]], int] = {}  # 4 x state: steps

    j = k = 0
    # state is now a tuple of 4
    while q:
        prio, steps, nodes, keys = heappop(q)
        j += 1
        # print(state)

        if len(keys) == num_keys:
            #print(f"i={j}, k={k}, seen={len(seen)}")
            return steps

        if (nodes, keys) in seen and seen[(nodes, keys)] < steps:
            continue
        k += 1

        for i, node in enumerate(nodes):
            # new_node is always a new key
            for new_node, add_steps in search_keys(graph, edges, node, keys):
                new_keys = keys | {new_node}
                new_steps = steps + add_steps
                new_prio = new_steps + (num_keys-len(new_keys))
                new_nodes = nodes[:i] + (new_node,) + nodes[i+1:]
                if (new_nodes, new_keys) in seen and seen[(new_nodes, new_keys)] <= new_steps:
                    continue
                seen[(new_nodes, new_keys)] = new_steps
                heappush(q, (new_prio, new_steps, new_nodes, new_keys))
    else:
        raise ValueError("Could not find all keys :(")


def search_keys(graph: Graph, edges: Edges, start: Entity, keys: frozenset[Entity]) -> list[tuple[Entity, int]]:
    init = (0, start)  # (steps=prio,node)
    q: list[tuple[int, Entity]] = [init]
    heapify(q)
    seen: dict[Entity, int] = {}  # node: steps
    new_keys = set()
    done: set[str] = set()

    while q:
        steps, node = heappop(q)

        if node in done:
            continue
        done.add(node)

        if node.islower() and node not in keys:
            new_keys.add(node)
            continue

        if node in seen and seen[node] < steps:
            continue
        # seen[node] = steps

        for new_node in graph[node]:
            # cant open the door
            if new_node.isupper() and new_node.lower() not in keys:
                continue

            new_steps = steps + edges[(node, new_node)]

            if new_node in seen and seen[new_node] < new_steps:
                continue

            seen[new_node] = new_steps
            heappush(q, (new_steps, new_node))

    return [(key, seen[key]) for key in new_keys]


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
