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


def get_surrounding(matrix, row, col):
    sv = []
    if 1 < row:
        sv += matrix[row - 1][max(0, col[0] - 1):min(col[1] + 1, len(matrix[0]))]
    if row < len(matrix) - 1:
        sv += matrix[row + 1][max(0, col[0] - 1):min(col[1] + 1, len(matrix[0]))]
    sv += matrix[row][max(0, col[0] - 1):col[0]]
    sv += matrix[row][col[1]:min(col[1] + 1, len(matrix[0]))]

    return sv


def get_star_pos(matrix, row, col):
    if 1 < row:
        for i in range(max(0, col[0] - 1), min(col[1] + 1, len(matrix[0]))):
            if matrix[row - 1][i] == '*':
                return row - 1, i
    if row < len(matrix) - 1:
        for i in range(max(0, col[0] - 1), min(col[1] + 1, len(matrix[0]))):
            if matrix[row + 1][i] == '*':
                return row + 1, i
    if col[0] > 0:
        if matrix[row][col[0] - 1] == '*':
            return row, col[0] - 1
    if col[1] < len(matrix[0]):
        if matrix[row][col[1]] == '*':
            return row, col[1]

    return -1, -1



@timer_func
def day03(filepath, part2=False):
    with open(filepath) as fin:
        lines = [line.strip() for line in fin.readlines()]

    pn_sum = 0
    if not part2:
        for r, line in enumerate(lines):
            for entry in re.finditer(r'\d+', line):
                pn = int(entry.group())
                sv = get_surrounding(lines, r, entry.span())
                sv = ''.join(sv)
                if re.search(r'[^0-9.]', sv):
                    pn_sum += pn
        return pn_sum
    gears = []
    for r, line in enumerate(lines):
        for entry in re.finditer(r'\d+', line):
            pn = int(entry.group())
            sv = get_surrounding(lines, r, entry.span())
            sv = ''.join(sv)
            if '*' in sv:
                sp = get_star_pos(lines, r, entry.span())
                gears.append([pn, sp, 0])
    for i, gear in enumerate(gears):
        if gear[2] == 1:
            continue
        loc = gear[1]
        for j in range(i + 1, len(gears)):
            if gears[j][1] == loc:
                pn_sum += gear[0] * gears[j][0]
                gears[i][2] = 1
                gears[j][2] = 1

    return pn_sum


def main():
    assert day03('test03') == 4361
    print(f"Part 1: {day03('input03')}")

    assert day03('test03', True) == 467835
    print(f"Part 2: {day03('input03', True)}")


if __name__ == '__main__':
    main()
