import sys
import heapq
import asyncio
import json
import websockets

INF = sys.maxsize
dir = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def djikstra(start, walls, n, m):
    dis = [[INF] * n for _ in range(m)]
    x, y = start
    heap = [(0, x, y)]
    while heap:
        d, i, j = heapq.heappop(heap)
        for ni, nj in dir:
            r, c = i + ni, j + nj
            if 0 <= r < m and 0 <= c < n and (r, c) not in walls and d + 1 < dis[r][c]:
                heapq.heappush(heap, (d + 1, r, c))
                dis[r][c] = d + 1
    return dis


def best_move_toward_target(start, target, walls, n, m):
    walls = set(walls)
    si, sj = start
    ti, tj = target

    distances_bot = djikstra(start, walls, n, m)
    distances_target = djikstra(target, walls, n, m)

    shortest_path = distances_bot[ti][tj]

    for ni, nj in dir:
        r, c = si + ni, sj + nj
        if (
            0 <= r < m
            and 0 <= c < n
            and distances_bot[r][c] + distances_target[r][c] == shortest_path
        ):
            return (ni, nj)
    return None


WS_URL = sys.argv[1]
print(WS_URL)


async def play():
    async with websockets.connect(WS_URL) as ws:
        while True:
            msg = json.loads(await ws.recv())

            if msg["type"] == "game_over":
                print(f"Game over! Score: {msg['score']}")
                break

            state = msg
            actions = []

            for bot in state["bots"]:
                action = decide(bot, state)
                actions.append(action)
            print(actions)
            await ws.send(json.dumps({"actions": actions}))


def decide(bot, state):
    x, y = bot["position"]
    drop_off = state["drop_off"]

    if bot["inventory"] and [x, y] == drop_off:
        return {"bot": bot["id"], "action": "drop_off"}

    if len(bot["inventory"]) >= 3:
        return move_toward(bot["id"], x, y, drop_off)

    active = next((o for o in state["orders"] if o["status"] == "active"), None)
    if not active:
        return {"bot": bot["id"], "action": "wait"}

    needed = list(active["items_required"])
    for d in active["items_delivered"]:
        if d in needed:
            needed.remove(d)

    for item in state["items"]:
        if item["type"] in needed:
            ix, iy = item["position"]
            if abs(ix - x) + abs(iy - y) == 1:
                return {"bot": bot["id"], "action": "pick_up", "item_id": item["id"]}

    for item in state["items"]:
        if item["type"] in needed:
            return move_toward(bot["id"], x, y, item["position"])

    if bot["inventory"]:
        return move_toward(bot["id"], x, y, drop_off)

    return {"bot": bot["id"], "action": "wait"}


def move_toward(bot_id, x, y, target):
    tx, ty = target
    if abs(tx - x) > abs(ty - y):
        return {"bot": bot_id, "action": "move_right" if tx > x else "move_left"}
    elif ty != y:
        return {"bot": bot_id, "action": "move_down" if ty > y else "move_up"}
    return {"bot": bot_id, "action": "wait"}


asyncio.run(play())
