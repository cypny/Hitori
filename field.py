from enum import Enum


class cell(Enum):
    gray = 0
    black = 1
    white = 2


class solve_field:
    def __init__(self, values):
        self.values = values
        self.field_len = len(values)
        self.cells = [[cell.gray for _ in range(self.field_len)] for _ in range(self.field_len)]

    def set_white(self, x, y):
        self.cells[x][y] = cell.white

    def set_black(self, x, y):
        self.cells[x][y] = cell.black
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if (abs(dx) + abs(dy) == 1
                        and self.argument_correct(x + dx)
                        and self.argument_correct(y + dy)):
                    self.set_white(x + dx, y + dy)

    def argument_correct(self, i):
        return 0 <= i <= self.field_len - 1

    def field_to_string(self):
        rez = []
        for x in range(self.field_len):
            for y in range(self.field_len):
                rez.append(str(self.cells[x][y].value))
        return "".join(rez)

    def is_white(self, x, y):
        return self.cells[x][y].value == cell.white.value

    def is_black(self, x, y):
        return self.cells[x][y].value == cell.black.value

    def copy(self):
        field = solve_field(self.values)
        for x in range(self.field_len):
            for y in range(self.field_len):
                field.cells[x][y] = self.cells[x][y]
        return field
