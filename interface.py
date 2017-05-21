from grid import BoxGrid
from solver import SudokuSolver


class SolverInterface:
    welcome_message = """
    -- Welcome to the sudokusolver --
                   -- by Matthew Ross
"""
    instructions = "[H]elp or [S]olve"
    prompt = ">>>"
    success_message = "Puzzle Solved!"
    help_message = """
The main menu allows you to access:
    H help - this helpful guide
    S solve - solve a puzzle

To input a puzzle, just enter the value of
the box it is indicating. If input
something invalid, it will reprompt you.

Input rules:
    "sN" (where N is an integer)
      - Skip N boxes (including the current
        and last)
    "<" - Move back one, and reinput
    "<N" - Move back N and reinput
    "N" - Input n in the current box
    "" - If you input nothing, it will leave
         that box empty, and move on to the
         next box.
"""

    def run(self):
        print(self.welcome_message)
        self.menu()

    def menu(self):
        while True:
            r = input(f"{self.instructions} {self.prompt} ")
            if r.lower() in ('s', 'solve'):
                self.solve()
            elif r.lower() in ('h', 'help'):
                self.help() # Not one of those bad books, though

    def help(self):
        print(self.help_message)

    def input_grid(self):
        grid = BoxGrid()

        y = 0
        while y < 9:
            x = 0
            while x < 9 and y < 9:
                e = input(f'{x+1, y+1} {self.prompt} ') or 's1'
                try:
                    if e.isdigit() and int(e) in grid[x, y].possible_values:
                        try:
                            grid[x, y].value = int(e)
                        except AssertionError:
                            grid[x, y].possible_values = set(range(1, 10))
                            grid[x, y].value = int(e)
                        x += 1
                    elif e.startswith('s'):
                        x += int(e.lstrip('s'))
                        while x > 8:
                            x -= 9
                            y += 1
                            print('---')
                    elif e.startswith('<'):
                        if len(e) == 1:
                            x -= 1
                        else:
                            x -= int(e.lstrip('<'))
                        while x < 0:
                            x += 9
                            y -= 1
                            print('^^^')
                except Exception as e:
                    print(f'Sorry, that didn\'t go to plan! ({e.__class__.__name__})')
            print('---')
            y += 1
        return grid

    def solve(self):
        grid = self.input_grid()
        print(grid)

        solver = SudokuSolver(grid)
        solver.solve()

        print('', self.success_message, grid, sep='\n')
