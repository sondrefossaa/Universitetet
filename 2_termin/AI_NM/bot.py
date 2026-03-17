import asyncio
import json
import sys
from collections import Counter
from dataclasses import dataclass
from itertools import combinations, permutations

import websockets


WS_URL = sys.argv[1]
INF = 10**9
BOT_PLANS: dict[int, list[str]] = {}


@dataclass
class PathCache:
    dist: dict
    step: dict


def make_path_cache():
    return PathCache(dist={}, step={})


def adjacent_cells(x, y):
    return ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))


def in_bounds(grid, x, y):
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])


def is_walkable(grid, x, y):
    return in_bounds(grid, x, y) and grid[y][x] in {".", "D", " "}


def extract_grid(state):
    raw_grid = state.get("grid")
    if (
        isinstance(raw_grid, list)
        and raw_grid
        and all(isinstance(r, str) for r in raw_grid)
    ):
        return [str(r) for r in raw_grid]

    if isinstance(raw_grid, dict):
        width = raw_grid.get("width")
        height = raw_grid.get("height")
        walls = raw_grid.get("walls", [])
        if (
            isinstance(width, int)
            and isinstance(height, int)
            and width > 0
            and height > 0
        ):
            blocked = set()
            if isinstance(walls, list):
                for wall in walls:
                    if isinstance(wall, (list, tuple)) and len(wall) >= 2:
                        blocked.add((wall[0], wall[1]))
                    elif isinstance(wall, dict) and "x" in wall and "y" in wall:
                        blocked.add((wall["x"], wall["y"]))

            shelves = state.get("shelves", [])
            if isinstance(shelves, list):
                for shelf in shelves:
                    if isinstance(shelf, dict):
                        pos = shelf.get("position", shelf)
                        if isinstance(pos, (list, tuple)) and len(pos) >= 2:
                            blocked.add((pos[0], pos[1]))

            items = state.get("items", [])
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict):
                        pos = item.get("position", item)
                        if isinstance(pos, (list, tuple)) and len(pos) >= 2:
                            blocked.add((pos[0], pos[1]))

            grid = []
            for y in range(height):
                row = []
                for x in range(width):
                    row.append("#" if (x, y) in blocked else ".")
                grid.append("".join(row))
            return grid
    return None


def extract_dropoffs(state, grid):
    out = []
    zones = state.get("drop_off_zones") or state.get("drop_zones") or []
    if isinstance(zones, list):
        for z in zones:
            if isinstance(z, (list, tuple)) and len(z) >= 2:
                out.append((z[0], z[1]))

    single = state.get("drop_off")
    if isinstance(single, (list, tuple)) and len(single) >= 2:
        out.append((single[0], single[1]))

    if out:
        return list(dict.fromkeys(out))

    if grid is not None:
        for y, row in enumerate(grid):
            for x, c in enumerate(row):
                if c == "D":
                    out.append((x, y))
    return out


def extract_order_needs(state):
    orders = state.get("orders", [])
    active = next((o for o in orders if o.get("status") == "active"), None)
    preview = next((o for o in orders if o.get("status") == "preview"), None)
    if active is None and orders:
        active = orders[0]

    def needs_for(order):
        if not order:
            return Counter()
        need = Counter(order.get("items_required", []))
        for delivered in order.get("items_delivered", []):
            need[delivered] -= 1
        return Counter({k: v for k, v in need.items() if v > 0})

    return needs_for(active), needs_for(preview)


def astar_distance(grid, start, targets, blocked):
    if start in targets:
        return 0

    tx = [t[0] for t in targets]
    ty = [t[1] for t in targets]

    def h(x, y):
        best = INF
        for i in range(len(tx)):
            d = abs(tx[i] - x) + abs(ty[i] - y)
            if d < best:
                best = d
        return best

    open_heap = [(h(start[0], start[1]), 0, start)]
    best_g = {start: 0}

    while open_heap:
        open_heap.sort(key=lambda t: t[0])
        _, g, cur = open_heap.pop(0)
        if cur in targets:
            return g
        if g != best_g.get(cur):
            continue

        for nx, ny in adjacent_cells(cur[0], cur[1]):
            nxt = (nx, ny)
            if nxt != start and nxt in blocked:
                continue
            if not is_walkable(grid, nx, ny):
                continue
            ng = g + 1
            if ng < best_g.get(nxt, INF):
                best_g[nxt] = ng
                open_heap.append((ng + h(nx, ny), ng, nxt))

    return None


