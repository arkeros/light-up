# coding=utf-8
from itertools import product
from operator import methodcaller

__author__ = 'rarquegi7.alumnes'


def vector_sum(a, b):
    return tuple(map(sum, zip(a, b)))

v_sum = vector_sum


def parse(filename):
    rosetta = {
        '0': 0,
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        'X': Cell.BLOCK,
    }
    with open(filename) as f:
        node = Node(7)
        for row, line in enumerate(f.readlines()):
            for col, c in enumerate(line[:-1]):
                if c in rosetta.keys():
                    node[(row, col)].value = rosetta[c]
        return node


class Cell(object):
    DIRECTIONS = [methodcaller('top'), methodcaller('right'), methodcaller('down'), methodcaller('left')]
    EMPTY = None
    BLOCK = 5
    BULB = 6
    NOT_BULB = 7

    rosetta = {
        EMPTY: ' ',
        0: '0',
        1: '1',
        2: '2',
        3: '3',
        4: '4',
        BLOCK: '#',
        BULB: 'X',
        NOT_BULB: '·'
    }

    def __init__(self, node, row, column, value=EMPTY):
        self.node = node
        self.row = row
        self.column = column
        self.value = value

    def key(self):
        return tuple([self.row, self.column])

    def top(self):
        """:rtype: Cell"""
        return self.node[v_sum(self.key(), (-1, 0))]

    def right(self):
        """:rtype: Cell"""
        return self.node[v_sum(self.key(), (0, +1))]

    def down(self):
        """:rtype: Cell"""
        return self.node[v_sum(self.key(), (+1, 0))]

    def left(self):
        """:rtype: Cell"""
        return self.node[v_sum(self.key(), (0, -1))]

    def watching(self):
        for direction in Cell.DIRECTIONS:
            try:
                cell = direction(self)
                while not (cell is None or cell.is_block()):
                    yield cell
                    cell = direction(cell)
            except KeyError:
                pass

    def neighbours(self):
        for direction in Cell.DIRECTIONS:
            try:
                cell = direction(self)
                if not (cell is None):
                    yield cell
            except KeyError:
                pass

    def is_valid(self):
        if self.is_empty():
            return True
        elif self.value is Cell.BLOCK:
            return True
        elif self.value in [0, 1, 2, 3, 4]:
            bulbs = sum(1 for cell in self.neighbours() if cell.is_bulb())
            not_bulbs = sum(1 for cell in self.neighbours() if cell.is_not_bulb())
            return bulbs <= self.value <= 4 - not_bulbs
        elif self.value is Cell.BULB:
            return not any(cell.is_bulb() for cell in self.watching())

    def is_block(self):
        """:rtype: bool"""
        return 0 <= self.value <= 5

    def is_bulb(self):
        """:rtype: bool"""
        return self.value is Cell.BULB

    def is_not_bulb(self):
        """:rtype: bool"""
        return self.value is Cell.NOT_BULB

    def is_empty(self):
        """:rtype: bool"""
        return self.value is Cell.EMPTY

    def __str__(self):
        return Cell.rosetta[self.value]

    def __repr__(self):
        return "({0},{1})".format(self.row, self.column)


class Node(dict):
    OFFSETS = tuple([(-1, 0), (0, 1), (1, 0), (0, -1)])

    def __init__(self, size):
        self.update(
            list((k, Cell(self, *k)) for k in product(range(size), repeat=2))
        )
        self.parent = None
        self.children = list()
        self.size = size

    def empty_cells(self):
        for cell in self.itercells():
            if cell.is_empty():
                yield cell

    def valid(self):
        """:rtype: bool"""
        return all(cell.is_valid() for cell in self.itercells())

    def is_finished(self):
        """:rtype: bool"""
        return not any(True for cell in self.empty_cells())

    def itercells(self):
        return self.itervalues()

    def __str__(self):
        ret = ""
        sizes = range(self.size)
        for row in sizes:
            for col in sizes:
                ret += str(self[(row, col)])
            ret += "\n"
        return ret


def backtracking(node):
    """

    :type node: Node
    """
    print node
    if not node.valid():
        return False
    elif node.is_finished():
        return node
    return any(backtracking(candidate) for candidate in candidates(node))


def candidates(node):
    # TODO reordenar para optimizar candidatos. ahora es fuerza bruta

    for cell in sorted(node.empty_cells(), key=criteria):
        cell.value = Cell.BULB
        yield node
        cell.value = Cell.NOT_BULB
        yield node
        cell.value = Cell.EMPTY


def criteria(cell):
    can_bulb =
    can_not_bulb =
    return 4 - sum(1 for x in cell.neighbours() if x in [0, 1, 2, 3, 4]), sum(1 for x in cell.watching())

def main():
    node = parse("easy.lightup")
    print node, backtracking(node)


main()