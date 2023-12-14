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


def tilt_north(rock_map: list):
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
                    rock_map[x][y] = 'O'
                    rock_map[x + 1][y] = '.'
                    move = True
    return rock_map


def transpose(m: list):
    # transposes a list of lists
    return [list(r) for r in list(zip(*m))]


def flip(m: list):
    return m[::-1]


def spin_platform(rock_map):
    for _ in range(4):
        rock_map = tilt_north(rock_map)
        rock_map = flip(rock_map)
        rock_map = transpose(rock_map)
    return rock_map


@timer_func
def day14(filepath, part2=False):
    with open(filepath) as fin:
        lines = [line.strip() for line in fin.readlines()]

    if not part2:
        round_rocks = []
        cube_rocks = set()
        stuck_rocks = set()
        for x, line in enumerate(lines):
            for y, c in enumerate(line):
                if c == '#':
                    cube_rocks.add(complex(x, y))
                elif c == 'O':
                    round_rocks.append(complex(x, y))
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
        rock_map = [list(x) for x in lines]
        rm_dict = {}
        loop_start = 0
        loop_length = 0
        for i in range(1, 1000000000):
            rock_map = spin_platform(rock_map)
            # make a string representation of the map for hashing
            rmh = ''.join(''.join(r) for r in rock_map)
            if rmh in rm_dict:
                loop_start = rm_dict[rmh]
                loop_length = i - loop_start
                break
            else:
                rm_dict[rmh] = i
        i_f = (1000000000 - loop_start) % loop_length + loop_start
        rmh = 0
        for rmh, i in rm_dict.items():
            if i == i_f:
                break
        # unpack the string map into something easier to calculate on
        n = len(rock_map[0])
        rock_map = [rmh[i:i+n] for i in range(0, len(rmh), n)]
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
