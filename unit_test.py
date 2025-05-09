from parser import *
from main import *
import pytest


def test_create_gaming_board_by_str_valid():
    test_board = """5
    empty black empty white empty
    black empty black empty black
    empty empty black empty white
    white black empty empty empty
    empty empty black empty empty"""

    board = create_gaming_board_by_str(test_board)
    assert board is not None
    assert board.board_size == 5


def test_create_gaming_board_by_str_invalid():
    test_board = """5
    empty black empty white empty
    black empty black empty black
    empty empty black empty white
    white black invalid empty empty
    empty empty black empty empty"""

    board = create_gaming_board_by_str(test_board)
    assert board is None


@pytest.mark.parametrize("input_str, expected_output", [
    ("5\nblack black black black black\nempty empty empty empty empty\nempty empty empty empty empty\nempty empty empty empty empty\nempty empty empty empty empty", True),
    ("5\nempty black empty empty empty\nempty black empty empty empty\nempty black empty empty empty\nempty black empty empty empty\nempty black empty empty empty", True),
    ("5\nblack empty empty empty empty\nempty black empty empty empty\nempty empty black empty empty\nempty empty empty black empty\nempty empty empty empty black", True),
    ("5\nblack empty empty empty empty\nempty black empty empty empty\nempty empty black empty empty\nempty empty empty black empty\nempty empty empty empty empty", False),
])
def test_check_win_parametrized(input_str, expected_output):
    board = create_gaming_board_by_str(input_str)
    assert board.check_win() == expected_output


@pytest.mark.parametrize("input_board_str, expected_move", [
    ("5\nblack empty empty empty empty\nempty black empty empty empty\nempty empty black empty empty\nempty empty empty black empty\nempty empty empty empty empty", (4, 4)),
    ("5\nblack black empty black black\nempty empty empty empty empty\nempty empty empty empty empty\nempty empty empty empty empty\nempty empty empty empty empty", (2, 2)),
    ("5\n5\nempty empty black empty empty\nempty empty empty black empty\nempty black empty empty empty\nempty black empty empty empty\nempty empty black empty empty", (2,0)),
])
def test_find_win_move_parametrized(input_board_str, expected_move):
    board = create_gaming_board_by_str(input_board_str).board
    bot_easy = easy_bot.easy_bot(Color.WHITE, 5)
    bot_hard = hard_bot.hard_bot(Color.WHITE, 5)
    bot_easy.board = board
    bot_hard.board = board
    assert bot_hard.find_win_move() == expected_move
    assert bot_easy.find_win_move(Color.BLACK) == expected_move




def test_make_move():
    game_1 = game.game(5)
    game_1.make_move(1, 1)
    game_1.make_move(0, 0)
    game_1.make_move(2, 2)
    assert game_1.board[1][1] == Color.BLACK
    assert game_1.board[0][0] == Color.WHITE
    assert game_1.board[2][2] == Color.BLACK