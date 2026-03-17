#!/usr/bin/env python3
import argparse
import asyncio
import base64
from collections import Counter, deque
from dataclasses import dataclass
from itertools import combinations, permutations
import json
import os
import time
from urllib.parse import parse_qs, urlparse
from typing import Any

import websockets


DEFAULT_WS_URL = (
    "wss://game.ainm.no/ws?token="
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJqdGkiOiI1MzZlOTczNy00ZTVkLTRlMDUtYmUzYy1iNjNjNTVlZDNlZmEiLCJ0ZWFtX2lkIjoiNmZiMGQ3NmMtYTJmYy00MDlkLTkxMzAtMTA4N2YyZjQ1YmE0IiwibWFwX2lkIjoiYzg5ZGEyZWMtM2NhNy00MGM5LWEzYjEtODAzNmZjYTNkMGI3IiwibWFwX3NlZWQiOjcwMDEsImRpZmZpY3VsdHkiOiJlYXN5IiwiZXhwIjoxNzczNzM0OTUxfQ."
    "P7VeyeF87Uhx96ZTalzoa5MV3uf-oGefZLQ-uSEyKwc"
)


Action = dict[str, Any]


@dataclass
class Bot:
    bot_id: int
    x: int
    y: int
    inventory: list[Any]


@dataclass
class ShelfItem:
    item_id: Any
    item_key: tuple[str, str] | None
    x: int
    y: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Easy difficulty Grocery Bot websocket client"
    )
    parser.add_argument(
        "--url",
        default=os.getenv("GROCERY_WS_URL", DEFAULT_WS_URL),
        help="WebSocket URL",
    )
    parser.add_argument(
        "--team",
        default=os.getenv("GROCERY_TEAM", "Erling Braut-Force Haaland"),
        help="Erling Braut-Force Haaland",
    )
    parser.add_argument(
        "--token", default=os.getenv("GROCERY_TOKEN"), help="Auth token if required"
    )
    return parser.parse_args()


def as_pos(value: Any) -> tuple[int, int] | None:
    if isinstance(value, dict):
        x = value.get("x", value.get("col"))
        y = value.get("y", value.get("row"))
        if isinstance(x, int) and isinstance(y, int):
            return x, y
    if isinstance(value, (list, tuple)) and len(value) >= 2:
        if isinstance(value[0], int) and isinstance(value[1], int):
            return value[0], value[1]
    return None


def normalize_key(item: Any) -> tuple[str, str] | None:
    if isinstance(item, dict):
        if item.get("item_type"):
            return "item_type", str(item["item_type"])
        if item.get("type"):
            return "type", str(item["type"])
        if item.get("name"):
            return "name", str(item["name"])
        if item.get("item_id") is not None:
            return "item_id", str(item["item_id"])
        if item.get("id") is not None:
            return "id", str(item["id"])
    if isinstance(item, str):
        return "name", item
    if isinstance(item, int):
        return "item_id", str(item)
    return None


def item_quantity(item: Any) -> int:
    if isinstance(item, dict):
        for key in ("qty", "quantity", "count", "amount"):
            value = item.get(key)
            if isinstance(value, int) and value > 0:
                return value
    return 1


def extract_order_counter(order: Any) -> Counter[tuple[str, str]]:
    needs: Counter[tuple[str, str]] = Counter()
    if not order:
        return needs

    def add_items(raw_items: Any, sign: int = 1) -> None:
        if isinstance(raw_items, dict):
            for key, value in raw_items.items():
                if isinstance(value, int) and value > 0:
                    needs[("name", str(key))] += sign * value
            return
        if isinstance(raw_items, list):
            for item in raw_items:
                item_key = normalize_key(item)
                if item_key is not None:
                    needs[item_key] += sign * item_quantity(item)

    if isinstance(order, dict):
        required = (
            order.get("items_required")
            or order.get("items")
            or order.get("requirements")
            or order.get("needed")
        )
        delivered = order.get("items_delivered")
        add_items(required, sign=1)
        add_items(delivered, sign=-1)
        return Counter({key: value for key, value in needs.items() if value > 0})

    if isinstance(order, list):
        add_items(order, sign=1)
    return needs


