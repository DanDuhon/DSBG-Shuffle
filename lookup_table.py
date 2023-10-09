from bisect import bisect_left
from collections.abc import Mapping


class LookupTable(Mapping):
    """
    A lookup table with contiguous ranges of small integers as
    keys. Initialize a table by passing pairs (max, value) as
    arguments. The first range starts at 0, and second and subsequent
    ranges start at the end of the previous range.

    >>> t = LookupTable((10, '0 - 10'), (35, '11 - 35'), (100, '36 - 100'))
    >>> t[10], t[11], t[100]
    ('0 - 10', '11 - 35', '36 - 100')
    >>> t[0]
    Traceback (most recent call last):
      ...
    KeyError: 0
    >>> next(iter(t.items()))
    (1, '0 - 10')
    """

    def __init__(self, *table):
        self.table = sorted(table)
        self.max = self.table[-1][0]

    def __getitem__(self, key):
        key = int(key)
        if not 0 <= key <= self.max:
            return None
        return self.table[bisect_left(self.table, (key,))][1]

    def __iter__(self):
        return iter(range(1, self.max + 1))

    def __len__(self):
        return self.max