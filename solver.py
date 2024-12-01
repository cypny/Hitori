import copy
from decorators import measure_time
import field
import parser as pars
import paterns as pat

@measure_time
def solve(game_field):
    rez = []
    game_field = pat.run_patterns(game_field)
    steak = [game_field]
    visited = set()

    if is_solve(game_field):
        rez.append(game_field)

    while steak:
        current_field = steak.pop()
        new_fields = get_all_step(current_field)
        for new_field in new_fields:
            field_str = new_field.field_to_string()
            if field_str in visited:
                continue
            visited.add(field_str)
            if is_solve(new_field):
                rez.append(new_field)
            else:
                steak.append(new_field)
    return rez

def get_all_repeats(game_field):
    rez = set()
    for x in range(game_field.field_len):
        line_y = {}
        line_x = {}
        for y in range(game_field.field_len):
            if not game_field.is_black(x, y):
                val = game_field.values[x][y]
                if val in line_y:
                    rez.add(line_y[val])
                    rez.add((x, y))
                line_y[val] = (x, y)
            if not game_field.is_black(y, x):
                val = game_field.values[y][x]
                if val in line_x:
                    rez.add(line_x[val])
                    rez.add((y, x))
                line_x[val] = (y, x)
    return rez
def white_have_way(game_field):
    start = (0, 1) if game_field.is_black(0, 0) else (0, 0)
    steak = [start]
    visited = set()

    while steak:
        x, y = steak.pop()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            new_x, new_y = x + dx, y + dy
            if (game_field.argument_correct(new_x) and 
                game_field.argument_correct(new_y) and 
                not game_field.is_black(new_x, new_y)):
                steak.append((new_x, new_y))

    for x in range(game_field.field_len):
        for y in range(game_field.field_len):
            if not game_field.is_black(x, y) and (x, y) not in visited:
                return False
    return True

def is_solve(game_field):
    return len(get_all_repeats(game_field)) == 0 and white_have_way(game_field)

def get_all_step(game_field):
    rez = []
    points = get_all_repeats(game_field)
    for x, y in points:
        if game_field.is_white(x,y):
            continue
        new_field = game_field.copy()
        new_field.set_black(x, y)
        rez.append(new_field)
    return rez

if __name__ == "__main__":
    field = pars.get_field_by_console()
    fields = solve(field)
    for i in fields:
        pars.write_field(i)

