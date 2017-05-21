from solver import *

grid = BoxGrid()

y = 0
while y < 9:
    x = 0
    while x < 9 and y < 9:
        e = input(f'{x, y} >>> ') or 's1'
        if e.isdigit():
            grid[x, y].value = int(e)
        elif e.startswith('s'):
            x += int(e.lstrip('s'))
            while x > 8:
                x -= 9
                y += 1
            continue
        else:
            continue
        x += 1
    y += 1

while True:
    try:
        print(eval(input('>>> ')))
    except:
        pass

