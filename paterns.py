def run_patterns(game_field):
    for x in range(game_field.field_len):
        for y in range(game_field.field_len):
            if not game_field.is_black(x, y) and not game_field.is_white(x, y):
                run_all_grey_patern(game_field, x, y)
    return game_field


def run_all_grey_patern(game_field, x, y):
    patern_two_equal_nearby(game_field, x, y)
    patern_three_equal_nearby(game_field, x, y)
    patern_three_equal(game_field, x, y)


def patern_two_equal_nearby(game_field, x, y):
    if not game_field.argument_correct(x + 2):
        return
    if game_field.values[x][y] == game_field.values[x + 2][y]:
        game_field.set_white(x + 1, y)
    if not game_field.argument_correct(y + 2):
        return
    if game_field.values[x][y] == game_field.values[x][y + 2]:
        game_field.set_white(x, y + 1)


def patern_three_equal_nearby(game_field, x, y):
    if not game_field.argument_correct(x + 2):
        return
    if (game_field.values[x][y] == game_field.values[x + 2][y] and
            game_field.values[x][y] == game_field.values[x + 1][y]):
        game_field.set_black(x, y)
        game_field.set_black(x + 2, y)
    if not game_field.argument_correct(y + 2):
        return
    if (game_field.values[x][y] == game_field.values[x][y + 2] and
            game_field.values[x][y] == game_field.values[x][y + 1]):
        game_field.set_black(x, y)
        game_field.set_black(x, y + 2)


def patern_three_equal(game_field, x, y):
    if not game_field.argument_correct(x + 2):
        return
    if game_field.values[x][y] == game_field.values[x + 1][y]:
        for dx in range(3, game_field.field_len - x):
            if game_field.values[x][y] == game_field.values[dx + x][y]:
                game_field.set_black(dx + x, y)
    if not game_field.argument_correct(y + 2):
        return
    if game_field.values[x][y] == game_field.values[x][y + 1]:
        for dy in range(3, game_field.field_len - y):
            if game_field.values[x][y] == game_field.values[x][y + dy]:
                game_field.set_black(x, y + dy)