def extract_orders(
    state: dict[str, Any],
) -> tuple[Counter[tuple[str, str]], Counter[tuple[str, str]]]:
    active = (
        state.get("active_order")
        or state.get("current_order")
        or state.get("order")
        or state.get("activeOrder")
    )
    preview = (
        state.get("preview_order")
        or state.get("next_order")
        or state.get("previewOrder")
    )

    orders = state.get("orders")
    if active is None and isinstance(orders, dict):
        active = orders.get("active")
        preview = preview or orders.get("preview")

    if isinstance(orders, list) and orders:
        active_by_status = None
        preview_by_status = None
        for order in orders:
            if not isinstance(order, dict):
                continue
            status = order.get("status")
            if status == "active":
                active_by_status = order
            elif status == "preview":
                preview_by_status = order

        if active is None:
            active = active_by_status or orders[0]
        if preview is None:
            preview = preview_by_status
            if preview is None and len(orders) > 1:
                preview = orders[1]

    return extract_order_counter(active), extract_order_counter(preview)


def extract_grid(state: dict[str, Any]) -> list[str] | None:
    candidates = [
        state.get("grid"),
        state.get("map"),
        state.get("board"),
        state.get("layout"),
        state.get("store"),
    ]
    for candidate in candidates:
        if (
            isinstance(candidate, list)
            and candidate
            and all(isinstance(row, str) for row in candidate)
        ):
            return [str(row) for row in candidate]
        if isinstance(candidate, dict):
            width = candidate.get("width")
            height = candidate.get("height")
            walls = candidate.get("walls")
            if (
                isinstance(width, int)
                and isinstance(height, int)
                and width > 0
                and height > 0
            ):
                wall_set: set[tuple[int, int]] = set()
                if isinstance(walls, list):
                    for wall in walls:
                        pos = as_pos(wall)
                        if pos is not None:
                            wall_set.add(pos)

                shelves = state.get("shelves")
                if isinstance(shelves, list):
                    for shelf in shelves:
                        if isinstance(shelf, dict):
                            pos = as_pos(shelf) or as_pos(shelf.get("position"))
                            if pos is not None:
                                wall_set.add(pos)

                floor_items = state.get("items")
                if isinstance(floor_items, list):
                    for item in floor_items:
                        if isinstance(item, dict):
                            pos = as_pos(item) or as_pos(item.get("position"))
                            if pos is not None:
                                wall_set.add(pos)

                rows: list[str] = []
                for y in range(height):
                    row_chars: list[str] = []
                    for x in range(width):
                        row_chars.append("#" if (x, y) in wall_set else ".")
                    rows.append("".join(row_chars))
                return rows

            tiles = (
                candidate.get("grid") or candidate.get("tiles") or candidate.get("rows")
            )
            if (
                isinstance(tiles, list)
                and tiles
                and all(isinstance(row, str) for row in tiles)
            ):
                return [str(row) for row in tiles]
    return None


def extract_dropoffs(
    state: dict[str, Any], grid: list[str] | None
) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for key in (
        "dropoffs",
        "drop_offs",
        "drop_zones",
        "drop_off_zones",
        "dropZones",
        "drop_points",
    ):
        value = state.get(key)
        if isinstance(value, list):
            for entry in value:
                pos = as_pos(entry)
                if pos is not None:
                    out.append(pos)
    for key in ("dropoff", "drop_off", "drop_zone", "dropZone"):
        pos = as_pos(state.get(key))
        if pos is not None:
            out.append(pos)
    if out:
        return out
    if grid is not None:
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell == "D":
                    out.append((x, y))
    return out


def extract_bots(state: dict[str, Any]) -> list[Bot]:
    raw_bots = state.get("bots")
    if raw_bots is None and isinstance(state.get("players"), list):
        raw_bots = state.get("players")
    if not isinstance(raw_bots, list):
        return []

    bots: list[Bot] = []
    for i, raw in enumerate(raw_bots):
        if not isinstance(raw, dict):
            continue
        pos = as_pos(raw)
        if pos is None:
            pos = as_pos(raw.get("position"))
        if pos is None:
            continue
        raw_inventory = raw.get("inventory")
        inventory = raw_inventory if isinstance(raw_inventory, list) else []
        bot_id_raw = raw.get("id", raw.get("bot_id", i))
        bot_id = (
            int(bot_id_raw)
            if isinstance(bot_id_raw, (int, str)) and str(bot_id_raw).isdigit()
            else i
        )
        bots.append(Bot(bot_id=bot_id, x=pos[0], y=pos[1], inventory=inventory))
    bots.sort(key=lambda b: b.bot_id)
    return bots


