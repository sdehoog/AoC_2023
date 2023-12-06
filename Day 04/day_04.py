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
def day04(filepath, part2=False):
    with open(filepath) as fin:
        lines = fin.readlines()

    total_score = 0
    sc = lines[0].index(':') + 1
    hb = lines[0].index('|')
    ec = [0] * len(lines)
    for i, line in enumerate(lines):

        wn = set(line[sc:hb].split())
        num = set(line[hb + 1::].split())
        wins = len(wn.intersection(num))
        if not part2:
            if wins > 0:
                total_score += 2 ** (wins - 1)
        else:
            if wins > 0:
                for j in range(wins):
                    ec[i + j + 1] += 1 * (ec[i] + 1)

            total_score += ec[i] + 1

    return total_score


def main():
    assert day04('test04') == 13
    print(f"Part 1: {day04('input04')}")

    assert day04('test04', True) == 30
    print(f"Part 2: {day04('input04', True)}")


if __name__ == '__main__':
    main()
