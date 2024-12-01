import field as fl



def read():
    n = int(input())
    mass = []
    for i in range(n):
        z = map(int, input().split())
        mass.append(list(z))
    mass = convent_x_y(mass)
    return mass


def readstr(input_str):
    lines = input_str.split("\n")
    n = int(lines[0])
    mass = []
    for i in range(n):
        z = map(int, lines[i + 1].split())
        mass.append(list(z))
    mass = convent_x_y(mass)
    return mass


def convent_x_y(mass):
    new_mass = []
    for y in range(len(mass)):
        line = []
        for x in range(len(mass[0])):
            line.append(mass[x][y])
        new_mass.append(line)
    return new_mass


def create_gaming_field(mass):
    rez=fl.solve_field(mass)
    return rez


def write_field(field):
    for y in range(field.field_len):
        for x in range(field.field_len):
            value_to_print=field.values[x][y]
            if field.cells[x][y]==fl.cell.black:
                value_to_print=0
            print(" " + str(value_to_print) + " ", end="")
        print()
    print()


def get_field_by_console():
    mass = read()
    return create_gaming_field(mass)


def get_field_by_str(input_str):
    mass_value = readstr(input_str)
    return create_gaming_field(mass_value)


def get_field_by_gui(input_fields):
    mass = []
    for x in range(len(input_fields)):
        line = []
        for y in range(len(input_fields[0])):
            line.append(input_fields[x][y].get())
        mass.append(line)
    return create_gaming_field(mass)
