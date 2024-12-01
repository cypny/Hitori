
class cell:
    value = 0
    is_black = False
    is_white = False

    def __init__(self, value):
        self.value = value


def set_white(field, x, y):
    field[x][y].is_white = True


def set_black(field, x, y):
    field[x][y].is_black = True
    field[x][y].value = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if (abs(dx) + abs(dy) == 1
                    and argument_correct(x + dx, len(field) - 1)
                    and argument_correct(y + dy, len(field[0]) - 1)):
                set_white(field, x + dx, y + dy)


def argument_correct(i, max_i):
    if 0 <= i <= max_i:
        return True
    return False


def field_to_string(field):
    rez = []
    for line in field:
        for cell in line:
            if cell.is_black:
                rez.append("1")
            elif cell.is_white:
                rez.append("2")
            else:
                rez.append("0")
    return "".join(rez)
