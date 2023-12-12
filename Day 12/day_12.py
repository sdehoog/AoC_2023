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


def find_combos_trim(s, g):
    if len(s) < (sum(g) + len(g) - 1):
        return 0
    if not s and not g:
        return 1
    if not g and '#' in s:
        return 0
    combos = 0
    if '?' in s:
        i = s.index('?')

        s1 = s.replace('?', '#', 1)
        s11 = s1[:i+1]
        g1 = count_groups(s11)
        gt = g[:len(g1)]
        if g1 == gt or g1[-1] < gt[-1]:
            combos += find_combos_trim(s1, g)

        s2 = s.replace('?', '.', 1)
        s21 = s2[:i+1]
        g2 = count_groups(s21)
        gt = g[:len(g2)]
        if g2 == gt or g2[-1] < gt[-1]:
            combos += find_combos_trim(s2, g)

    else:
        if count_groups(s) == g:
            return combos + 1
        else:
            return combos

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
        if not part2:
            combos += find_combos_trim(records, groups)
        else:
            combo = find_combos_trim('?'.join([records for _ in range(5)]), groups * 5)
            combos += combo
    return combos


def main():
    assert day12('test12') == 21
    print(f"Part 1: {day12('input12')}")

    assert day12('test12', True) == 525152
    print(f"Part 2: {day12('input12', True)}")


if __name__ == '__main__':
    main()