def extract_shelf_items(state: dict[str, Any]) -> list[ShelfItem]:
    items: list[ShelfItem] = []

    shelves = state.get("shelves")
    if isinstance(shelves, list):
        for shelf in shelves:
            if not isinstance(shelf, dict):
                continue
            shelf_pos = as_pos(shelf) or as_pos(shelf.get("position"))
            if shelf_pos is None:
                continue
            shelf_items = shelf.get("items")
            if not isinstance(shelf_items, list):
                continue
            for item in shelf_items:
                if not isinstance(item, dict):
                    continue
                item_id = item.get("item_id", item.get("id"))
                items.append(
                    ShelfItem(
                        item_id=item_id,
                        item_key=normalize_key(item),
                        x=shelf_pos[0],
                        y=shelf_pos[1],
                    )
                )

    floor_items = state.get("items")
    if isinstance(floor_items, list):
        for item in floor_items:
            if not isinstance(item, dict):
                continue
            pos = as_pos(item) or as_pos(item.get("position"))
            if pos is None:
                continue
            item_id = item.get("item_id", item.get("id"))
            items.append(
                ShelfItem(
                    item_id=item_id, item_key=normalize_key(item), x=pos[0], y=pos[1]
                )
            )

    dedup: dict[Any, ShelfItem] = {}
    for item in items:
        if item.item_id is None or item.item_key is None:
            continue
        dedup[item.item_id] = item
    return list(dedup.values())


def in_bounds(grid: list[str], x: int, y: int) -> bool:
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])


def is_walkable(grid: list[str], x: int, y: int) -> bool:
    if not in_bounds(grid, x, y):
        return False
    return grid[y][x] in {".", "D", " "}


def adjacent_cells(x: int, y: int) -> list[tuple[int, int]]:
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]


def bfs_next_step(
    grid: list[str],
    start: tuple[int, int],
    targets: set[tuple[int, int]],
    blocked: set[tuple[int, int]],
) -> tuple[int, int] | None:
    if start in targets:
        return start

    queue: deque[tuple[int, int]] = deque([start])
    parent: dict[tuple[int, int], tuple[int, int] | None] = {start: None}
    found: tuple[int, int] | None = None

    while queue:
        current = queue.popleft()
        if current in targets:
            found = current
            break
        for nx, ny in adjacent_cells(current[0], current[1]):
            nxt = (nx, ny)
            if nxt in parent:
                continue
            if nxt != start and nxt in blocked:
                continue
            if not is_walkable(grid, nx, ny):
                continue
            parent[nxt] = current
            queue.append(nxt)

    if found is None:
        return None

    cur = found
    prev = parent[cur]
    while prev is not None and prev != start:
        cur = prev
        prev = parent[cur]
    return cur


def bfs_distance(
    grid: list[str],
    start: tuple[int, int],
    targets: set[tuple[int, int]],
    blocked: set[tuple[int, int]],
) -> int | None:
    if start in targets:
        return 0

    queue: deque[tuple[tuple[int, int], int]] = deque([(start, 0)])
    seen: set[tuple[int, int]] = {start}

    while queue:
        current, dist = queue.popleft()
        for nx, ny in adjacent_cells(current[0], current[1]):
            nxt = (nx, ny)
            if nxt in seen:
                continue
            if nxt != start and nxt in blocked:
                continue
            if not is_walkable(grid, nx, ny):
                continue
            if nxt in targets:
                return dist + 1
            seen.add(nxt)
            queue.append((nxt, dist + 1))
    return None


