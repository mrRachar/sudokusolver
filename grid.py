from typing import Set, List, TypeVar, Tuple, Union, Iterable


class Box:
    _value: int
    possible_values: Set[int]

    def __init__(self, value: int=None, possible_values: Set[int]=None):
        self.possible_values = possible_values or {n+1 for n in range(9)}
        self._value = value

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
        return f"{self.__class__.__name__}({self.value}, {self.possible_values})"


Column = List[Box]
Row = List[Box]
Coordinate = Tuple[int, int]
Position = Union[Coordinate, int]

class BoxGrid:
    block_height: int = 3
    block_width: int = 3
    columns: List[Column]

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            base, = args
            if isinstance(base, BoxGrid):
                self.columns = base.columns.copy()
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

            self.columns = [[Box() for _ in range(height)] for _ in range(width)]

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

    def get_containing_arrays(self, position: Coordinate):
        x, y = position
        blocks_tall = (self.height // self.block_height) + 1
        block_n = (blocks_tall * (x // self.block_width)) + (y//self.block_height)
        block = self.get_blocks()[block_n]
        return (self.rows[y],
                self.columns[x],
                block)

    def update_possible_values(self, position: Coordinate=None):
        if None:
            self.update_all_possible_values()
        x, y = position
        for array in self.get_containing_arrays(position):
            boxes_values = self.box_values(array)
            for box in array:
                if not box.possible_values:
                    continue
                elif len(box.possible_values) == 1:
                    box.value = tuple(box.possible_values)[0]
                for possible_value in set(box.possible_values):
                    # Okay, as only ints are possible_values, and None is default value
                    if possible_value in boxes_values:
                        box.possible_values.remove(possible_value)

    @staticmethod
    def box_values(iter_of_boxes: Iterable[Box]):
        return iter_of_boxes.__class__(x.value for x in iter_of_boxes)

    def check_complete(self):
        for row in self.rows:
            for box in row:
                if box.possible_values:
                    return False
        return True
