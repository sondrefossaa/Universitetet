from sys import stdin

input = stdin.readline

n = int(input())

adj = [[] for _ in range(n)]

for i in range(n):
    for val in map(int, input().split()):
        adj[i].append(val)


def is_safe(v, graph, color, c):
    for neighbor in graph[v]:
        if color[neighbor] == c:
            return False  # Check if adj vertex has same color
    return True


def graph_coloring_util(v, graph, color, m):
    if v == len(graph):
        # If all vertices are colored, return true
        return True
    first_new_color = min(
        m,
        max(color) + 1,
    )
    for c in range(1, first_new_color + 1):
        if is_safe(v, graph, color, c):
            color[v] = c

            # Recur for the next vertices
            if graph_coloring_util(v + 1, graph, color, m):
                return True

            # Backtrack
            color[v] = 0

    return False  # No solution found for this coloring


def graph_coloring(graph, m):
    n = len(graph)
    color = [0] * n

    if not graph_coloring_util(0, graph, color, m):
        return 0

    # Count unique colors to determine chromatic number
    unique_colors = set(color)
    return len(unique_colors)


# Find and output the chromatic number
for i in range(2, n + 1):
    chromatic_number = graph_coloring(adj, i)
    if chromatic_number:
        print(chromatic_number)
        exit()