def adjacent_walkable_cells(grid: list[str], x: int, y: int) -> set[tuple[int, int]]:
    out: set[tuple[int, int]] = set()
    for adj in adjacent_cells(x, y):
        if is_walkable(grid, adj[0], adj[1]):
            out.add(adj)
    return out


def path_len_between_points(
    grid: list[str],
    start: tuple[int, int],
    goal: tuple[int, int],
    blocked: set[tuple[int, int]],
) -> int | None:
    return bfs_distance(grid, start, {goal}, blocked)


def route_cost_with_pickups(
    grid: list[str],
    start: tuple[int, int],
    sequence: list[ShelfItem],
    dropoff_set: set[tuple[int, int]],
    blocked: set[tuple[int, int]],
) -> int | None:
    position_costs: dict[tuple[int, int], int] = {start: 0}

    for item in sequence:
        target_cells = adjacent_walkable_cells(grid, item.x, item.y)
        if not target_cells:
            return None

        next_costs: dict[tuple[int, int], int] = {}
        for src_pos, src_cost in position_costs.items():
            for dst_pos in target_cells:
                dist = path_len_between_points(grid, src_pos, dst_pos, blocked)
                if dist is None:
                    continue
                candidate_cost = src_cost + dist + 1
                prev = next_costs.get(dst_pos)
                if prev is None or candidate_cost < prev:
                    next_costs[dst_pos] = candidate_cost

        if not next_costs:
            return None
        position_costs = next_costs

    best_total: int | None = None
    for src_pos, src_cost in position_costs.items():
        dist_to_drop = bfs_distance(grid, src_pos, dropoff_set, blocked)
        if dist_to_drop is None:
            continue
        candidate_total = src_cost + dist_to_drop + 1
        if best_total is None or candidate_total < best_total:
            best_total = candidate_total
    return best_total


def choose_best_batch(
    grid: list[str],
    bot_pos: tuple[int, int],
    candidates: list[ShelfItem],
    dropoff_set: set[tuple[int, int]],
    blocked: set[tuple[int, int]],
    max_pickups: int,
) -> list[ShelfItem] | None:
    if not candidates or max_pickups <= 0:
        return None

    ranked: list[tuple[int, ShelfItem]] = []
    for item in candidates:
        target_cells = adjacent_walkable_cells(grid, item.x, item.y)
        if not target_cells:
            continue
        dist = bfs_distance(grid, bot_pos, target_cells, blocked)
        if dist is None:
            continue
        ranked.append((dist, item))

    if not ranked:
        return None

    ranked.sort(key=lambda pair: pair[0])
    pool = [item for _, item in ranked[:8]]

    best_seq: list[ShelfItem] | None = None
    best_key: tuple[int, int] | None = None

    for k in range(min(max_pickups, len(pool)), 0, -1):
        for combo in combinations(pool, k):
            for perm in permutations(combo):
                seq = list(perm)
                cost = route_cost_with_pickups(
                    grid,
                    bot_pos,
                    seq,
                    dropoff_set,
                    blocked,
                )
                if cost is None:
                    continue
                candidate_key = (-k, cost)
                if best_key is None or candidate_key < best_key:
                    best_key = candidate_key
                    best_seq = seq
        if best_seq is not None:
            break

    return best_seq


def move_action(bot_id: int, cur: tuple[int, int], nxt: tuple[int, int]) -> Action:
    x, y = cur
    nx, ny = nxt
    if nx == x + 1 and ny == y:
        return {"bot_id": bot_id, "type": "move_right"}
    if nx == x - 1 and ny == y:
        return {"bot_id": bot_id, "type": "move_left"}
    if nx == x and ny == y - 1:
        return {"bot_id": bot_id, "type": "move_up"}
    if nx == x and ny == y + 1:
        return {"bot_id": bot_id, "type": "move_down"}
    return {"bot_id": bot_id, "type": "wait"}


