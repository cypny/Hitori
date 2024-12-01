import unittest
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
                self.assertEqual(answer[x][y], output.values[x][y])

    def test_is_solve(self):
        result_1 = sol.is_solve(pars.get_field_by_str("3\n1 2 3\n4 5 6\n7 8 9"))
        result_2 = sol.is_solve(pars.get_field_by_str("3\n1 1 1\n2 5 6\n7 8 9"))
        result_3 = sol.is_solve(pars.get_field_by_str("3\n1 2 3\n4 2 6\n7 8 9"))
        field_4 = pars.get_field_by_str("3\n1 2 3\n4 5 6\n7 8 9")
        field_4.set_black(0, 1)
        field_4.set_black(1, 0)
        result_4 = sol.is_solve(field_4)
        self.assertEqual(result_1, True)
        self.assertEqual(result_2, False)
        self.assertEqual(result_3, False)
        self.assertEqual(result_4, False)

    def test_patern_two_equal_nearby(self):
        z=pars.get_field_by_str("3\n1 2 1\n4 5 6\n7 8 9")
        result = pat.run_patterns(z)
        self.assertTrue(result.is_white(1, 0))
        
        result = pat.run_patterns(pars.get_field_by_str("3\n1 2 3\n4 5 6\n1 8 9"))
        self.assertTrue(result.is_white(0, 1))

    def test_patern_three_equal_nearby(self):
        result_1 = pat.run_patterns(pars.get_field_by_str("3\n1 2 3\n5 5 5\n7 8 9"))

        
        result_2 = pat.run_patterns(pars.get_field_by_str("3\n1 2 3\n1 5 6\n1 8 9"))
        self.assertTrue(result_1.is_black(0, 1))
        self.assertTrue(result_1.is_black(2, 1))
        self.assertTrue(result_2.is_black(0, 0))
        self.assertTrue(result_2.is_black(0, 2))

    def test_patern_three_equal(self):
        eaw=pars.get_field_by_str("4\n1 2 3 4\n5 5 3 5\n7 8 9 5\n1 2 3 4")
        result_1 = pat.run_patterns(eaw)
        self.assertTrue(result_1.is_black(3, 1))
        
        result_2 = pat.run_patterns(pars.get_field_by_str("4\n1 2 3 4\n1 10 3 5\n7 8 9 5\n1 2 3 4"))
        self.assertTrue(result_2.is_black(0, 3))

    def test_white_have_way(self):
        game_field = pars.get_field_by_str("3\n1 2 3\n4 5 6\n7 8 9")
        game_field.set_black(0, 0)
        game_field.set_black(1, 1)
        game_field.set_black(0, 2)
        self.assertFalse(sol.white_have_way(game_field))

    def test_get_all_repeats(self):
        game_field = pars.get_field_by_str("3\n1 2 1\n4 5 6\n7 8 9")
        repeats = sol.get_all_repeats(game_field)
        self.assertEqual(len(repeats), 2)


