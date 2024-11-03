# This script is called as the entrypoint on our cluster
# ONLY import libraries in this file that are explicitly listed in the task description
# or are part of the standard library!

import numpy as np
import pandas as pd

from pathlib import Path
from task_1_remote_sensing_data.main_sub import main_sub


def main():
  # this function MUST execute the code for all tasks and print the solutions
  # in the required format.
  print("Hello World from Group01")
  # silly example; used for testing write access
  # on our cluster
  Path("test.txt").write_text("Writing works")
  assert Path("untracked-files/milestone01/metadata.parquet").exists()

  # main of Group01
  main_sub()


if __name__ == "__main__":
  main()
