import unittest

import cell
import parser as pars
import paterns as pat
import solver as sol


class Tests(unittest.TestCase):
    def test_parser(self):
        mass_value = pars.readstr("3\n1 2 3\n4 5 6\n7 8 9")
        output = pars.create_gaming_field(mass_value)
        answer = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
        self.assertEqual(answer, mass_value)
        for x in range(len(answer)):
            for y in range(len(answer[0])):
                self.assertEqual(answer[x][y], output[x][y].value)

    def test_is_solve(self):
        result_1 = sol.is_solve(pars.get_field_by_str("3\n1 2 3\n4 5 6\n7 8 9"))
        result_2 = sol.is_solve(pars.get_field_by_str("3\n1 1 1\n2 5 6\n7 8 9"))
        result_3 = sol.is_solve(pars.get_field_by_str("3\n1 2 3\n4 2 6\n7 8 9"))
        field_4 = pars.get_field_by_str("3\n1 2 3\n4 5 6\n7 8 9")
        cell.set_black(field_4, 0, 1)
        cell.set_black(field_4, 1, 0)
        result_4 = sol.is_solve(field_4)
        self.assertEqual(result_1, True)
        self.assertEqual(result_2, False)
        self.assertEqual(result_3, False)
        self.assertEqual(result_4, False)

    def test_patern_two_equal_nearby(self):
        result_1 = pat.run_patterns(pars.get_field_by_str("3\n1 2 3\n5 8 5\n7 8 9"))
        result_2 = pat.run_patterns(pars.get_field_by_str("3\n1 2 3\n3 5 6\n1 8 9"))
        self.assertEqual(result_1[1][1].is_white, True)
        self.assertEqual(result_1[0][0].is_white, False)
        self.assertEqual(result_2[0][1].is_white, True)
        self.assertEqual(result_1[0][0].is_white, False)

    def test_patern_three_equal_nearby(self):
        result_1 = pat.run_patterns(pars.get_field_by_str("3\n1 2 3\n5 5 5\n7 8 9"))
        result_2 = pat.run_patterns(pars.get_field_by_str("3\n1 2 3\n1 5 6\n1 8 9"))
        self.assertEqual(result_1[0][1].is_black, True)
        self.assertEqual(result_1[2][1].is_black, True)
        self.assertEqual(result_2[0][0].is_black, True)
        self.assertEqual(result_2[0][2].is_black, True)

    def test_patern_three_equal(self):
        result_1 = pat.run_patterns(pars.get_field_by_str("4\n1 2 3 4\n5 5 3 5\n7 8 9 5\n1 2 3 4"))
        result_2 = pat.run_patterns(pars.get_field_by_str("4\n1 2 3 4\n1 10 3 5\n7 8 9 5\n1 2 3 4"))
        self.assertEqual(result_1[3][1].is_black, True)
        self.assertEqual(result_2[0][3].is_black, True)

    def test_white_have_way(self):
        field = pars.get_field_by_str("3\n1 2 3\n4 5 6\n7 8 9")
        field[0][0].is_black = True
        field[1][1].is_black = True
        field[0][2].is_black = True
        self.assertEqual(sol.white_have_way(field), False)
