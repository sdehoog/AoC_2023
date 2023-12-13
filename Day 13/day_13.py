from time import time
import numpy as np


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


def score_map(m, smudge=False):
    m = np.array([np.array([*x]) for x in m])
    m = m == '#'
    # searching columns first
    for i in range(1, m.shape[1]):
        # left slice
        m_l = m[:, 0:i]
        m_r = m[:, i:]
        w = min(m_l.shape[1], m_r.shape[1])
        # reduce left and right to the same wide
        m_l = m_l[:, -w:]
        m_r = m_r[:, :w]
        # flip the right side
        m_r = m_r[:, ::-1]
        if not smudge:
            if (m_l == m_r).all():
                return i
        else:
            if (~(m_l == m_r)).sum() == 1:
                return i
    for i in range(1, m.shape[0]):
        m_u = m[0:i]
        m_d = m[i:]
        h = min(m_u.shape[0], m_d.shape[0])
        m_u = m_u[-h:]
        m_d = m_d[:h]
        m_d = m_d[::-1]
        if not smudge:
            if (m_u == m_d).all():
                return i * 100
        else:
            if (~(m_u == m_d)).sum() == 1:
                return i * 100
    return 0


@timer_func
def day13(filepath, part2=False):
    with open(filepath) as fin:
        maps = [[line.strip() for line in group.split('\n')] for group in fin.read().split('\n\n')]

    score = 0
    for m in maps:
        score += score_map(m,part2)

    return score


def main():
    assert day13('test13') == 405
    print(f"Part 1: {day13('input13')}")

    assert day13('test13', True) == 400
    print(f"Part 2: {day13('input13', True)}")


if __name__ == '__main__':
    main()
