from sys import stdin

input = stdin.readline


def read_line_as(conversion):
    return map(conversion, input().strip().split())


def make_counter_clockwise(triangle):
    a, b, c = triangle
    # Calculate orientation
    area2 = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

    if area2 < 0:  # If clockwise, swap two vertices to reverse orientation
        return (a, c, b)  # Swap b and c
    else:
        return triangle


Xa, Ya = read_line_as(int)
Xb, Yb = read_line_as(int)
Xc, Yc = read_line_as(int)

area = round(abs(Xa * (Yb - Yc) + Xb * (Yc - Ya) + Xc * (Ya - Yb)) / 2, 1)
print(area)

n = int(input())


def orient(a, b, c):
    # Cross product
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def in_angle(a, b, c, p):
    return orient(a, b, p) >= 0 and orient(a, c, p) <= 0


def inside(triangle, pos):
    a, b, c = triangle

    return in_angle(a, b, c, pos) and in_angle(c, a, b, pos)


triangle = make_counter_clockwise([(Xa, Ya), (Xb, Yb), (Xc, Yc)])
count = 0
for _ in range(n):
    x, y = read_line_as(int)
    if inside(triangle, (x, y)):
        count += 1

print(count)