def build_actions(state: dict[str, Any]) -> dict[str, Any]:
    grid = extract_grid(state)
    bots = extract_bots(state)
    if not bots:
        return {"actions": []}

    if grid is None:
        return {"actions": [{"bot_id": bot.bot_id, "type": "wait"} for bot in bots]}

    dropoffs = extract_dropoffs(state, grid)
    shelf_items = extract_shelf_items(state)
    active_need, preview_need = extract_orders(state)

    carried = Counter()
    for bot in bots:
        for item in bot.inventory:
            key = normalize_key(item)
            if key is not None:
                carried[key] += 1

    active_remaining = active_need - carried
    preview_remaining = preview_need - carried

    blocked_positions = {(bot.x, bot.y) for bot in bots}
    dropoff_set = set(dropoffs)
    actions: list[Action] = []

    for bot in bots:
        bot_pos = (bot.x, bot.y)
        blocked_without_self = blocked_positions - {bot_pos}

        inv_keys = Counter()
        for item in bot.inventory:
            key = normalize_key(item)
            if key is not None:
                inv_keys[key] += 1

        has_active_item = any(
            inv_keys[key] > 0 and active_need[key] > 0 for key in inv_keys
        )
        active_in_inventory = sum(
            inv_keys[key] for key in inv_keys if active_need[key] > 0
        )
        active_remaining_count = sum(active_remaining.values())

        active_candidates: list[ShelfItem] = []
        for item in shelf_items:
            if item.item_key is None:
                continue
            if active_remaining[item.item_key] <= 0:
                continue
            active_candidates.append(item)

        # If inventory can finish current order, rush dropoff.
        if has_active_item and dropoffs:
            if bot_pos in dropoff_set:
                actions.append({"bot_id": bot.bot_id, "type": "drop_off"})
                continue
            if active_remaining_count <= active_in_inventory:
                next_step = bfs_next_step(
                    grid, bot_pos, dropoff_set, blocked_without_self
                )
                if next_step is not None and next_step != bot_pos:
                    actions.append(move_action(bot.bot_id, bot_pos, next_step))
                    continue

        if len(bot.inventory) < 3:
            prioritized_adjacent: list[tuple[int, ShelfItem]] = []
            for item in shelf_items:
                if item.item_key is None:
                    continue
                if abs(item.x - bot.x) + abs(item.y - bot.y) != 1:
                    continue
                if active_remaining[item.item_key] > 0:
                    prioritized_adjacent.append((0, item))
                elif preview_remaining[item.item_key] > 0:
                    prioritized_adjacent.append((1, item))

            if prioritized_adjacent:
                prioritized_adjacent.sort(key=lambda x: x[0])
                target = prioritized_adjacent[0][1]
                actions.append(
                    {"bot_id": bot.bot_id, "type": "pick_up", "item_id": target.item_id}
                )
                if target.item_key is not None:
                    if active_remaining[target.item_key] > 0:
                        active_remaining[target.item_key] -= 1
                    elif preview_remaining[target.item_key] > 0:
                        preview_remaining[target.item_key] -= 1
                continue

        should_deliver_now = (
            has_active_item
            and dropoffs
            and (
                len(bot.inventory) >= 3
                or not active_candidates
                or active_remaining_count <= 0
            )
        )

        if should_deliver_now:
            next_step = bfs_next_step(grid, bot_pos, dropoff_set, blocked_without_self)
            if next_step is not None and next_step != bot_pos:
                actions.append(move_action(bot.bot_id, bot_pos, next_step))
                continue

        if len(bot.inventory) < 3:
            max_pickups = min(3 - len(bot.inventory), active_remaining_count)
            if max_pickups > 0 and active_candidates and dropoffs:
                best_batch = choose_best_batch(
                    grid,
                    bot_pos,
                    active_candidates,
                    dropoff_set,
                    blocked_without_self,
                    max_pickups,
                )
                if best_batch:
                    first_item = best_batch[0]
                    target_cells = adjacent_walkable_cells(
                        grid, first_item.x, first_item.y
                    )
                    next_step = bfs_next_step(
                        grid, bot_pos, target_cells, blocked_without_self
                    )
                    if next_step is not None and next_step != bot_pos:
                        actions.append(move_action(bot.bot_id, bot_pos, next_step))
                        continue

            best_item: ShelfItem | None = None
            best_cost: int | None = None

            for item in shelf_items:
                if item.item_key is None:
                    continue

                active_missing = active_remaining[item.item_key]
                preview_missing = preview_remaining[item.item_key]
                if active_missing <= 0 and preview_missing <= 0:
                    continue

                target_cells = adjacent_walkable_cells(grid, item.x, item.y)
                if not target_cells:
                    continue

                dist_to_pick = bfs_distance(
                    grid, bot_pos, target_cells, blocked_without_self
                )
                if dist_to_pick is None:
                    continue

                priority_penalty = 0 if active_missing > 0 else 8
                inventory_penalty = 0 if active_missing > 0 else len(bot.inventory) * 2
                cost = dist_to_pick + priority_penalty + inventory_penalty

                if best_cost is None or cost < best_cost:
                    best_cost = cost
                    best_item = item

            if best_item is not None:
                target_cells = adjacent_walkable_cells(grid, best_item.x, best_item.y)
                next_step = bfs_next_step(
                    grid, bot_pos, target_cells, blocked_without_self
                )
                if next_step is not None and next_step != bot_pos:
                    actions.append(move_action(bot.bot_id, bot_pos, next_step))
                    continue

        actions.append({"bot_id": bot.bot_id, "type": "wait"})

    return {"actions": actions}


