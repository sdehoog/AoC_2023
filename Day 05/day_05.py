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


@timer_func
def day05(filepath, part2=False):
    with open(filepath) as fin:
        lines = [line.strip() for line in fin.readlines()]
    locs = [[int(x) for x in lines[0][6::].split()]]
    map_names = ['seed-to-soil map:',
                 'soil-to-fertilizer map:',
                 'fertilizer-to-water map:',
                 'water-to-light map:',
                 'light-to-temperature map:',
                 'temperature-to-humidity map:',
                 'humidity-to-location map:']
    maps = {}
    for map_name in map_names:
        i = lines.index(map_name) + 1
        maps[map_name] = []
        while True:
            line = lines[i]
            maps[map_name].append([int(x) for x in line.split()])
            i += 1
            if i == len(lines) or lines[i] == '':
                break

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


def main():
    assert day05('test05') == 35
    print(f"Part 1: {day05('input05')}")

    # assert day05('test05', True) == 1
    # print(f"Part 2: {day05('input05', True)}")


if __name__ == '__main__':
    main()
