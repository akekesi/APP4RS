import unittest

from projects.task_1.task_1.milestone01_task_1_3 import milestone01_task_1_3


class TestConnect4(unittest.TestCase):
    """
    """

    def setUp(self) -> None:
        """
        This method is called before each test.
        """
        pass

    def tearDown(self) -> None:
        """
        This method is called after each test.
        """
        pass

    def test_main_sub(self):
        """
        """
        milestone01_task_1_3()
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