def to_protocol_payload(payload: dict[str, Any]) -> dict[str, Any]:
    raw_actions = payload.get("actions", [])
    if not isinstance(raw_actions, list):
        return {"actions": []}

    protocol_actions: list[dict[str, Any]] = []
    for action in raw_actions:
        if not isinstance(action, dict):
            continue
        bot = action.get("bot", action.get("bot_id"))
        act = action.get("action", action.get("type"))
        if bot is None or not isinstance(act, str):
            continue
        out = {"bot": bot, "action": act}
        if "item_id" in action:
            out["item_id"] = action["item_id"]
        protocol_actions.append(out)

    return {"actions": protocol_actions}


def token_expiry_from_url(url: str) -> int | None:
    token = parse_qs(urlparse(url).query).get("token", [None])[0]
    if not token:
        return None

    parts = token.split(".")
    if len(parts) < 2:
        return None

    payload = parts[1]
    payload += "=" * (-len(payload) % 4)
    try:
        decoded = json.loads(base64.urlsafe_b64decode(payload))
    except (ValueError, json.JSONDecodeError):
        return None
    return decoded.get("exp")


def redact_url(url: str) -> str:
    parsed = urlparse(url)
    if not parsed.query:
        return url
    params = parse_qs(parsed.query)
    if "token" in params:
        params["token"] = ["<redacted>"]
    safe_query = "&".join(f"{k}={v[0]}" for k, v in sorted(params.items()))
    return parsed._replace(query=safe_query).geturl()


async def run(url: str, team: str, token: str | None) -> None:
    headers: dict[str, str] = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    print(f"Connecting to {redact_url(url)}")
    try:
        async with websockets.connect(
            url, additional_headers=headers or None, open_timeout=15
        ) as ws:
            await ws.send(
                json.dumps({"type": "join", "team": team, "difficulty": "easy"})
            )
            print(f"Connected as {team}")

            async for raw in ws:
                try:
                    message = json.loads(raw)
                except json.JSONDecodeError:
                    print(f"Skipping non-JSON message: {raw!r}")
                    continue

                # Customize this if your server uses different event names.
                event = message.get("type")
                if event in {"state", "tick", "round", "game_state"}:
                    response = build_actions(message)
                    await ws.send(json.dumps(to_protocol_payload(response)))
                elif event is None and "bots" in message:
                    response = build_actions(message)
                    await ws.send(json.dumps(to_protocol_payload(response)))
                elif event in {"game_over", "finished"}:
                    print("Game ended")
                    break
    except websockets.exceptions.InvalidStatus as exc:
        exp = token_expiry_from_url(url)
        if (
            exc.response.status_code == 403
            and exp is not None
            and exp <= int(time.time())
        ):
            print(
                "Connection rejected (HTTP 403): token in URL is expired. Get a fresh game URL."
            )
            return
        raise


def main() -> None:
    args = parse_args()
    try:
        asyncio.run(run(args.url, args.team, args.token))
    except KeyboardInterrupt:
        print("Stopped")


if __name__ == "__main__":
    main()
