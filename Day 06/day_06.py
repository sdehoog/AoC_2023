from time import time
from math import floor, ceil


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


@timer_func
def day06(filepath, part2=False):
    with open(filepath) as fin:
        lines = [line.strip() for line in fin.readlines()]

    if not part2:
        ts = [int(x) for x in lines[0][11::].split()]
        ds = [int(x) for x in lines[1][11::].split()]
    else:
        ts = [int(''.join(x for x in lines[0][11::].split()))]
        ds = [int(''.join(x for x in lines[1][11::].split()))]
    r = 1
    for t, d in zip(ts, ds):
        r1 = (-t + (t ** 2 - 4 * -1 * -d) ** (1 / 2)) / 2 * -1
        r2 = (-t - (t ** 2 - 4 * -1 * -d) ** (1 / 2)) / 2 * -1
        r1 = floor(r1 + 1)
        r2 = ceil(r2 - 1)
        r *= (r2 - r1 + 1)
    return r


def main():
    assert day06('test06') == 288
    print(f"Part 1: {day06('input06')}")

    assert day06('test06', True) == 71503
    print(f"Part 2: {day06('input06', True)}")


if __name__ == '__main__':
    main()
