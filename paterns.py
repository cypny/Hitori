import numpy

import cell
import parser as par
from decorators import measure_time


@measure_time
def run_patterns(field):
    for x in range(len(field)):
        for y in range(len(field[0])):
            if not field[x][y].is_black and not field[x][y].is_white:
                run_all_grey_patern(field, x, y)
    return field


def run_all_grey_patern(field, x, y):
    patern_two_equal_nearby(field, x, y)
    patern_three_equal_nearby(field, x, y)
    patern_three_equal(field, x, y)


def patern_two_equal_nearby(field, x, y):
    if not (cell.argument_correct(x + 2, len(field) - 1)):
        return
    if field[x][y].value == field[x + 2][y].value:
        cell.set_white(field, x + 1, y)
    if not (cell.argument_correct(y + 2, len(field) - 1)):
        return
    if field[x][y].value == field[x][y + 2].value:
        cell.set_white(field, x, y + 1)


def patern_three_equal_nearby(field, x, y):
    if not (cell.argument_correct(x + 2, len(field) - 1)):
        return
    if field[x][y].value == field[x + 2][y].value and field[x][y].value == field[x + 1][y].value:
        cell.set_black(field, x, y)
        cell.set_black(field, x + 2, y)
    if not (cell.argument_correct(y + 2, len(field) - 1)):
        return
    if field[x][y].value == field[x][y + 2].value and field[x][y].value == field[x][y + 1].value:
        cell.set_black(field, x, y)
        cell.set_black(field, x, y + 2)


def patern_three_equal(field, x, y):
    if not (cell.argument_correct(x + 2, len(field) - 1)):
        return
    if field[x][y].value == field[x + 1][y].value:
        for dx in range(3, len(field) - x):
            if field[x][y].value == field[dx + x][y].value:
                cell.set_black(field, dx + x, y)
    if not (cell.argument_correct(y + 2, len(field) - 1)):
        return
    if field[x][y].value == field[x][y + 1].value:
        for dy in range(3, len(field) - y):
            if field[x][y].value == field[x][y+dy].value:
                cell.set_black(field,x, y+dy)

