import sys


def solve():
    data = sys.stdin.read().split()
    idx = 0

    n = int(data[idx])
    idx += 1

    speed = {}
    children = {}
    parent = {}

    for _ in range(n):
        name = data[idx]
        idx += 1
        spd = float(data[idx])
        idx += 1
        sup = data[idx]
        idx += 1

        speed[name] = spd
        children[name] = []

        if sup == "CEO":
            root = name
        else:
            parent[name] = sup

    for emp in speed:
        if emp in parent:
            children[parent[emp]].append(emp)

    # dp[node] = [(teams, total_speed) if node is free,
    #             (teams, total_speed) if node is matched to parent]
    dp = {}

    # Iterative post-order traversal
    order = []
    stack = [(root, False)]
    while stack:
        node, visited = stack.pop()
        if visited:
            order.append(node)
        else:
            stack.append((node, True))
            for child in children[node]:
                stack.append((child, False))

    for node in order:
        # Base: all children are free (not connected to parent/current node)
        base = (
            sum(dp[c][0][0] for c in children[node]),
            sum(dp[c][0][1] for c in children[node]),
        )

        # Try pairing node with each child; keep the best outcome
        free = base
        for c in children[node]:
            # Base[0] is all teams made up of children, remove childs contribution to the sum when it is free and add the contribution when it is not +1
            teams = base[0] - dp[c][0][0] + dp[c][1][0] + 1
            # Base[1] is total speed of all children child speed contribution of child if mathced + free child speed + the current speed of the pair
            speed_sum = base[1] - dp[c][0][1] + dp[c][1][1] + min(speed[node], speed[c])
            candidate = (teams, speed_sum)
            # If pairing node with child is better than childs current
            if candidate > free:
                free = candidate

        # If node is matched to its parent, it cannot also pair with a child
        matched = base

        dp[node] = [free, matched]

    teams, total_speed = dp[root][0]
    avg = total_speed / teams
    print(f"{teams} {avg}")


solve()

