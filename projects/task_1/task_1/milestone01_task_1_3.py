import os
import numpy as np
import pandas as pd


def milestone01_task_1_3() -> None:
    """
    Analyze seasonal distribution and label statistics of remote sensing image patches.

    This function reads metadata from a Parquet file containing image patch information,
    determines the acquisition season for each image (northern hemisphere), and calculates 
    the total number of patches per season. The results are printed in the format:
        spring: #samples
        summer: #samples
        fall: #samples
        winter: #samples

    Additionally, the function calculates the average and maximum number of labels 
    assigned to image patches. These values are printed as:
        average-num-labels: AVG (rounded to two decimals)
        maximum-num-labels: MAX

    Raises:
        AssertionError: If essential files or directories are not found.
    """
    # Path to the metadata Parquet file
    path_metadata_parquet = "untracked-files/milestone01/metadata.parquet"

    # Ensure the metadata file exists before proceeding; raise an error if not found.
    assert os.path.isfile(path_metadata_parquet), f"File not found: {path_metadata_parquet}"

    # Read the metadata file into a DataFrame
    metadata = pd.read_parquet(path=path_metadata_parquet)

    # Assert that 'patch_id' column exists
    assert "patch_id" in metadata.columns, "'patch_id' column is missing in the metadata file."

    # Extract the date from the "patch_id" column using a regex pattern
    date = metadata["patch_id"].str.extract(r"(\d{8})")[0]

    # Convert the extracted date strings to datetime objects
    date = pd.to_datetime(date, format="%Y%m%d", errors="coerce")

    # Drop rows with invalid dates (if any)
    metadata = metadata.dropna(subset=["patch_id"])

    # Assign the corresponding season to each image based on its acquisition date
    metadata["season"] = date.dt.month.apply(get_season)

    # Count the number of image patches for each season
    season_counts = {season: metadata["season"].value_counts().get(season, 0) for season in ["spring", "summer", "fall", "winter"]}

    # Print the total number of samples per season
    for season, count in season_counts.items():
        print(f"{season}: {count}")

    # Count the number of labels for each patch, handling different data structures
    metadata["label_num"] = metadata["labels"].apply(lambda x: len(x) if isinstance(x, (list, np.ndarray)) else 0)

    # Assert that label counts are non-negative integers
    assert (metadata["label_num"] >= 0).all(), "Label count contains invalid values."

    # Calculate the average and maximum number of labels
    label_num_avg = metadata["label_num"].mean()
    label_num_max = metadata["label_num"].max()

    # Print the average and maximum numbers of labels
    print(f"average-num-labels: {label_num_avg:.2f}")
    print(f"maximum-num-labels: {label_num_max}")


def get_season(month: int) -> str:
    """
    Return the season corresponding to the given month in the northern hemisphere.

    The function maps the provided month (1-12) to the corresponding season:
    - Spring: March (3), April (4), May (5)
    - Summer: June (6), July (7), August (8)
    - Fall: September (9), October (10), November (11)
    - Winter: December (12), January (1), February (2)

    Args:
        month (int): Month as an integer (1-12), representing the month of the year.

    Returns:
        str: The season as a string ("spring", "summer", "fall", "winter").
             Returns "unknown" if the input is outside the valid range (1-12).
    """
    if month in [3, 4, 5]:
        return "spring"
    if month in [6, 7, 8]:
        return "summer"
    if month in [9, 10, 11]:
        return "fall"
    if month in [12, 1, 2]:
        return "winter"
    return "unknown"


if __name__ == "__main__":
    milestone01_task_1_3()
