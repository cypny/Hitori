import pytest
import parser as pars
import paterns as pat
import solver as sol
import asyncio

# Для тестов GameField
from solver import GameField


@pytest.mark.parametrize("input_str, expected_output", [
    (
            "3\n1 2 3\n4 5 6\n7 8 9",
            [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    )
])
def test_parser(input_str, expected_output):
    """Проверяет корректность парсинга строки в игровое поле"""
    mass_value = pars.readstr(input_str)
    output = pars.create_gaming_field(mass_value)
    for x in range(len(expected_output)):
        for y in range(len(expected_output[0])):
            assert expected_output[x][y] == output.values[x][y]


@pytest.mark.parametrize("input_str, expected_result", [
    ("3\n1 2 3\n4 5 6\n7 8 9", True),
    ("3\n1 1 1\n2 5 6\n7 8 9", False),
    ("3\n1 2 3\n4 2 6\n7 8 9", False)
])
def test_is_solve(input_str, expected_result):
    """Проверяет, является ли поле решением (через Solver)"""
    field = pars.get_field_by_str(input_str)
    solver = sol.Solver(field)
    result = solver.is_solve()
    assert result == expected_result


def test_is_solve_with_black_cells():
    field_4 = pars.get_field_by_str("3\n1 2 3\n4 5 6\n7 8 9")
    field_4.set_black(0, 1)
    field_4.set_black(1, 0)
    solver1 = sol.Solver(field_4)
    assert solver1.is_solve() == False

    field_5 = pars.get_field_by_str("3\n1 2 3\n4 2 6\n7 8 9")
    field_5.set_black(1, 1)
    solver2 = sol.Solver(field_5)
    assert solver2.is_solve() == True


@pytest.mark.parametrize("input_str, expected_x, expected_y", [
    ("3\n1 2 1\n4 5 6\n7 8 9", 1, 0),
    ("3\n1 2 3\n4 5 6\n1 8 9", 0, 1)
])
def test_patern_two_equal_nearby(input_str, expected_x, expected_y):
    """Проверяет паттерн: две одинаковые цифры рядом"""
    result = pat.run_patterns(pars.get_field_by_str(input_str))
    assert result.is_white(expected_x, expected_y)


@pytest.mark.parametrize("input_str, expected_positions", [
    (
            "3\n1 2 3\n5 5 5\n7 8 9",
            [(0, 1), (2, 1)]
    ),
    (
            "3\n1 2 3\n1 5 6\n1 8 9",
            [(0, 0), (0, 2)]
    )
])
def test_patern_three_equal_nearby(input_str, expected_positions):
    """Проверяет паттерн: три одинаковые цифры в ряд"""
    result = pat.run_patterns(pars.get_field_by_str(input_str))
    for x, y in expected_positions:
        assert result.is_black(x, y)


@pytest.mark.parametrize("input_str, expected_x, expected_y", [
    ("4\n1 2 3 4\n5 5 3 5\n7 8 9 5\n1 2 3 4", 3, 1),
    ("4\n1 2 3 4\n1 10 3 5\n7 8 9 5\n1 2 3 4", 0, 3)
])
def test_patern_three_equal(input_str, expected_x, expected_y):
    """Проверяет паттерн: три одинаковые цифры в разных конфигурациях"""
    result = pat.run_patterns(pars.get_field_by_str(input_str))
    assert result.is_black(expected_x, expected_y)


def test_white_have_way():
    """Проверяет связность белых ячеек"""
    field = pars.get_field_by_str("3\n1 2 3\n4 5 6\n7 8 9")
    solver = sol.Solver(field)
    assert solver.white_have_way() == True

    # Блокируем связность
    field.set_black(1, 0)
    field.set_black(0, 1)
    solver1 = sol.Solver(field)
    assert solver1.white_have_way() == False


def test_get_all_repeats():
    """Проверяет, что get_all_repeats возвращает уникальные позиции"""
    field = pars.get_field_by_str("3\n1 2 1\n4 5 6\n7 8 9")
    solver = sol.Solver()
    solver.current_field = field

    repeats = list(solver._get_all_repeats())
    assert len(repeats) == 2


@pytest.mark.parametrize("input_str, expected_blacks", [
    (
            "5\n2 5 2 1 2\n5 2 4 4 2\n4 2 1 5 3\n5 4 2 2 5\n2 3 5 4 2",
            [
                (0, 0), (4, 0),
                (1, 1), (3, 1),
                (0, 3), (2, 3),
                (4, 4)
            ]
    ),
    (
            "5\n4 2 3 2 4\n2 5 3 3 4\n1 3 5 2 2\n1 2 2 1 3\n3 4 2 5 2",
            [
                (1, 0), (4, 0),
                (2, 1),
                (3, 2),
                (0, 3), (2, 3),
                (4, 4)
            ]
    ),
    (
            "5\n3 3 5 1 3\n1 3 4 2 5\n1 5 2 3 3\n2 4 3 4 1\n3 1 2 4 3",
            [
                (1, 0), (4, 0),
                (0, 2), (2, 2),
                (4, 2),
                (3, 3),
                (0, 4)
            ]
    )
])
def test_real_in_solved(input_str, expected_blacks):
    solver = sol.Solver()
    field = pars.get_field_by_str(input_str)
    solutions = asyncio.run(solver.solve(field))

    found_solution = False
    for solution in solutions:
        current_blacks = []
        for x in range(solution.field_len):
            for y in range(solution.field_len):
                if solution.is_black(x, y):
                    current_blacks.append((x, y))

        if sorted(current_blacks) == sorted(expected_blacks):
            found_solution = True
            break

    assert found_solution