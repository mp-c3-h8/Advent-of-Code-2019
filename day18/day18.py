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
    init = (0, 0, ("@", ""))  # (prio,steps,state)
    q: list[tuple[int, int, State]] = [init]
    heapify(q)
    seen: dict[State, int] = {}  # (node,tuple(collected_keys)): steps

    while q:
        prio, steps, state = heappop(q)
        node, keys = state

        if len(keys) == num_keys:
            return steps

        if state in seen and seen[state] <= steps:
            continue
        seen[state] = steps

        
        for new_node in graph[node]:
            add_steps = edges[(node, new_node)]
            new_steps = steps + add_steps
            if new_node.islower():  # key
                if new_node in keys:
                    heappush(q, (prio + add_steps, new_steps, (new_node, keys)))
                else:
                    new_keys = ''.join(sorted(keys+new_node))
                    #print(new_keys)
                    new_prio = new_steps + (num_keys-len(new_keys))
                    heappush(q, (new_prio, new_steps, (new_node, new_keys)))
            elif new_node.isupper():  # door
                if new_node.lower() in keys:  # we have a key!
                    heappush(q, (prio + add_steps, new_steps, (new_node, keys)))
            else:  # start position
                heappush(q, (prio + add_steps, new_steps, (new_node, keys)))
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

t = frozenset(["a","b"])
tt = {t:1}
a = frozenset(["b","a"])
print(a in tt)

e = timer()
print(f"time: {e-s}")
