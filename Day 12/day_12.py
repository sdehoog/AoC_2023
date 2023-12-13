from time import time
from functools import cache


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


def count_groups(string):
    # return an empty list if the input is empty
    if not string:
        return tuple()
    # Initialize an empty list to store the output
    output = []
    # Initialize a variable to store the current group count
    count = 0
    # Loop through each character in the string
    for char in string:
        # Check if the character is '#'
        if char == '#':
            # Increment the count by 1
            count += 1
        # Check if the character is '.'
        elif char == '.':
            # Check if the count is not zero
            if count != 0:
                # Add the count to the output list
                output.append(count)
                # Reset the count to zero
                count = 0
    # Append the last count if the last character was a '#'
    if string[-1] == '#':
        output.append(count)
    # Return the output list
    return tuple(output)


# Example usage:
# string = '#.#.###'
# print(count_groups(string))  # Output: [1, 1, 3]


def find_permutations(string):
    # Import the itertools module
    import itertools
    # Initialize an empty list to store the output
    output = []
    # Loop through all possible combinations of '.' and '#' for the '?' characters
    for combo in itertools.product(['.', '#'], repeat=string.count('?')):
        # Initialize a variable to store the current permutation
        perm = string
        # Replace each '?' with the corresponding character in the combo
        for char in combo:
            perm = perm.replace('?', char, 1)
        # Add the permutation to the output list
        output.append(perm)
    # Return the output list
    return output


# Example usage:
# string = '#.#.?#?'
# print(find_permutations(string))  # Output: ['#.#..#', '#.#.#']


@cache
def find_combos_trim(s, g):
    if not s:  # if s is empty, check if there are entries left in g
        return g == ()  # return True if g is empty
    if not g:  # if g is empty, check if there are any broken springs left in s
        return '#' not in s
    combos = 0
    if s[0] in '.?':  # skip if it is a good spring, or pretend it is a good spring
        combos += find_combos_trim(s[1:], g)
    if s[0] in '#?':
        ls = len(s)
        fs = g[0]  # first spring group
        ss = s[:fs]  # slice of the string equal to the len of the first spring group
        if fs <= ls:  # make sure the len of the string is longer than the first required spring
            if '.' not in ss:  # make sure there are no good springs in slice
                if ls == fs or s[fs] != '#':  # if we have the whole rest of the slice
                    # or the next thing after our slice is not a good spring
                    combos += find_combos_trim(s[fs + 1:], g[1:])  # recursive

    return combos


# TODO Fix this broken implementation
@cache
def fcs(s, g):
    if len(s) < sum(g):
        return 0
    if not s:  # if s is empty, check if there are entries left in g
        return g == ()  # return True if g is empty
    if not g:  # if g is empty, check if there are any broken springs left in s
        return '#' not in s
    combos = 0
    if '?' in s:
        i = s.index('?')
    else:
        return count_groups(s) == g
    sbi = s[:i]
    sai = s[i+1:]

    # if the ? is a .
    gb = count_groups(sbi)
    gt = g[:len(gb)]  # trimming g to match the len of gb
    if gt == gb:
        combos += fcs(sai, g[len(gb):])

    # if the ? is a #
    gb = count_groups(sbi + '#')
    gt = g[:len(gb)]
    if gb[:-1] == gt[:-1]:
        if gb[-1] < gt[-1]:
            combos += fcs(sbi + '#' + sai, g)
        if gb[-1] == gt[-1] and i != len(s) and (not sai or sai[0] != '#'):
            combos += fcs(sai[1:], g[len(gb):])

    return combos


@timer_func
def day12(filepath, part2=False):
    with open(filepath) as fin:
        lines = [line.strip() for line in fin.readlines()]
    combos = 0
    for line in lines:
        records, groups = line.split()
        groups = tuple([int(x) for x in groups.split(',')])

        # brute force way
        # perms = find_permutations(records)
        # for perm in perms:
        #     if count_groups(perm) == groups:
        #         combos += 1

        # recursive way
        # if not part2:
        #     combos += find_combos_trim(records, groups)
        # else:
        #     combo = find_combos_trim('?'.join([records for _ in range(5)]), groups * 5)
        #     combos += combo

        # other recursive way
        if not part2:
            combos += fcs(records, groups)
        else:
            combo = fcs('?'.join([records for _ in range(5)]), groups * 5)
            combos += combo

    return combos


def main():
    assert day12('test12') == 21
    print(f"Part 1: {day12('input12')}")

    assert day12('test12', True) == 525152
    print(f"Part 2: {day12('input12', True)}")


if __name__ == '__main__':
    main()
