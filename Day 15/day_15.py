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
def day15(filepath, part2=False):
    with open(filepath) as fin:
        lines = [line.strip() for line in fin.readlines()]

    nums = lines[0].split(',')
    if not part2:
        v_sum = 0
        for n in nums:
            v = 0
            for c in n:
                v += ord(c)
                v *= 17
                v %= 256
            v_sum += v
        return v_sum
    else:
        lens_dict = {}
        for n in nums:
            # split out the label and lens
            label, lens = re.split('[-=]', n)
            # find the box number
            box = 0
            for c in label:
                box += ord(c)
                box *= 17
                box %= 256
            # if there is a lens number, it is an addition '=' operator
            if lens:
                lens = int(lens)
                # check to see if that box has lenses in it yet
                if box in lens_dict:
                    # check to see if that label already exists in the box
                    for p, l in enumerate(lens_dict[box]):
                        if label in l:
                            lens_dict[box][p][label] = lens
                            break
                    # add label and lens to the end of the list
                    else:
                        lens_dict[box].append({label: lens})
                else:
                    lens_dict[box] = [{label: lens}]
            # subtraction operator
            else:
                # check to see if lenses in that box exist yet
                if box in lens_dict:
                    # loop over the lenses in the box
                    for p, l in enumerate(lens_dict[box]):
                        # if that label does exist
                        if label in l:
                            # remove the lens
                            lens_dict[box].pop(p)
                            break
        lens_power_sum = 0
        for bn, b in lens_dict.items():
            if b:
                for i, l in enumerate(b, 1):
                    lens_power_sum += (bn + 1) * i * [*l.values()][0]
        return lens_power_sum


def main():
    assert day15('test15') == 1320
    print(f"Part 1: {day15('input15')}")

    assert day15('test15', True) == 145
    print(f"Part 2: {day15('input15', True)}")


if __name__ == '__main__':
    main()
