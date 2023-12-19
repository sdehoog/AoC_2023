from time import time
import re
from math import prod


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


def rate_part(part, workflows, wfn):
    if wfn in 'AR':
        return wfn
    cwf = workflows[wfn]
    for step in cwf:
        # if the step is a string, it is either accepted, rejected, or sent to another workflow
        if isinstance(step, str):
            # if the step is either A or R
            if step in 'AR':
                # return the step
                return step
            else:
                # else, run it through the workflow it says to
                return rate_part(part, workflows, step)
        # otherwise we have to do the evaluation
        else:
            if step['op'] == '<':
                if part[step['cat']] < step['val']:
                    return rate_part(part, workflows, step['dst'])
            else:
                if part[step['cat']] > step['val']:
                    return rate_part(part, workflows, step['dst'])


def less_than_range(r, v):
    l, u = r
    if l < v <= u:
        return (l, v-1), (v, u)
    elif v <= l:
        return None, (l, u)
    elif v > u:
        return (l, u), None


def greater_than_range(r, v):
    l, u = r
    if l <= v < u:
        return (l, v), (v + 1, u)
    elif v < l:
        return None, (l, u)
    elif v >= u:
        return (l, u), None


def rate_part_range(part, workflows, wfn):
    if wfn == 'A':
        return prod([v[1] - v[0] + 1 for c, v in part.items() if c in 'xmas'])
    elif wfn == 'R':
        return 0
    combos = 0
    cwf = workflows[wfn]
    for step in cwf:
        # if the step is a string, it is either accepted, rejected, or sent to another workflow
        if isinstance(step, str):
            # if the step is either A or R
            if step in 'A':
                # add the product of the ranges to the combos
                combos += prod([v[1] - v[0] + 1 for c, v in part.items() if c in 'xmas'])
            else:
                # else, run it through the workflow it says to
                combos += rate_part_range(part, workflows, step)
        # otherwise we have to do the evaluation
        else:
            if step['op'] == '<':
                # split the range into the less than and greater than
                l, u = less_than_range(part[step['cat']], step['val'])
                # lower than range gets sent to the next workflow
                if l:
                    new_part = part.copy()
                    new_part[step['cat']] = l
                    combos += rate_part_range(new_part, workflows, step['dst'])
                # upper range remains to go through the rest of this workflow
                if u:
                    part[step['cat']] = u
            else:
                # split the range
                l, u = greater_than_range(part[step['cat']], step['val'])
                # lower range remains to go through the rest of this workflow
                if l:
                    part[step['cat']] = l
                # upper range goes to the next workflow
                if u:
                    new_part = part.copy()
                    new_part[step['cat']] = u
                    combos += rate_part_range(new_part, workflows, step['dst'])

    return combos


@timer_func
def day19(filepath, part2=False):
    with open(filepath) as fin:
        wfs, ps = fin.read().split('\n\n')

    wfl = {}
    for wf in wfs.split('\n'):
        name = re.search(r'(.*){', wf).groups()[0]
        wfl[name] = []
        for entry in re.search(r'{(.*)}', wf).groups()[0].split(','):
            if ':' in entry:
                cat, op, val, dst = re.search(r'(.)([><])(\d*):([a-zA-Z]*)', entry).groups()
                wfl[name].append({'cat': cat,
                                  'op': op,
                                  'val': int(val),
                                  'dst': dst})
            else:
                wfl[name].append(entry)

    parts = [{e[0]: int(e[2:]) for e in p[1:-1].split(',')} for p in ps.split('\n')]

    if not part2:
        for part in parts:
            part['fd'] = rate_part(part, wfl, 'in')
        return sum([sum([v for c, v in p.items() if c in 'xmas']) for p in parts if p['fd'] == 'A'])
    else:
        part = {i: (1, 4000) for i in 'xmas'}
        return rate_part_range(part, wfl, 'in')


def main():
    assert day19('test19') == 19114
    print(f"Part 1: {day19('input19')}")

    assert day19('test19', True) == 167409079868000
    print(f"Part 2: {day19('input19', True)}")


if __name__ == '__main__':
    main()
