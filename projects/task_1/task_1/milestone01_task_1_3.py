import os
import numpy as np
import pandas as pd


def milestone01_task_1_3() -> None:
    """
    Process the metadata of remote sensing images.
    
    path of subject: /documents/APP4RS_milestone01_tasks.pdf

    This function reads a metadata file in Parquet format, extracts the season in which
    each image was acquired based on the date, and calculates statistics about the labels
    associated with the images.

    The output includes:
    - The total number of image patches per season (spring, summer, fall, winter).
    - The average number of labels per patch, rounded to two decimal places.
    - The maximum number of labels assigned to any single patch.
    """
    # Path to the metadata Parquet file
    path_metadata_parquet = "untracked-files/milestone01/metadata.parquet"


    # TODO: is it needed (if or assert)
    # Check if the file exists (to handle any missing files)
    if not os.path.isfile(path_metadata_parquet):
        return

    # Read the metadata file into a DataFrame
    metadata = pd.read_parquet(path=path_metadata_parquet)

    # Extract the date from the "patch_id" column using a regex pattern
    date = metadata["patch_id"].str.extract(r"(\d{8})")[0]

    # Convert the extracted date strings to datetime objects
    date = pd.to_datetime(date, format="%Y%m%d")

    # Assign the corresponding season to each image based on its acquisition date
    metadata["season"] = date.dt.month.apply(get_season)

    # Count the number of image patches for each season
    season_num = metadata["season"].value_counts()

    # Print the total number of samples per season
    for season in ["spring", "summer", "fall", "winter"]:
        print(f"{season}: {season_num.get(season, 0)}")

    # Count the number of labels for each patch, handling different data structures
    metadata["label_num"] = metadata["labels"].apply(lambda x: len(x) if isinstance(x, (list, np.ndarray)) else 0)

    # Calculate the average and maximum number of labels
    label_num_avg = metadata["label_num"].mean()
    label_num_max = metadata["label_num"].max()

    # Print the average and maximum numbers of labels
    print(f"average-num-labels: {label_num_avg:.2f}")
    print(f"maximum-num-labels: {label_num_max}")


def get_season(month: int) -> str:
    """Return the season corresponding to the given month.

    Args:
        month (int): Month as an integer (1-12).

    Returns:
        str: The season as a string ("spring", "summer", "fall", "winter").
    """
    if month in [3, 4, 5]:
        return "spring"
    if month in [6, 7, 8]:
        return "summer"
    if month in [9, 10, 11]:
        return "fall"
    if month in [12, 1, 2]:
        return "winter"


if __name__ == "__main__":
    milestone01_task_1_3()