def astar_next_step(grid, start, targets, blocked):
    if start in targets:
        return start

    tx = [t[0] for t in targets]
    ty = [t[1] for t in targets]

    def h(x, y):
        best = INF
        for i in range(len(tx)):
            d = abs(tx[i] - x) + abs(ty[i] - y)
            if d < best:
                best = d
        return best

    open_heap = [(h(start[0], start[1]), 0, start)]
    best_g = {start: 0}
    parent = {start: None}

    goal = None
    while open_heap:
        open_heap.sort(key=lambda t: t[0])
        _, g, cur = open_heap.pop(0)
        if cur in targets:
            goal = cur
            break
        if g != best_g.get(cur):
            continue
        for nx, ny in adjacent_cells(cur[0], cur[1]):
            nxt = (nx, ny)
            if nxt != start and nxt in blocked:
                continue
            if not is_walkable(grid, nx, ny):
                continue
            ng = g + 1
            if ng < best_g.get(nxt, INF):
                best_g[nxt] = ng
                parent[nxt] = cur
                open_heap.append((ng + h(nx, ny), ng, nxt))

    if goal is None:
        return None

    cur = goal
    prev = parent[cur]
    while prev is not None and prev != start:
        cur = prev
        prev = parent[cur]
    return cur


def cached_dist(cache, grid, start, targets, blocked):
    key = (start, frozenset(targets), frozenset(blocked))
    if key not in cache.dist:
        cache.dist[key] = astar_distance(grid, start, targets, blocked)
    return cache.dist[key]


def cached_step(cache, grid, start, targets, blocked):
    key = (start, frozenset(targets), frozenset(blocked))
    if key not in cache.step:
        cache.step[key] = astar_next_step(grid, start, targets, blocked)
    return cache.step[key]


def adjacent_walkable_cells(grid, x, y):
    out = set()
    for nx, ny in adjacent_cells(x, y):
        if is_walkable(grid, nx, ny):
            out.add((nx, ny))
    return out


def route_cost_and_state(
    cache,
    grid,
    start,
    sequence,
    dropoff_set,
    blocked,
    active_need,
    preview_need,
    inv,
):
    pos_costs = {start: (0, Counter(inv), Counter(active_need), 0)}
    # state tuple: (cost, inv_counter, active_remaining, preview_carried)

    for item in sequence:
        item_type = item.get("type")
        if item_type is None:
            continue
        cells = adjacent_walkable_cells(grid, item["position"][0], item["position"][1])
        if not cells:
            return None

        next_states = {}
        for src_pos, (
            src_cost,
            src_inv,
            src_active,
            src_preview_carried,
        ) in pos_costs.items():
            for dst in cells:
                d = cached_dist(cache, grid, src_pos, {dst}, blocked)
                if d is None:
                    continue
                cost = src_cost + d + 1
                inv2 = Counter(src_inv)
                active2 = Counter(src_active)
                preview2 = src_preview_carried
                inv2[item_type] += 1
                if active2[item_type] > 0:
                    active2[item_type] -= 1
                elif preview_need[item_type] > 0:
                    preview2 += 1
                key = dst
                prev = next_states.get(key)
                cand = (cost, inv2, active2, preview2)
                if prev is None or cost < prev[0]:
                    next_states[key] = cand
        if not next_states:
            return None
        pos_costs = next_states

    best = None
    for src_pos, (
        src_cost,
        src_inv,
        src_active,
        src_preview_carried,
    ) in pos_costs.items():
        d_drop = cached_dist(cache, grid, src_pos, dropoff_set, blocked)
        if d_drop is None:
            continue
        total = src_cost + d_drop + 1
        delivered_now = 0
        inv_after = Counter(src_inv)
        active_after = Counter(src_active)
        for t in list(inv_after):
            use = min(inv_after[t], active_need[t])
            if use > 0:
                delivered_now += use
                inv_after[t] -= use
                active_after[t] = max(0, active_after[t] - use)
        active_complete = sum(active_after.values()) == 0
        auto_preview = 0
        if active_complete:
            for t in list(inv_after):
                auto_preview += min(inv_after[t], preview_need[t])

        key = (
            0 if active_complete else 1,
            -auto_preview,
            total,
            -delivered_now,
            -src_preview_carried,
        )
        cand = (key, total)
        if best is None or cand[0] < best[0]:
            best = cand
    return best


def choose_sequence(
    cache, grid, pos, items, dropoff_set, blocked, local_need, preview_need, inv
):
    free_slots = 3 - len(inv)
    if free_slots <= 0:
        return None

    useful = [
        it
        for it in items
        if it.get("type") is not None
        and (local_need[it["type"]] > 0 or preview_need[it["type"]] > 0)
    ]
    if not useful:
        return None

    ranked = []
    for item in useful:
        cells = adjacent_walkable_cells(grid, item["position"][0], item["position"][1])
        if not cells:
            continue
        d = cached_dist(cache, grid, pos, cells, blocked)
        if d is None:
            continue
        ranked.append((d, item))

    if not ranked:
        return None

    ranked.sort(key=lambda t: t[0])
    pool = [it for _, it in ranked[:7]]

    k = min(free_slots, len(pool))
    best = None
    best_seq = None
    for combo in combinations(pool, k):
        for perm in permutations(combo):
            seq = list(perm)
            res = route_cost_and_state(
                cache,
                grid,
                pos,
                seq,
                dropoff_set,
                blocked,
                local_need,
                preview_need,
                inv,
            )
            if res is None:
                continue
            key, _ = res
            if best is None or key < best:
                best = key
                best_seq = seq
    return best_seq


