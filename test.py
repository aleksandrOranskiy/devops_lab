import task
import unittest


class TestTask(unittest.TestCase):

    def setUp(self):
        """Init"""

    def test_correct_input(self):
        self.assertEqual(task.read_line("3 5"), [3, 5])
        self.assertEqual(task.read_line("3  4"), [3, 4])

    def test_incorrect_input(self):
        self.assertRaises(ValueError, task.read_line, "3 a")
        self.assertRaises(ValueError, task.read_line, "3 3a")

    def test_checked_value(self):
        self.assertEqual(task.read_with_check([3, 5, 66]), [3, 5, 66])
        self.assertEqual(task.read_with_check([1, 5, 10 ** 9]),
                         [1, 5, 10 ** 9])

    def test_fail_checked_value(self):
        self.assertRaises(TypeError, task.read_with_check, [3, 'a', 4])
        self.assertEqual(task.read_with_check([0, 5, 9]), 1)
        self.assertEqual(task.read_with_check([1, 5, 10 ** 9 + 1]), 1)

    def test_first_line(self):
        self.assertEqual(task.get_first_line([3, 5]), [3, 5])
        self.assertEqual(task.get_first_line([10 ** 5, 1]), [10 ** 5, 1])
        self.assertEqual(task.get_first_line([1, 10 ** 5]), [1, 10 ** 5])

    def test_fail_first_line(self):
        self.assertRaises(TypeError, task.get_first_line, [3, 'a'])
        self.assertEqual(task.get_first_line([0, 5]), 1)
        self.assertEqual(task.get_first_line([3, 0]), 1)

    def test_result(self):
        self.assertEqual(task.get_result([3, 5, 2], [2, 5], [1, 4], 2),
                         "Resulting happiness is: 2")
        self.assertEqual(task.get_result([3, 5, 2], [2, 5], [1, 3], 2),
                         "Resulting happiness is: 1")
        self.assertEqual(task.get_result([3, 5, 2], [2, 4], [1, 3], 2),
                         "Resulting happiness is: 0")

    def test_fail_result(self):
        self.assertEqual(task.get_result([3, 5, 2], [2, 5], [1, 5], 2), 1)

    def tearDown(self):
        """Finish"""


if __name__ == '__main__':
    unittest.main()
