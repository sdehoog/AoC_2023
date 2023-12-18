from time import time


def timer_func(func):
    # This function shows the execution time of
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2 - t1):.4f}s')
        return result

    return wrap_func


def shoelace_area(points):
    # points is a list of tuples (x, y) representing the vertices of the polygon
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    return abs(sum([x[i] * (y[(i + 1) % len(y)] - y[i - 1]) for i in range(len(x))])) // 2


@timer_func
def day18(filepath, part2=False):
    with open(filepath) as fin:
        lines = [line.strip() for line in fin.readlines()]

    points = [(0, 0)]
    for line in lines:
        if not part2:
            d, l, c = line.split()
            p = points[-1]
            if d == 'U':
                points.append((p[0] - int(l), p[1]))
            elif d == 'D':
                points.append((p[0] + int(l), p[1]))
            elif d == 'R':
                points.append((p[0], p[1] + int(l)))
            elif d == 'L':
                points.append((p[0], p[1] - int(l)))
        else:
            _, _, h = line.split()
            p = points[-1]
            d = h[-2]
            length = int(h[2:-2], 16)
            # 0 means R, 1 means D, 2 means L, and 3 means U
            if d == '3':
                points.append((p[0] - length, p[1]))
            elif d == '1':
                points.append((p[0] + length, p[1]))
            elif d == '0':
                points.append((p[0], p[1] + length))
            elif d == '2':
                points.append((p[0], p[1] - length))
    # find the points on the boundary
    if part2:
        c = [int(line.split()[2][2:-2], 16) for line in lines]
        b = sum(c)
    else:
        b = sum([int(line.split()[1]) for line in lines])
    # shoelace formula to get the polygon area
    a = shoelace_area(points)
    # picks theorem to get the interior points
    i = a - (b // 2) + 1
    # return interior plus boundary points
    return int(i + b)


def main():
    assert day18('test18') == 62
    print(f"Part 1: {day18('input18')}")

    assert day18('test18', True) == 952408144115
    print(f"Part 2: {day18('input18', True)}")


if __name__ == '__main__':
    main()