def move_action(bot_id, cur, nxt):
    x, y = cur
    nx, ny = nxt
    if nx == x + 1 and ny == y:
        return {"bot": bot_id, "action": "move_right"}
    if nx == x - 1 and ny == y:
        return {"bot": bot_id, "action": "move_left"}
    if nx == x and ny == y - 1:
        return {"bot": bot_id, "action": "move_up"}
    if nx == x and ny == y + 1:
        return {"bot": bot_id, "action": "move_down"}
    return {"bot": bot_id, "action": "wait"}


def decide(bot, state, grid, dropoff_set, active_need, preview_need, occupied, cache):
    bot_id = bot["id"]
    x, y = bot["position"]
    pos = (x, y)
    inv = list(bot.get("inventory", []))

    inv_counter = Counter(inv)
    inv_active = sum(inv_counter[t] for t in inv_counter if active_need[t] > 0)

    if inv_active > 0 and pos in dropoff_set:
        BOT_PLANS[bot_id] = []
        return {"bot": bot_id, "action": "drop_off"}

    items = [
        it
        for it in state.get("items", [])
        if isinstance(it, dict) and it.get("id") is not None
    ]
    item_by_id = {str(it["id"]): it for it in items}

    local_need = Counter(active_need)
    for t in inv:
        if local_need[t] > 0:
            local_need[t] -= 1

    blocked = occupied - {pos}
    plan = BOT_PLANS.get(bot_id, [])

    if len(inv) < 3 and plan:
        head = item_by_id.get(str(plan[0]))
        if head is not None:
            ix, iy = head["position"]
            if abs(ix - x) + abs(iy - y) == 1:
                plan.pop(0)
                return {"bot": bot_id, "action": "pick_up", "item_id": head["id"]}

    remaining = sum(local_need.values())
    if inv and (len(inv) >= 3 or remaining <= 0 or inv_active >= remaining):
        step = cached_step(cache, grid, pos, dropoff_set, blocked)
        BOT_PLANS[bot_id] = []
        if step is not None and step != pos:
            return move_action(bot_id, pos, step)

    if not plan and len(inv) < 3 and dropoff_set:
        seq = choose_sequence(
            cache,
            grid,
            pos,
            items,
            dropoff_set,
            blocked,
            local_need,
            preview_need,
            inv,
        )
        if seq:
            BOT_PLANS[bot_id] = [str(it["id"]) for it in seq]
            plan = BOT_PLANS[bot_id]

    while plan and len(inv) < 3:
        head = item_by_id.get(str(plan[0]))
        if head is None:
            plan.pop(0)
            continue
        ix, iy = head["position"]
        if abs(ix - x) + abs(iy - y) == 1:
            plan.pop(0)
            return {"bot": bot_id, "action": "pick_up", "item_id": head["id"]}
        cells = adjacent_walkable_cells(grid, ix, iy)
        if not cells:
            plan.pop(0)
            continue
        step = cached_step(cache, grid, pos, cells, blocked)
        if step is None:
            plan.pop(0)
            continue
        return move_action(bot_id, pos, step)

    if inv_active > 0 and dropoff_set:
        step = cached_step(cache, grid, pos, dropoff_set, blocked)
        if step is not None and step != pos:
            return move_action(bot_id, pos, step)

    return {"bot": bot_id, "action": "wait"}


def decide_all(state):
    bots = sorted(state.get("bots", []), key=lambda b: b.get("id", 0))
    if not bots:
        return []

    grid = extract_grid(state)
    if grid is None:
        return [{"bot": bot["id"], "action": "wait"} for bot in bots]

    dropoffs = extract_dropoffs(state, grid)
    dropoff_set = set(dropoffs)
    if not dropoff_set:
        return [{"bot": bot["id"], "action": "wait"} for bot in bots]

    active_need, preview_need = extract_order_needs(state)
    occupied = {tuple(bot["position"]) for bot in bots}
    cache = make_path_cache()

    actions = []
    for bot in bots:
        actions.append(
            decide(
                bot,
                state,
                grid,
                dropoff_set,
                active_need,
                preview_need,
                occupied,
                cache,
            )
        )
    return actions


async def play():
    async with websockets.connect(WS_URL) as ws:
        async for raw in ws:
            msg = json.loads(raw)
            msg_type = msg.get("type")

            if msg_type == "game_over":
                print(
                    f"Game over! Score: {msg.get('score')}, Rounds: {msg.get('rounds_used')}"
                )
                break

            if msg_type in {"game_state", "state", "tick", "round"} or (
                msg_type is None and "bots" in msg
            ):
                actions = decide_all(msg)
                await ws.send(json.dumps({"actions": actions}))


asyncio.run(play())
