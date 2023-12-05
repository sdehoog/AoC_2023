from time import time
import regex as re


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
def day01(filepath, part2=False):
    with open(filepath) as fin:
        lines = fin.readlines()

    if not part2:
        cv = []
        for line in lines:
            for c in line:
                if c.isdigit():
                    cv.append(c)
                    break
            for c in line[::-1]:
                if c.isdigit():
                    cv[-1] += c
                    break

        cv_sum = 0
        for e in cv:
            cv_sum += int(e)

        return cv_sum

    # part 2
    cv = []
    r = re.compile('one|two|three|four|five|six|seven|eight|nine|[1-9]')
    digits = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight','nine']
    for line in lines:
        first = r.search(line).group()
        last = r.findall(line, overlapped=True)[-1]
        if len(first) > 1:
            first = str(digits.index(first) + 1)
        if len(last) > 1:
            last = str(digits.index(last) + 1)

        cv.append(int(first + last))

    cv_sum = 0
    for e in cv:
        cv_sum += int(e)

    return cv_sum


def main():
    assert day01('test01') == 142
    print(f"Part 1: {day01('input01')}")

    assert day01('test01b', True) == 281
    print(f"Part 2: {day01('input01', True)}")


if __name__ == '__main__':
    main()
