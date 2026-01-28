from sys import stdin

stdin.readline()

cheetas = []
for line in stdin:
    start_time, vel = map(int, line.split())
    cheetas.append({"start_time": start_time, "vel": vel, "distance": 0, "time": 0})


time = max(cheeta["start_time"] for cheeta in cheetas)


def cheeta_pos_at_time(cheeta):
    cheeta["distance"] = cheeta["vel"] * max(0, time - cheeta["start_time"])
    return float(cheeta["distance"])


epsilon = pow(10, -2)
min_distance = float("inf")
prevmax = 0
while True:
    cheeta_pos = [cheeta_pos_at_time(cheeta) for cheeta in cheetas]
    time += epsilon

    cur_max_distance = abs(max(cheeta_pos) - min(cheeta_pos))
    min_distance = min(min_distance, cur_max_distance)

    if min_distance <= epsilon or min_distance == prevmax:
        break
    prevmax = min_distance

print(f"{min_distance:.3f}")
