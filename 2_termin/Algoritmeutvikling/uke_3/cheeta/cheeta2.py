from sys import stdin

stdin.readline()

cheetas = []
for line in stdin:
    start_time, vel = map(int, line.split())
    cheetas.append({"start_time": start_time, "vel": vel, "distance": 0, "time": 0})


time = max(cheeta["start_time"] for cheeta in cheetas)


def cheeta_pos_at_time(cheeta, time):
    cheeta["distance"] = cheeta["vel"] * max(0, time - cheeta["start_time"])
    return float(cheeta["distance"])


def check(time):
    return cheeta_pos_at_time(cheetas[0], time) <= cheeta_pos_at_time(cheetas[-1], time)


def get_distance_span_at_time(time):
    return max(cheeta_pos_at_time(cheeta, time) for cheeta in cheetas) - min(
        cheeta_pos_at_time(cheeta, time) for cheeta in cheetas
    )


epsilon = pow(10, -2)
lo = time
hi = time
while not check(hi):
    hi *= 2
print(hi)
while hi - lo >= epsilon:
    mid = (lo + hi) / 2.0
    print(mid)
    if get_distance_span_at_time(mid) > get_distance_span_at_time(mid + epsilon):
        lo = mid
    else:
        hi = mid

print(
    f"{abs(cheeta_pos_at_time(cheetas[0], lo) - cheeta_pos_at_time(cheetas[-1], lo)):.3f}"
)
