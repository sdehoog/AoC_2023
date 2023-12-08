from time import time
from collections import Counter


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


class Hand:
    def __init__(self, c: str, b: int):
        self.cards = c
        self.bid = b
        self.type = self.__find_type()

    def __find_type(self):
        freq = Counter(self.cards)
        if freq.most_common(1)[0][1] == 5:
            return 6
        if freq.most_common(1)[0][1] == 4:
            return 5
        if freq.most_common(1)[0][1] == 3 and freq.most_common(2)[1][1] == 2:
            return 4
        if freq.most_common(1)[0][1] == 3:
            return 3
        if freq.most_common(1)[0][1] == 2 and freq.most_common(2)[1][1] == 2:
            return 2
        if freq.most_common(1)[0][1] == 2:
            return 1
        return 0

    def __lt__(self, other):
        ranks = '23456789TJQKA'
        if self.type < other.type:
            return True
        elif self.type > other.type:
            return False
        elif self.type == other.type:
            for x, y in zip(self.cards, other.cards):
                if ranks.index(x) < ranks.index(y):
                    return True
                elif ranks.index(x) > ranks.index(y):
                    return False

    def __gt__(self, other):
        return not self < other

    def __str__(self):
        return self.cards


class Hand2(Hand):
    def __init__(self, c: str, b: int):
        super().__init__(c, b)
        self.type = self.__find_type()

    def __find_type(self):
        freq = Counter(self.cards)
        if freq['J'] == 5:
            return 6
        if freq.most_common(1)[0][1] + freq['J'] == 5:
            return 6
        if freq['J'] == 4:
            return 6
        if freq['J'] == 3 and freq.most_common(2)[1][1] == 2:
            return 6
        if freq.most_common(1)[0][1] == 4:
            return 5
        if freq['J'] == 3:
            return 5
        if Counter(freq.values())[2] == 2 and freq['J'] == 2:
            return 5
        if freq.most_common(1)[0][1] == 3 and freq['J'] == 1:
            return 5
        if freq.most_common(1)[0][1] == 3 and freq.most_common(2)[1][1] == 2:
            return 4
        if freq.most_common(1)[0][1] == 2 and freq.most_common(2)[1][1] == 2 and freq['J'] == 1:
            return 4
        if freq.most_common(1)[0][1] == 3:
            return 3
        if freq['J'] == 2:
            return 3
        if freq.most_common(1)[0][1] == 2 and freq['J'] == 1:
            return 3
        if freq.most_common(1)[0][1] == 2 and freq.most_common(2)[1][1] == 2:
            return 2
        if freq.most_common(1)[0][1] == 2 and freq['J'] == 1:
            return 2
        if freq.most_common(1)[0][1] + freq['J'] == 2:
            return 1
        return 0

    def __lt__(self, other):
        ranks = 'J23456789TQKA'
        if self.type < other.type:
            return True
        elif self.type > other.type:
            return False
        elif self.type == other.type:
            for x, y in zip(self.cards, other.cards):
                if ranks.index(x) < ranks.index(y):
                    return True
                elif ranks.index(x) > ranks.index(y):
                    return False


@timer_func
def day07(filepath, part2=False):
    with open(filepath) as fin:
        lines = [line.strip() for line in fin.readlines()]

    if not part2:
        hands = [Hand(line[:5], int(line[6::])) for line in lines]
    else:
        hands = [Hand2(line[:5], int(line[6::])) for line in lines]

    hands.sort()
    for hand in hands:
        print(hand)
    return sum([(i+1)*h.bid for i, h in enumerate(hands)])


def main():
    assert day07('test07') == 6440
    print(f"Part 1: {day07('input07')}")

    assert day07('test07', True) == 5905
    print(f"Part 2: {day07('input07', True)}")


if __name__ == '__main__':
    main()
