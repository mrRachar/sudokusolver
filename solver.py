from typing import Iterable
from grid import Box, BoxGrid


class SodokuSolver:
    def solve(self, grid):
        #grid.fill_possible_values()
        while not grid.check_complete():
            # Array here meaning OrderedIterable
            for arrays_of_boxes_f in (grid.get_columns, grid.get_rows, grid.get_blocks):
                arrays: Iterable[Iterable[Box]] = arrays_of_boxes_f()
                for array in arrays:
                    boxes_values = BoxGrid.box_values(array)
                    for box in array:
                        if not box.possible_values:
                            continue
                        elif len(box.possible_values) == 1:
                            box.value = tuple(box.possible_values)[0]
                        else:
                            for possible_value in set(box.possible_values):
                                # Okay, as only ints are possible_values, and None is default value
                                if possible_value in boxes_values:
                                    box.possible_values.remove(possible_value)


example = BoxGrid([[Box(8, set()), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(5, set()), Box(None, {1, 2,
                                                                                                                                            3, 4,
                                                                                                                                        5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(3, set())], [Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(1, set()), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(4, set()), Box(5, set()), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9})], [Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(9, set()), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(8, set()), Box(2, set()), Box(1, set()), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9})], [Box(4, set()), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(9, set())], [Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(3, set()), Box(7, set()), Box(2, set()), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9})], [Box(6, set()), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(2, set())], [Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(4, set()), Box(6, set()), Box(7, set()), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(1, set()), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9})], [Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(5, set()), Box(8, set()), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(9, set()), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9})], [Box(7, set()), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(3, set()), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}), Box(5, set())]], block_height=3, block_width=3)