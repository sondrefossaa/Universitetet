from sys import stdin

n, seconds = map(int, stdin.readline().split())
people = []
for _ in range(n):
    enter, exit = map(int, stdin.readline().split())
    people.append({"enters": enter, "exits": exit})
sorted_people = sorted(people, key=lambda x: x["enters"])

met = 0
a = [person["enters"] for person in sorted_people]
b = [person["exits"] for person in sorted_people]
end = a[0]
for i in range(n):
    met = max(met, end - a[i])
    end = max(end, b[i])
print(met)
