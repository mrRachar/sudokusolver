from typing import Iterable
from grid import Box, BoxGrid, Coordinate


class SudokuSolver:
    def __init__(self, grid):
        self.grid: BoxGrid = grid

    def solve(self):
        previous_grid = self.grid.deep_copy()
        while not self.grid.check_complete():
            if self.grid == previous_grid:
                raise SystemExit("No Change, so lets leave be")
            # Array meaning OrderedIterable, `arrays` is all rows, columns or blocks
            for arrays in self.grid.all_arrays:
                # `array` is a row, column or block
                for array in arrays:
                    for box in array:
                        self.handle_box(box, BoxGrid.box_values(array))

    def update_possible_values(self, coords: Coordinate):
        for array in self.grid.get_containing_arrays(coords):
            for box in array:
                self.handle_box(box, BoxGrid.box_values(array))

    def handle_box(self, box, other_values):
        if box.is_filled:
            return
        elif len(box.possible_values) == 1:
            box.finalise()
            self.update_possible_values(box.coords)
        else:
            # Shallow-copy the set of possible values to not affect the looping as items are removed
            for possible_value in set(box.possible_values):
                # Okay, as only ints are possible_values, and None is default value
                if possible_value in other_values:
                    box.possible_values.remove(possible_value)


example = BoxGrid([[Box(8, set(), coords=(0, 0)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(0, 1)), Box(7, set(), coords=(0, 2)), Box(2, set(), coords=(0, 3)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(0, 4)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(0, 5)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(0, 6)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(0, 7)), Box(5, set(), coords=(0, 8))], [Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(1, 0)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(1, 1)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(1, 2)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(1, 3)), Box(6, set(), coords=(1, 4)), Box(7, set(), coords=(1, 5)), Box(2, set(), coords=(1, 6)), Box(3, set(), coords=(1, 7)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(1, 8))], [Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(2, 0)), Box(9, set(), coords=(2, 1)), Box(2, set(), coords=(2, 2)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(2, 3)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(2, 4)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(2, 5)), Box(7, set(), coords=(2, 6)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(2, 7)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(2, 8))], [Box(9, set(), coords=(3, 0)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(3, 1)), Box(1, set(), coords=(3, 2)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(3, 3)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(3, 4)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(3, 5)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(3, 6)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(3, 7)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(3, 8))], [Box(3, set(), coords=(4, 0)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(4, 1)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(4, 2)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(4, 3)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(4, 4)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(4, 5)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(4, 6)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(4, 7)), Box(6, set(), coords=(4, 8))], [Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(5, 0)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(5, 1)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(5, 2)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(5, 3)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(5, 4)), Box(6, set(), coords=(5, 5)), Box(8, set(), coords=(5, 6)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(5, 7)), Box(2, set(), coords=(5, 8))], [Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(6, 0)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(6, 1)), Box(9, set(), coords=(6, 2)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(6, 3)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(6, 4)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(6, 5)), Box(4, set(), coords=(6, 6)), Box(5, set(), coords=(6, 7)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(6, 8))], [Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(7, 0)), Box(4, set(), coords=(7, 1)), Box(6, set(), coords=(7, 2)), Box(9, set(), coords=(7, 3)), Box(7, set(), coords=(7, 4)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(7, 5)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(7, 6)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(7, 7)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(7, 8))], [Box(2, set(), coords=(8, 0)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(8, 1)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(8, 2)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(8, 3)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(8, 4)), Box(5, set(), coords=(8, 5)), Box(6, set(), coords=(8, 6)), Box(None, {1, 2, 3, 4, 5, 6, 7, 8, 9}, coords=(8, 7)), Box(8, set(), coords=(8, 8))]], block_height=3, block_width=3)

if __name__ == '__main__':
    s = SudokuSolver(example)
    try:
        s.solve()
    except:
        pass
    print(example)