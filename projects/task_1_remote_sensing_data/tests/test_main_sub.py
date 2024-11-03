import unittest

from task_1_remote_sensing_data.main_sub import main_sub


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
        self.assertTrue(main_sub())


if __name__ == "__main__":
    unittest.main()
