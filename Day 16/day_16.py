from time import time
from collections import deque
from multiprocessing import Pool
from itertools import chain
from functools import partial
import os


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


class Grid2d:

    def __init__(self, grid):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])

    def __getitem__(self, item):
        # returns None if outside the grid
        if len(item) > 2:
            raise ValueError('Grid2D expected a list like of length 2. Length of accessor longer than expected')
        x, y = item
        if 0 <= x < self.height:
            if 0 <= y < self.width:
                return self.grid[x][y]
        return None


class LaserBeam:

    def __init__(self, pos, heading):
        self.pos = pos
        self.heading = heading

    def next_loc(self):
        x, y = self.pos
        h = self.heading
        if h == 'u':
            return x - 1, y
        elif h == 'd':
            return x + 1, y
        elif h == 'l':
            return x, y - 1
        elif h == 'r':
            return x, y + 1


class BeamMap:

    def __init__(self, grid, start=((0, -1), 'r')):
        self.grid = Grid2d(grid)
        self.beams = deque()
        self.beams.append(LaserBeam(*start))
        self.beam_tracking = set()  # set of coordinates and heading of locations beams have gone through ((x, y), d)
        self.BOUNCE_DICT = {'l': {'/': ('d', None),
                                  '\\': ('u', None),
                                  '-': ('l', None),
                                  '|': ('u', 'd'),
                                  '.': ('l', None)},
                            'r': {'/': ('u', None),
                                  '\\': ('d', None),
                                  '-': ('r', None),
                                  '|': ('u', 'd'),
                                  '.': ('r', None)},
                            'u': {'/': ('r', None),
                                  '\\': ('l', None),
                                  '-': ('l', 'r'),
                                  '|': ('u', None),
                                  '.': ('u', None)},
                            'd': {'/': ('l', None),
                                  '\\': ('r', None),
                                  '-': ('l', 'r'),
                                  '|': ('d', None),
                                  '.': ('d', None)}}

    def project_beams(self):
        while self.beams:
            beam = self.beams.popleft()
            # get the next location for the beam
            nl = beam.next_loc()
            # get the value of the grid
            ng = self.grid[nl]
            # if the next point is in the grid
            if ng:
                # if the next point is a mirror or splitter, not empty space
                if ng != '.':
                    # update the beam position
                    beam.pos = nl
                    # find the new heading(s)
                    beam.heading, split_b = self.BOUNCE_DICT[beam.heading][ng]
                    # check to see if the current beam heading has been seen before
                    if not self.beam_tracking.intersection([(nl, beam.heading)]):
                        # beam hasn't been seen before, add the record to the tracking set
                        self.beam_tracking.add((nl, beam.heading))
                        # add to end of queue
                        self.beams.append(beam)
                    # if a split exists, and it isn't in the beam tracking set
                    if split_b and not self.beam_tracking.intersection([(nl, split_b)]):
                        # add the new beam to the beam queue
                        self.beams.append(LaserBeam(nl, split_b))
                        # add the new beam to the beam tracking set
                        self.beam_tracking.add((nl, split_b))
                # beam position is empty space
                else:
                    # update beam position
                    beam.pos = nl
                    # add to beam tracking list
                    self.beam_tracking.add((nl, beam.heading))
                    # add to beam queue
                    self.beams.append(beam)
            # point is outside the grid and we don't need to do anything

    def count_energized(self):
        return len(set([p for p, d in self.beam_tracking]))

    def new_start(self, start):
        self.beam_tracking.clear()
        self.beams.clear()
        self.beams.append(LaserBeam(*start))


def f(*args):
    bm = BeamMap(*args)
    bm.project_beams()
    return bm.count_energized()


@timer_func
def day16(filepath, part2=False):
    with open(filepath) as fin:
        lines = [line.strip() for line in fin.readlines()]

    beam_map = BeamMap(lines)
    beam_map.project_beams()
    if not part2:
        return beam_map.count_energized()
    else:
        # using multiprocessing
        starts = chain([((x, y), d) for d, y in [['r', -1], ['l', len(lines[0])]] for x in range(len(lines))],
                       [((x, y), d) for d, x in [['u', len(lines)], ['d', -1]] for y in range(len(lines[0]))])
        with Pool(os.cpu_count()) as p:
            return max(p.map(partial(f, lines), starts))

        # old way
        # max_e = beam_map.count_energized()
        # for d, y in [['r', -1], ['l', len(lines[0])]]:
        #     for x in range(len(lines)):
        #         if x == 0 and d == 'r':
        #             continue
        #         beam_map.new_start(((x, y), d))
        #         beam_map.project_beams()
        #         e_c = beam_map.count_energized()
        #         if e_c > max_e:
        #             max_e = e_c
        # for d, x in [['u', len(lines)], ['d', -1]]:
        #     for y in range(len(lines[0])):
        #         beam_map.new_start(((x, y), d))
        #         beam_map.project_beams()
        #         e_c = beam_map.count_energized()
        #         if e_c > max_e:
        #             max_e = e_c
        # return max_e


def main():
    assert day16('test16') == 46
    print(f"Part 1: {day16('input16')}")

    assert day16('test16', True) == 51
    print(f"Part 2: {day16('input16', True)}")


if __name__ == '__main__':
    main()
