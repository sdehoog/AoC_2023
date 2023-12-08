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


# Define a helper function to find the greatest common divisor of two numbers
def gcd(a, b):
    # Use Euclid's algorithm to find the gcd
    while b != 0:
        a, b = b, a % b
    return a


# Define the main function to find the least common multiple of a list of numbers
def lcm(numbers):
    # Initialize the lcm to the first number in the list
    lcm = numbers[0]
    # Loop through the rest of the numbers in the list
    for num in numbers[1:]:
        # Use the formula lcm(a, b) = (a * b) / gcd(a, b)
        lcm = (lcm * num) // gcd(lcm, num)
    # Return the lcm
    return lcm


@timer_func
def day08(filepath, part2=False):
    with open(filepath) as fin:
        lines = [line.strip() for line in fin.readlines()]

    ins = lines[0]
    node = [line[:3] for line in lines[2:]]
    paths = [[line[7:10], line[12:15]] for line in lines[2:]]
    steps = 0
    if not part2:
        cur = 'AAA'
        while cur != 'ZZZ':
            steps += 1
            side = ins[steps % len(ins) - 1]
            cur = paths[node.index(cur)][0 if side == 'L' else 1]
        return steps
    else:
        ghosts = [x for x in node if x[2] == 'A']
        steps = []
        for g in ghosts:
            steps.append(0)
            while g[2] != 'Z':
                steps[-1] += 1
                side = ins[steps[-1] % len(ins) - 1]
                g = paths[node.index(g)][0 if side == 'L' else 1]

        return lcm(steps)


def main():
    assert day08('test08') == 6
    print(f"Part 1: {day08('input08')}")

    assert day08('test08_2', True) == 6
    print(f"Part 2: {day08('input08', True)}")


if __name__ == '__main__':
    main()
