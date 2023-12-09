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


def difference(a: list):
    if len(a) == 1:
        return []
    b = []
    for i, x in enumerate(a[:-1]):
        b.append(a[i+1] - x)
    return b


def is_constant(a):
    c = a[0]
    for x in a[1:]:
        if x != c:
            return False
    return True


def next_value(a):
    d = difference(a)
    if is_constant(d):
        return a[-1] + d[0]
    else:
        return a[-1] + next_value(d)


def prior_value(a):
    d = difference(a)
    if is_constant(d):
        return a[0] - d[0]
    else:
        return a[0] - prior_value(d)


@timer_func
def day09(filepath, part2=False):
    with open(filepath) as fin:
        lines = [line.strip() for line in fin.readlines()]

    hist_sum = 0
    if not part2:
        for line in lines:
            hist_sum += next_value([int(x) for x in line.split()])
    else:
        for line in lines:
            hist_sum += prior_value([int(x) for x in line.split()])

    return hist_sum


def main():
    assert day09('test09') == 114
    print(f"Part 1: {day09('input09')}")

    assert day09('test09', True) == 2
    print(f"Part 2: {day09('input09', True)}")


if __name__ == '__main__':
    main()
