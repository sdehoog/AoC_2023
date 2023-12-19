from time import time
from heapq import heappop, heappush


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


class Grid2d:

    def __init__(self, grid):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])

    def __getitem__(self, item):
        # returns None if outside the grid
        if len(item) > 2:
            raise ValueError('Grid2D expected a list like of length 2. Length of accessor longer than expected')
        x, y = item
        if 0 <= x < self.height:
            if 0 <= y < self.width:
                return self.grid[x][y]
        return None


def path_to_source(v, end):
    dirs = {'r': (0, 1),
            'd': (1, 0),
            'l': (0, -1),
            'u': (-1, 0)}
    path = [end]
    x, y = end
    while (x, y) != (0, 0):
        d = v[(x, y)][1][0]
        dx, dy = dirs[d]
        x, y = x - dx, y - dy
        path.append((x, y))
    return path[::-1]


def print_path(path, grid):
    for x in range(grid.height):
        for y in range(grid.width):
            if (x, y) in path:
                print('X', end='')
            else:
                print(grid[(x,y)], end='')
        print()


def opposites(a, b):
    if (a, b) in [('r', 'l'), ('l', 'r')]:
        return True
    if (a, b) in [('u', 'd'), ('d', 'u')]:
        return True
    return False


@timer_func
def day17(filepath, part2=False):
    with open(filepath) as fin:
        lines = [line.strip() for line in fin.readlines()]
    dirs = {'r': (0, 1),
            'd': (1, 0),
            'l': (0, -1),
            'u': (-1, 0)}
    grid = Grid2d(lines)
    h = [(0, (0, 0), ('r', 0))]  # heap (heat loss, (x, y), (current direction, steps taken in that direction)
    if part2:
        heappush(h, (0, (0, 0), ('d', 0)))
    v = {((0, 0), ('r', 0)): 0}  # visited nodes

    while h:
        hl, (x, y), (hd, hs) = heappop(h)
        # check in all directions
        for d, (dx, dy) in dirs.items():
            # get the grid value in that direction
            w = grid[(x + dx, y + dy)]
            # if the grid value exists
            if w:
                w = int(w)
                # check to see if we have done three steps in that direction already
                # or if the direction is the opposite of the current heading
                if (d == hd and hs == 3) or opposites(d, hd):
                    # skip this heading if we have taken the 3 steps already
                    continue
                # check to see if we are heading in the same direction
                if d == hd:
                    # increase the heading step by 1
                    nhs = hs + 1
                else:
                    # reset to 1 if a different direction
                    nhs = 1
                if ((x + dx, y + dy), (d, nhs)) in v:
                    # get the current hl value
                    chl = v[((x + dx, y + dy), (d, nhs))]
                else:
                    # else the value is inf
                    chl = float('inf')
                # check to see if this value is lower than the current
                # (looking at a new point will always trip this, since its value is inf
                if hl + w < chl:
                    # if it is heading the same direction
                    if d == hd:
                        # increase the heading step by 1
                        nhs = hs + 1
                    else:
                        # reset to 1 if a different direction
                        nhs = 1
                    # add/update the visited points
                    v[(x + dx, y + dy), (d, nhs)] = hl + w
                    # add the point to the heap
                    heappush(h, (hl + w, (x + dx, y + dy), (d, nhs)))
    # path = path_to_source(v, (len(lines)-1, len(lines[0])-1))
    # print_path(path, grid)
    ends = [hl for ((x, y), (d, hs)), hl in v.items() if (x, y) == (grid.height - 1, grid.width - 1)]
    ans = min(ends)
    return ans


def main():
    assert day17('test17') == 102
    print(f"Part 1: {day17('input17')}")

    # assert day17('test17', True) == 94
    # print(f"Part 2: {day17('input17', True)}")


if __name__ == '__main__':
    main()
