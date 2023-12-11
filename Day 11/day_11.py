import bisect
from time import time
import numpy as np
from bisect import bisect


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
def day11(filepath, expansion_scale=2):
    star_map = np.genfromtxt(filepath, delimiter=1, dtype=str, comments='%')
    star_map = star_map == '#'
    empty_row = np.where(~star_map.any(axis=1))[0].tolist()
    empty_col = np.where(~star_map.any(axis=0))[0].tolist()

    galaxies = [complex(i, j) for i, j in zip(np.where(star_map)[0], np.where(star_map)[1])]

    d = 0
    for i, g in enumerate(galaxies):
        for j, h in enumerate(galaxies[i+1:]):
            d += abs((h-g).real)
            d += abs((h-g).imag)
            d += (expansion_scale - 1) * abs(bisect(empty_row, int(h.real)) - bisect(empty_row, int(g.real)))
            d += (expansion_scale - 1) * abs(bisect(empty_col, int(h.imag)) - bisect(empty_col, int(g.imag)))

    return int(d)


def main():
    assert day11('test11') == 374
    print(f"Part 1: {day11('input11')}")

    assert day11('test11', 100) == 8410
    print(f"Part 2: {day11('input11', 1000000)}")


if __name__ == '__main__':
    main()
