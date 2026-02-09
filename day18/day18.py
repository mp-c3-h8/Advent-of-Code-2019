import os.path
import os
from timeit import default_timer as timer
from collections import defaultdict, deque
from heapq import heapify, heappop, heappush

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


def heuristic(entity_map: EntityMap, missing_keys: set[Entity]) -> int:
    return 0


def collect_all_keys(graph: Graph, edges: Edges, entity_map: EntityMap) -> int:
    num_keys = sum(e.islower() for e in entity_map)

    # state = (node,(collected_keys))
    # collected_keys must be sorted
    init = (0, 0, "@", "", ("@", ""))  # (prio,steps,last_node,last_key,state)
    q: list[tuple[int, int, Entity, Entity, State]] = [init]
    heapify(q)
    seen: dict[State, int] = {}  # state: steps

    i = 0
    k = 0
    while q:
        prio, steps, last_node, last_key, state = heappop(q)
        node, keys = state
        i += 1
        if len(keys) == num_keys:
            print(f"i={i}, k={k}, seen= {len(seen)}")
            return steps

        if state in seen and seen[state] < steps:
            continue

        k += 1
        for new_node in graph[node]:
            # dont backtrack unless we just picked up a new key
            if new_node == last_node and last_key != node:
                continue
            new_steps = steps + edges[(node, new_node)]
            if new_node.islower():  # key
                if new_node in keys:
                    new_prio = new_steps + (num_keys-len(keys))
                    if (new_node, keys) in seen and seen[(new_node, keys)] <= new_steps:
                        continue
                    seen[(new_node, keys)] = new_steps
                    heappush(q, (new_prio, new_steps, node, last_key, (new_node, keys)))
                else:
                    new_keys = ''.join(sorted(keys+new_node))
                    new_prio = new_steps + (num_keys-len(new_keys))
                    if (new_node, new_keys) in seen and seen[(new_node, new_keys)] <= new_steps:
                        continue
                    seen[(new_node, new_keys)] = new_steps
                    heappush(q, (new_prio, new_steps, node, new_node, (new_node, new_keys)))
            elif new_node.isupper():  # door
                if new_node.lower() in keys:  # we have a key!
                    new_prio = new_steps + (num_keys-len(keys))
                    if (new_node, keys) in seen and seen[(new_node, keys)] <= new_steps:
                        continue
                    seen[(new_node, keys)] = new_steps
                    heappush(q, (new_prio, new_steps, node, last_key, (new_node, keys)))
            else:  # start position
                new_prio = new_steps + (num_keys-len(keys))
                if (new_node, keys) in seen and seen[(new_node, keys)] <= new_steps:
                    continue
                seen[(new_node, keys)] = new_steps
                heappush(q, (new_prio, new_steps, node, last_key, (new_node, keys)))
    print(seen)

    return 0


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

grid, entity_map = init_data(data)
graph, edges = create_graph(grid, entity_map)
steps = collect_all_keys(graph, edges, entity_map)
print("Part 1:", steps)


e = timer()
print(f"time: {e-s}")
