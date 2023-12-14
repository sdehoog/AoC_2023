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


def print_rocks(round_rocks, cube_rocks, lims):
    for r in range(lims[0]):
        for c in range(lims[1]):
            if complex(r, c) in round_rocks:
                print('O', end='')
            elif complex(r, c) in cube_rocks:
                print('#', end='')
            else:
                print('.', end='')
        print()
    print()


def list_to_str(lst):
    output = ''
    for i in lst:
        output += str(i)
    return output


def tilt_north(rock_map: tuple):
    rock_map = list(rock_map)
    move = True
    while move:
        move = False
        for x, line in enumerate(rock_map[1:]):
            # x will be off by one
            for y, c in enumerate(line):
                if rock_map[x + 1][y] in '.#':
                    continue
                if rock_map[x][y] in '#O':
                    continue
                else:
                    rock_map[x] = rock_map[x][:y] + 'O' + rock_map[x][y + 1:]
                    rock_map[x + 1] = rock_map[x + 1][:y] + '.' + rock_map[x + 1][y + 1:]
                    move = True
    return tuple(rock_map)


def transpose(m: tuple):
    # transposes a tuple of strings
    m = list(zip(*m))
    for i, row in enumerate(m):
        m[i] = list_to_str(row)
    return tuple(m)


def spin_platform(rock_map: tuple):
    # tilt north
    rock_map = tilt_north(rock_map)

    # tilt west, going to use the same algo as tilt north
    rock_map = transpose(rock_map)
    rock_map = tilt_north(rock_map)
    rock_map = transpose(rock_map)

    # tilt south
    rock_map = rock_map[::-1]
    rock_map = tilt_north(rock_map)
    rock_map = rock_map[::-1]

    # tilt east
    rock_map = transpose(rock_map)
    rock_map = rock_map[::-1]
    rock_map = tilt_north(rock_map)
    rock_map = rock_map[::-1]
    rock_map = transpose(rock_map)

    return tuple(rock_map)


@timer_func
def day14(filepath, part2=False):
    with open(filepath) as fin:
        lines = [line.strip() for line in fin.readlines()]

    round_rocks = []
    cube_rocks = set()
    stuck_rocks = set()
    for x, line in enumerate(lines):
        for y, c in enumerate(line):
            if c == '#':
                cube_rocks.add(complex(x, y))
            elif c == 'O':
                round_rocks.append(complex(x, y))

    if not part2:
        while round_rocks:
            moved_rocks = []
            for rock in round_rocks:
                if rock.real == 0:
                    stuck_rocks.add(rock)
                elif stuck_rocks.intersection([rock - 1]) or cube_rocks.intersection([rock - 1]):
                    stuck_rocks.add(rock)
                else:
                    moved_rocks.append(rock - 1)
            round_rocks = [*moved_rocks]
        round_rocks = stuck_rocks
        rock_load = 0
        height = len(lines)
        for rock in round_rocks:
            rock_load += height - rock.real

        return int(rock_load)
    else:
        rock_map = tuple(lines)
        rm_dict = {}
        loop_start = 0
        loop_length = 0
        for i in range(1, 1000000000):
            rock_map = spin_platform(rock_map)
            if rock_map in rm_dict:
                loop_start = rm_dict[rock_map]
                loop_length = i - loop_start
                # print(f'Loop found after {i} iterations')
                # print(f'Loop start: {loop_start}'
                # print(f'Loop length: {loop_length}')
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
