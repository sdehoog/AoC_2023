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


def tilt_east(rock_map: tuple):
    # rock map is a tuple of strings
    return tuple('#'.join([''.join(sorted(p)) for p in row.split('#')]) for row in rock_map)


def tilt_north(m: tuple):
    return rotate_counterclockwise(tilt_east(rotate_clockwise(m)))


def transpose(m: tuple):
    # transposes a tuple of strings
    return tuple(''.join(i) for i in list(zip(*m)))


def flip(m: tuple):
    # flip a tuple north-south
    return m[::-1]


def rotate_clockwise(m: tuple):
    # rotate clockwise a tuple of string
    return transpose(flip(m))


def rotate_counterclockwise(m: tuple):
    # rotate counterclockwise a tuple of strings
    return flip(transpose(m))


def spin_platform(rock_map):
    for _ in range(4):
        rock_map = rotate_clockwise(rock_map)
        rock_map = tilt_east(rock_map)
    return rock_map


@timer_func
def day14(filepath, part2=False):
    with open(filepath) as fin:
        lines = [line.strip() for line in fin.readlines()]

    if not part2:
        rock_map = tilt_north(tuple(lines))
        load = 0
        for i, row in enumerate(rock_map[::-1]):
            load += row.count('O') * (i + 1)
        return load
    else:
        rock_map = tuple(lines)
        rm_dict = {}
        loop_start = 0
        loop_length = 0
        for i in range(1, 1000000000):
            rock_map = spin_platform(rock_map)
            # make a string representation of the map for hashing
            if rock_map in rm_dict:
                loop_start = rm_dict[rock_map]
                loop_length = i - loop_start
                break
            else:
                rm_dict[rock_map] = i
        i_f = (1000000000 - loop_start) % loop_length + loop_start
        for rock_map, i in rm_dict.items():
            if i == i_f:
                break
        load = 0
        for i, row in enumerate(rock_map[::-1]):
            load += row.count('O') * (i + 1)
        return load


def main():
    assert day14('test14') == 136
    print(f"Part 1: {day14('input14')}")

    assert day14('test14', True) == 64
    print(f"Part 2: {day14('input14', True)}")


if __name__ == '__main__':
    main()
