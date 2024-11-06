# This script is called as the entrypoint on our cluster
# ONLY import libraries in this file that are explicitly listed in the task description
# or are part of the standard library!

from task_1.milestone01 import milestone01_tasks


def main():
    milestone01_tasks()


if __name__ == "__main__":
    main()
