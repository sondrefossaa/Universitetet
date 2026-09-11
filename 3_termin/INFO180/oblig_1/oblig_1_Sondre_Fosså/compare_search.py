"""Run each search 10 times on the current grid and save Markdown averages."""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from queue import Queue, LifoQueue, PriorityQueue
from statistics import mean
from time import perf_counter

from grid_walk_space import GridWalkSpace
from zero_h import ZeroH
from max_dim_h import MaxDimH
from pythagoras_h import PythagorasH
from approx_max_dim_h import ApproxMaxDimH


RUNS = 10


def main():
    # Store classes here so each run gets a fresh queue and heuristic.
    algorithms = [
        ("Breadth-first", Queue, ZeroH),
        ("Depth-first", LifoQueue, ZeroH),
        ("Lowest-cost-first", PriorityQueue, ZeroH),
        ("MaxDimH", PriorityQueue, MaxDimH),
        ("PythagorasH", PriorityQueue, PythagorasH),
        ("ApproxMaxDimH", PriorityQueue, ApproxMaxDimH),
    ]

    report = [
        "# Search comparison",
        "",
        f"Each algorithm was run {RUNS} times on the same grid and costs.",
        "Time measures solve(); search-object setup is excluded.",
        "Visited nodes and path length follow the original program's counting:",
        "the goal counts as visited, and path length counts nodes, including the start.",
        "Path averages include successful runs only; time and visited averages include all runs.",
        "Repeated runs measure timing variation, not performance across different grids.",
        "",
        "| Algorithm | Solved | Avg time (s) | Avg visited | Avg path length | Avg cost |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]

    for name, queue_class, heuristic_class in algorithms:
        times, visited, lengths, costs = [], [], [], []

        for run in range(RUNS):
            print(f"{name}: run {run + 1}/{RUNS}", flush=True)
            space = GridWalkSpace(queue_class(), heuristic_class())

            # Capture solve()'s prints so the terminal only shows progress.
            with redirect_stdout(StringIO()):
                start = perf_counter()
                path = space.solve()
                elapsed = perf_counter() - start

            times.append(elapsed)
            visited.append(len(space.visited) + (1 if path is not None else 0))
            if path is not None:
                lengths.append(len(path.node_list))
                costs.append(path.cost)

        avg_length = f"{mean(lengths):.1f}" if lengths else "N/A"
        avg_cost = f"{mean(costs):.1f}" if costs else "N/A"
        report.append(
            f"| {name} | {len(lengths)}/{RUNS} | {mean(times):.4f} | "
            f"{mean(visited):.1f} | {avg_length} | {avg_cost} |"
        )

    output = Path(__file__).with_name("search_comparison.md")
    output.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Saved results to {output}")


if __name__ == "__main__":
    main()
