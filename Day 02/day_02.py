from time import time
import re


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
def day02(filepath, part2=False):
    with open(filepath) as fin:
        lines = fin.readlines()

    if not part2:
        red_max = 12
        green_max = 13
        blue_max = 14
        id_sum = 0
        for line in lines:
            if red_max >= max([int(i) for i in re.findall(r'(\d+) red', line)]):
                if blue_max >= max([int(i) for i in re.findall(r'(\d+) blue', line)]):
                    if green_max >= max([int(i) for i in re.findall(r'(\d+) green', line)]):
                        id_sum += int(re.search(r'Game (\d+)', line).groups()[0])

        return id_sum
    set_sum = 0
    for line in lines:
        red_max = max([int(i) for i in re.findall(r'(\d+) red', line)])
        blue_max = max([int(i) for i in re.findall(r'(\d+) blue', line)])
        green_max = max([int(i) for i in re.findall(r'(\d+) green', line)])
        set_sum += red_max * blue_max * green_max
    return set_sum


def main():
    assert day02('test02') == 8
    print(f"Part 1: {day02('input02')}")

    assert day02('test02', True) == 2286
    print(f"Part 2: {day02('input02', True)}")


if __name__ == '__main__':
    main()
