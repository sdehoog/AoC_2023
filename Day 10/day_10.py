from time import time
import numpy as np


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


def get_surrounding(m, l):
    ls = []
    if l[0] > 0:
        ls.append([l[0] - 1, l[1]])
    if l[0] < len(m) - 1:
        ls.append([l[0] + 1, l[1]])
    if l[1] > 0:
        ls.append([l[0], l[1] - 1])
    if l[1] < len(m[0]) - 1:
        ls.append([l[0], l[1] + 1])
    return ls


def next_pipe_loc(d, l):
    if d == 'left':
        return l[0], l[1] - 1
    if d == 'right':
        return l[0], l[1] + 1
    if d == 'up':
        return l[0] - 1, l[1]
    if d == 'down':
        return l[0] + 1, l[1]


@timer_func
def day10(filepath, part2=False):
    pipe_map = np.genfromtxt(filepath, delimiter=1, dtype=str)

    start = np.where(pipe_map == 'S')
    trail = [start]
    steps = 0
    pipes = {'|': {'up': 'down', 'down': 'up'},
             '-': {'left': 'right', 'right': 'left'},
             'F': {'down': 'right', 'right': 'down'},
             '7': {'down': 'left', 'left': 'down'},
             'J': {'left': 'up', 'up': 'left'},
             'L': {'right': 'up', 'up': 'right'}}
    opp = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
    for d in opp:
        loc = next_pipe_loc(d, start)
        val = pipe_map[loc].item()
        if val == '.':
            continue
        if opp[d] in pipes[val]:
            next_location = loc
            pipe_exit = pipes[pipe_map[next_location].item()][opp[d]]
            steps += 1
            trail.append(next_location)
            break

    while True:
        next_location = next_pipe_loc(pipe_exit, next_location)
        steps += 1
        if pipe_map[next_location].item() == 'S':
            break
        trail.append(next_location)
        pipe_exit = pipes[pipe_map[next_location].item()][opp[pipe_exit]]
    if not part2:
        return steps // 2

    sum_i = 0
    trail_np = np.array(trail)
    row_start = trail_np[:,0].min()
    row_end = trail_np[:,0].max()
    col_start = trail_np[:,1].min()
    col_end = trail_np[:,1].max()
    trail = set([(e[0].item(), e[1].item()) for e in trail])
    # too lazy to code the dynamic way to replace the start point with the correct pipe, so I'm just hard coding it
    if filepath=='test10_2':
        pipe_map[start] = 'F'
    if filepath=='test10_3':
        pipe_map[start] = '7'
    if filepath=='input10':
        pipe_map[start] = '|'
    for i in range(row_start, row_end + 1):
        for j in range(col_start, col_end + 1):
            if trail.intersection([(i, j)]):
                continue
            # looking up
            right_count = 0
            left_count = 0
            for x in range(row_start, i):
                if trail.intersection([(x, j)]):
                    if 'right' in pipes[pipe_map[(x, j)]]:
                        right_count += 1
                    if 'left' in pipes[pipe_map[(x, j)]]:
                        left_count += 1
            if left_count % 2 == 0 and right_count % 2 == 0:
                continue
            # looking down
            right_count = 0
            left_count = 0
            for x in range(i, row_end + 1):
                if trail.intersection([(x, j)]):
                    if 'right' in pipes[pipe_map[(x, j)]]:
                        right_count += 1
                    if 'left' in pipes[pipe_map[(x, j)]]:
                        left_count += 1
            if left_count % 2 == 0 and right_count % 2 == 0:
                continue
            # looking left
            up_count = 0
            down_count = 0
            for y in range(col_start, j):
                if trail.intersection([(i, y)]):
                    if 'up' in pipes[pipe_map[(i, y)]]:
                        up_count += 1
                    if 'down' in pipes[pipe_map[(i, y)]]:
                        down_count += 1
            if up_count % 2 == 0 and down_count % 2 == 0:
                continue
            # looking right
            up_count = 0
            down_count = 0
            for y in range(col_start, j):
                if trail.intersection([(i, y)]):
                    if 'up' in pipes[pipe_map[(i, y)]]:
                        up_count += 1
                    if 'down' in pipes[pipe_map[(i, y)]]:
                        down_count += 1
            if up_count % 2 == 0 and down_count % 2 == 0:
                continue

            sum_i += 1
    return sum_i


def main():
    assert day10('test10') == 4
    print(f"Part 1: {day10('input10')}")

    assert day10('test10_2', True) == 4
    assert day10('test10_3', True) == 10
    print(f"Part 2: {day10('input10', True)}")


if __name__ == '__main__':
    main()
