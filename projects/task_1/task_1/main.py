import time
from task_1.milestone01 import milestone01_tasks


def main():
    # this function MUST execute the code for all tasks 
    # and print the solutions in the required format.
    milestone01_tasks()


if __name__ == "__main__":
    time_start = time.time()
    main()
    time_all_sec = time.time() - time_start
    time_all_min = time_all_sec / 60
    print(f"{time_all_min:.01f}")
