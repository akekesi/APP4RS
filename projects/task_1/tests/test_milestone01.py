import unittest

from task_1.main import main
from task_1.milestone01 import milestone01_tasks
from task_1.milestone01_task_1_3 import milestone01_task_1_3
from task_1.milestone01_task_1_4 import milestone01_task_1_4, milestone01_task_1_4_1, milestone01_task_1_4_2, milestone01_task_1_4_3
from task_1.milestone01_task_1_5 import milestone01_task_1_5, milestone01_task_1_5_1, milestone01_task_1_5_2
from task_1.milestone01_task_1_6 import milestone01_task_1_6


class TestMilestone01(unittest.TestCase):
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

    def test_main(self):
        """
        """
        main()
        self.assertTrue(True)

    def test_milestone01(self):
        """
        """
        milestone01_tasks()
        self.assertTrue(True)

    def test_milestone_task_1_3(self):
        """
        """
        milestone01_task_1_3()
        self.assertTrue(True)

    def test_milestone_task_1_4(self):
        """
        """
        milestone01_task_1_4()
        self.assertTrue(True)

    def test_milestone_task_1_4_1(self):
        """
        """
        milestone01_task_1_4_1()
        self.assertTrue(True)

    def test_milestone_task_1_4_2(self):
        """
        """
        milestone01_task_1_4_2()
        self.assertTrue(True)

    def test_milestone_task_1_4_3(self):
        """
        """
        milestone01_task_1_4_3()
        self.assertTrue(True)

    def test_milestone_task_1_5(self):
        """
        """
        milestone01_task_1_5()
        self.assertTrue(True)

    def test_milestone_task_1_5_1(self):
        """
        """
        milestone01_task_1_5_1()
        self.assertTrue(True)

    def test_milestone_task_1_5_2(self):
        """
        """
        milestone01_task_1_5_2()
        self.assertTrue(True)

    def test_milestone_task_1_6(self):
        """
        """
        milestone01_task_1_6()
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
