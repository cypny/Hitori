import copy
import time
from functools import wraps

import cell
import parser as pars
import paterns as pat
from decorators import measure_time


@measure_time
def solve(field):
    rez = []
    field = pat.run_patterns(field)
    steak = []
    if is_solve(field):
        rez.append(field)
    steak.append(field)
    visited = []
    while len(steak) != 0:
        field = steak.pop()
        if field in visited:
            continue
        visited.append(cell.field_to_string(field))
        new_fields = get_all_step(field)
        for new_field in new_fields:
            if cell.field_to_string(new_field) in visited:
                continue
            visited.append(cell.field_to_string(new_field))
            if is_solve(new_field):
                rez.append(new_field)
            else:
                steak.append(new_field)
    return rez

def get_all_repeats(field):
    rez = set()
    for x in range(len(field)):
        line_y = {}
        line_x = {}
        for y in range(len(field[0])):
            if field[x][y].value != 0:
                if field[x][y].value in line_y.keys():
                    rez.add(line_y[field[x][y].value])
                    rez.add((x, y))
                line_y[field[x][y].value] = (x, y)
            if field[y][x].value != 0:
                if field[y][x].value in line_x.keys():
                    rez.add(line_x[field[y][x].value])
                    rez.add((y, x))
                line_x[field[y][x].value] = (y, x)
    return rez

def white_have_way(field):
    steak = []
    if field[0][0].is_black:
        steak.append((0, 1))
    else:
        steak.append((0, 0))
    visited = []
    while len(steak) != 0:
        point = steak.pop()
        visited.append(point)
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if (abs(dx) + abs(dy) == 1
                        and cell.argument_correct(point[0] + dx, len(field) - 1)
                        and cell.argument_correct(point[1] + dy, len(field[0]) - 1)
                        and not field[point[0] + dx][point[1] + dy].is_black):
                    if not ((point[0] + dx, point[1] + dy) in visited):
                        steak.append((point[0] + dx, point[1] + dy))
    for x in range(len(field)):
        for y in range(len(field[0]) - 1):
            if field[x][y].is_black:
                continue
            if not ((x, y) in visited):
                return False
    return True


def is_solve(field):
    return len(get_all_repeats(field)) == 0 and white_have_way(field)

def get_all_step(field):
    rez = []
    new_field = copy.deepcopy(field)
    points = get_all_repeats(field)
    for point in points:
        x, y = point[0], point[1]
        if not field[x][y].is_white:
            cell.set_black(new_field, x, y)
            rez.append(new_field)
            new_field = copy.deepcopy(field)
    return rez


if __name__ == "__main__":
    field = pars.get_field_by_console()
    fields = solve(field)
    for i in fields:
        pars.write_field(i)
