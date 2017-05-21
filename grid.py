from typing import Set, List, Tuple, Union, Iterable, Callable, Iterator, Optional
import math as maths


Coordinate = Tuple[int, int]
Position = Union[Coordinate, int]

class BoxNotSolvedException(Exception): pass

class Box:
    _value: int
    possible_values: Set[int]
    coords: Optional[Coordinate]

    def __init__(self, value: int=None, possible_values: Set[int]=None, *, coords: Coordinate=None):
        self.possible_values = possible_values if possible_values is not None else {n+1 for n in range(9)}
        self._value = value
        self.coords = coords

    def clear_possible_values(self):
        self.possible_values &= set()

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, n: int):
        assert n in self.possible_values
        self.clear_possible_values()
        self._value = n

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value}, {self.possible_values}, coords={self.coords})"

    def finalise(self) -> int:
        """Make the only remaining possible value the value"""
        assert len(self.possible_values) == 1, BoxNotSolvedException
        self.value, = self.possible_values
        return self.value

    @property
    def is_filled(self):
        return not not self.value

    def copy(self):
        return self.__class__(self._value, set(self.possible_values), coords=self.coords)

    def __eq__(self, other):
        return isinstance(other, Box) and self.value == other.value and self.possible_values == other.possible_values


Column = List[Box]
Row = List[Box]

class BoxGrid:
    block_height: int = 3
    block_width: int = 3
    columns: List[Column]

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            base, = args
            if isinstance(base, BoxGrid):
                base = base.deep_copy()
                self.columns = base.columns
                self.block_height = base.block_height
                self.block_width = base.block_width
            elif isinstance(base, Iterable):
                self.columns = []
                for column in base:
                    assert isinstance(column, Iterable), "Given iterable must be Iterable[Iterable]"
                    self.columns.append(list(column))
        else:
            if len(args) == 2:
                height = args[0]
                width = args[1]
            elif len(args):
                raise ValueError(f"{len(args)} arguments is not supported by Grid")
            else:
                height = 9
                width = 9

            height = kwargs.get('height', height)
            width = kwargs.get('width', width)

            self.columns = [[Box(coords=(x, y)) for y in range(height)] for x in range(width)]

        self.block_height = kwargs.get('block_height', self.block_height)
        self.block_width = kwargs.get('block_width', self.block_width)

    @property
    def height(self) -> int:
        return len(self.columns[0])

    @property
    def width(self) -> int:
        return len(self.columns)

    @property
    def rows(self) -> List[Row]:
        rows = [[] for _ in range(self.height)]
        for column in self.columns:
            for n, value in enumerate(column):
                rows[n].append(value)
        return rows

    def get_rows(self) -> List[Row]:
        return self.rows

    def get_columns(self) -> List[Column]:
        return self.columns

    def get_blocks(self) -> List[List[Box]]:
        blocks = []
        block_n = 0
        for col_n, column in enumerate(self.columns):
            for row_n, box in enumerate(column):
                try:
                    blocks[block_n].append(box)
                except IndexError:
                    blocks.append([box])
                if not (row_n + 1) % self.block_height:
                    block_n += 1
            if not (col_n + 1) % self.block_width:
                pass #block_n += 1
            else:
                block_n -= self.height // self.block_height
        return blocks

    def __str__(self):
        build_str = ""
        for row in self.rows:
            build_str += '\t'.join(str(box.value or '-') for box in row) + '\n'
        return build_str

    def __repr__(self):
        return f"{self.__class__.__name__}({self.columns}, block_height={self.block_height}, block_width={self.block_width})"

    def __getitem__(self, position: Position):
        if isinstance(position, int):
            return self.columns[position]
        elif isinstance(position, tuple):
            return self.columns[position[0]][position[1]]

    def __setitem__(self, position: Position, value):
        if isinstance(position, int):
            self.columns[position] = value
        elif isinstance(position, tuple):
            self.columns[position[0]][position[1]] = value

    def get_all_arrays(self) -> List[List[Box]]:
        """Return all the 'arrays' of boxes that can be made out of the BoxGrid

        It will return the columns, then the rows, and then the boxes
        """
        for array_f in (self.get_columns, self.get_rows, self.get_blocks):
            yield array_f()

    @property
    def all_arrays(self) -> Iterable[List[List[Box]]]:
        """All the 'arrays' of boxes that can be made out of the BoxGrid

        First the columns, then the rows, and then the boxes
        """
        yield from self.get_all_arrays()

    def get_containing_array_functions(self, position: Coordinate) -> Iterator[Callable[[], List[Box]]]:
        x, y = position
        blocks_tall = maths.ceil(self.height / self.block_height)
        block_n = (blocks_tall * (x // self.block_width)) + (y//self.block_height)
        yield from (lambda: self.rows[y],
                    lambda: self.columns[x],
                    lambda: self.get_blocks()[block_n]
                    )

    def get_containing_arrays(self, position: Coordinate):
        for array_f in self.get_containing_array_functions(position):
            yield array_f()

    @staticmethod
    def box_values(iter_of_boxes: Iterable[Box]) -> Iterable[Optional[int]]:
        return iter_of_boxes.__class__(x.value for x in iter_of_boxes)

    def update_boxes_internal_coordinates(self):
        for x, column in enumerate(self.columns):
            for y, box in enumerate(column):
                box.coords = (x, y)

    def deep_copy(self):
        return BoxGrid([[box.copy() for box in column] for column in self.columns])

    def check_complete(self):
        for row in self.rows:
            for box in row:
                if box.possible_values:
                    return False
        return True

    def __eq__(self, other):
        if not isinstance(other, BoxGrid):
            return False
        for col, othercol in zip(self.columns, other.columns):
            for box, otherbox in zip(col, othercol):
                if box != otherbox:
                    return False
        return True

