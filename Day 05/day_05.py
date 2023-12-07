from time import time
from itertools import islice


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


def overlap_and_shift(r1, r2, x):
    if r2[0] <= r1[1]:
        if r2[1] >= r1[0]:
            overlap = [max(r1[0], r2[0]), min(r1[1], r2[1])]
            if r1[0] == r2[0] and r1[1] == r2[1]:
                return overlap, None
            non_overlap = [None, None]
            if r2[0] > r1[0]:
                non_overlap[0] = [r1[0], r2[0] - 1]
            if r2[1] < r1[1]:
                non_overlap[1] = [r2[1] + 1, r1[1]]
            return [i + x for i in overlap], [i for i in non_overlap if i]
    return None, [r1]


# overlap and shift testing
# print(overlap_and_shift([1, 5], [4, 7], 0))
# print(overlap_and_shift([4, 7], [1, 5], 4))
# print(overlap_and_shift([1, 10], [4, 7], 3))
# print(overlap_and_shift([4, 7], [1, 10], 5))
# print(overlap_and_shift([1, 5], [7, 9], 4))
# print(overlap_and_shift([1, 5], [1, 5], 1))


@timer_func
def day05(filepath, part2=False):
    with open(filepath) as fin:
        lines = [line.strip() for line in fin.readlines()]

    map_names = ['seed-to-soil map:',
                 'soil-to-fertilizer map:',
                 'fertilizer-to-water map:',
                 'water-to-light map:',
                 'light-to-temperature map:',
                 'temperature-to-humidity map:',
                 'humidity-to-location map:']

    if not part2:
        locs = [[int(x) for x in lines[0][6::].split()]]

        maps = {}
        for map_name in map_names:
            i = lines.index(map_name) + 1
            maps[map_name] = []
            x = True
            while x:
                line = lines[i]
                maps[map_name].append([int(x) for x in line.split()])
                i += 1
                if i == len(lines) or lines[i] == '':
                    x = False

        for map_name in map_names:
            locs.append([])
            for loc in locs[-2]:
                for map_key in maps[map_name]:
                    start = map_key[1]
                    stop = start + map_key[2]
                    if start <= loc < stop:
                        locs[-1].append(map_key[0] + (loc - start))
                        break
                else:
                    locs[-1].append(loc)

        locs[-1].sort()
        return locs[-1][0]

    # part2
    seeds = [int(x) for x in lines[0][6::].split()]
    seeds = [[seeds[i], seeds[i] + seeds[i + 1] - 1] for i in range(0, len(seeds), 2)]
    current = seeds
    unchanged = []
    changed = []
    for map_name in map_names:
        i = lines.index(map_name) + 1
        x = True
        while x:
            line = lines[i]
            cur_map = [int(x) for x in line.split()]
            map_range = [cur_map[1], cur_map[1] + cur_map[2] - 1]
            map_shift = cur_map[0] - cur_map[1]
            for j in current:
                ov, nov = overlap_and_shift(j, map_range, map_shift)
                if ov:
                    changed.append(ov)
                if nov:
                    for k in nov:
                        unchanged.append(k)
            current = list(unchanged)
            unchanged = []
            i += 1
            if i == len(lines) or lines[i] == '':
                x = False
        current = current + changed
        changed = []

    min_loc = float('inf')
    for r in current:
        if r[0] < min_loc:
            min_loc = r[0]
    return min_loc


def main():
    assert day05('test05') == 35
    print(f"Part 1: {day05('input05')}")

    assert day05('test05', True) == 46
    print(f"Part 2: {day05('input05', True)}")


if __name__ == '__main__':
    main()
