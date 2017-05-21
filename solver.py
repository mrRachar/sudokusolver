from typing import List, Set, Optional, Tuple

from grid import Box, BoxGrid, Coordinate

class UnsolvableException(ValueError): pass

class SudokuSolver:
    def __init__(self, grid):
        self.grid: BoxGrid = grid

    def solve(self):
        previous_grid = None
        pre_previous_grid, previous_grid = previous_grid, self.grid.deep_copy()
        while not self.grid.check_complete():
            print("Restart process")
            if pre_previous_grid == self.grid == previous_grid:
                raise SystemExit("No Change, so lets leave be")
            # Array meaning OrderedIterable, `arrays` is all rows, columns or blocks
            for arrays in self.grid.all_arrays:
                # `array` is a row, column or block
                for array in arrays:
                    for box in array:
                        self.handle_box(box, array)

    def update_possible_values(self, coords: Coordinate):
        for array in self.grid.get_containing_arrays(coords):
            for box in array:
                self.handle_box(box, array)

    def handle_box(self, box, array):
        if box.is_filled:
            return

        # Remove any impossible values and finalise if necessary
        box.possible_values -= set(BoxGrid.box_values(array))
        if len(box.possible_values) == 1:
            box.finalise()
            # If finalised, we can remove possible values from nearby items, and actually just handle the corresponding arrays
            self.update_possible_values(box.coords)
            return

        for heuristic in (self.uniquetobox_heuristic, self.smallsamegrouping_heuristic, self.intersectinggrouping_heuristic):
            r = heuristic(box, array.copy())
            if r:
                box.value = r
                # If finalised, we can remove possible values from nearby items, and actually just handle the corresponding arrays
                self.update_possible_values(box.coords)
                break
            else:
                # Clear things up by doing quick finalisations without starting further recursive calls
                for b in array:
                    if len(b.possible_values) == 1:
                        b.finalise()

    def uniquetobox_heuristic(self, box: Box, array: List[Box]):
        """This heuristic sees if there are any values which are unique to the box within the array

        Also know as heuristic_a
        """
        # Values which only this box has in the array
        uniquetobox_values = box.possible_values - {possibility for other in array for possibility in other.possible_values}
        result, *rest = uniquetobox_values or {None}
        if rest:
            raise UnsolvableException(
                f"Could not solve due to box at {box.coords} being the only box available to hold {','.join(uniquetobox_values)}"
            )
        return result

    def smallsamegrouping_heuristic(self, box: Box, array: List[Box]):
        """This heurisitc sees if there any groups of boxes with the same possible values

        They must have the same possible values, and be small (i.e. < n in a n*n grid) for it to really work.
        It removes these possible values from any boxes not found in this group

        Also know as heuristic_b
        """
        # As this heuristic only deals with possible values, remove any filled boxes
        array = [b for b in array if not b.is_filled]
        # True == 1 so this should give the number of true occurrences
        count = sum(box.possible_values == b.possible_values for b in array)
        # If there is the same number of boxes with only these possible values as there are possible values, only these boxes can have these values,
        #  and any other boxes must have one of their other values
        if count == len(box.possible_values):
            for b in array:
                if box.possible_values != b.possible_values and box.possible_values & b.possible_values:
                    b.possible_values -= box.possible_values
                elif b.possible_values < box.possible_values:
                    raise UnsolvableException(f"Could not solved as too many boxes ({count}) must contain too few values ({box.possible_values}), "
                                              f"and one even a subset of that ({b.possible_values}), in array {array}")

        elif count > len(box.possible_values):
            raise UnsolvableException(f"Could not solved as too many boxes ({count}) must contain too few values ({box.possible_values}), in"
                                      f"array {array}")

    def intersectinggrouping_heuristic(self, box: Box, array: List[Box]):
        def inner(boxes: List[Box], possible_value_set: Set[int], remaining: List[Box]) -> Optional[Tuple[List[Box], Set[int]]]:
            #boxes_possible_values = reduce(lambda a, b: a & b, (b.possible_values for b in boxes))
            for other in sorted(remaining, key=lambda x: len(x.possible_values)):
                if other.possible_values & possible_value_set:
                    extended_pvs = other.possible_values | possible_value_set
                    if len(extended_pvs) == len(boxes) + 1:
                        return (boxes + [other], extended_pvs)
                    elif len(extended_pvs) < len(boxes) + 1:
                        raise UnsolvableException(f"There is a suggestion that too few values ({extended_pvs}) must fit in too many boxes, "
                                                  f"{boxes + [other]}")
                    # If next time we'll only be dealing with one
                    if len(remaining) <= 2:
                        # Don't bother
                        continue
                    remaining = remaining.copy()
                    remaining.remove(other)
                    r = inner(boxes + [other], extended_pvs, remaining)
                    if isinstance(r, tuple):
                        return r

        # This handles `box` separately, and as with h_b, only deals with possible values, so remove any filled boxes
        array = [b for b in array if not b.is_filled and b is not box]
        r = inner([box], box.possible_values, array)
        if isinstance(r, tuple):
            boxes, possible_value_set = r
            #print('Result!', boxes, possible_value_set)
            for b in array:
                if b not in boxes and possible_value_set & b.possible_values:
                    print('Removing', boxes, possible_value_set, b)
                    b.possible_values -= possible_value_set

