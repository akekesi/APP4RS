import os
import rasterio
import numpy as np
import pandas as pd

# Define NO_DATA value
VALUE_NO_DATA = 7

def milestone01_task_1_4() -> None:
    """
    """
    milestone01_task_1_4_1()
    milestone01_task_1_4_2()

def milestone01_task_1_4_1() -> None:
    """
    """
    num_wrong_size = 0
    num_with_no_data = 0
    num_not_part_of_dataset = 0

    # Define expected resolutions for each band
    expected_resolutions = {
        "B02": (120, 120), "B03": (120, 120), "B04": (120, 120), "B08": (120, 120),
        "B05": (60, 60), "B06": (60, 60), "B07": (60, 60), "B8A": (60, 60), "B11": (60, 60), "B12": (60, 60),
        "B01": (20, 20), "B09": (20, 20),
    }

    # Path to the metadata Parquet file
    path_metadata_parquet = "untracked-files/milestone01/metadata.parquet"

    # TODO: is it needed (if or assert)
    # Check if the file exists (to handle any missing files)
    if not os.path.isfile(path_metadata_parquet):
        return

    # Read the metadata file into a DataFrame
    metadata = pd.read_parquet(path=path_metadata_parquet)

    # Path to the BigEarthNet-v2.0-S2-with-errors
    path_big_earth_net_errors = "untracked-files/milestone01/BigEarthNet-v2.0-S2-with-errors"

    # Recursively search through the directory for patches
    for dirpath, dirnames, filenames in os.walk(path_big_earth_net_errors):
        # Check if the current directory contains a patch (i.e., .tif files for bands)
        tif_files = [f for f in filenames if f.endswith(".tif")]

        # Only proceed if .tif files are found
        if tif_files:
            # Extract the patch ID from the directory name
            patch_id = os.path.basename(dirpath)

            # Check if metadata exists
            if patch_id not in metadata["patch_id"].values:
                num_not_part_of_dataset += 1
                continue

            # Check each band for resolution and NO_DATA value
            for tif_file in tif_files:
                band = tif_file.split(".")[0].split("_")[-1]
                if band in expected_resolutions:
                    expected_size = expected_resolutions[band]

                    # TODO: is it needed (if or assert)
                    # Check if the file exists (to handle any missing files)
                    if not os.path.isfile(path_metadata_parquet):
                        continue

                    with rasterio.open(os.path.join(dirpath, tif_file)) as src:
                        data = src.read(1) # Read the first (and only) band of the .tif (Single-Band) file.
                        
                        # Check for correct size
                        if data.shape != expected_size:
                            num_wrong_size += 1
                            continue
                        
                        # Check for NO_DATA [7] values
                        # If a pixel has a value of 7, it represents a NO_DATA pixel, 
                        # meaning that the data for that pixel is invalid or missing.
                        if (data == VALUE_NO_DATA).any():
                            num_with_no_data += 1
                            continue

    print(f"wrong-size: {num_wrong_size}")
    print(f"with-no-data: {num_with_no_data}")
    print(f"not-part-of-dataset: {num_not_part_of_dataset}")

def milestone01_task_1_4_2() -> None:
    # Path to the BigEarthNet-v2.0-S2-with-errors
    path_big_earth_net_errors = "untracked-files/milestone01/BigEarthNet-v2.0-S2-with-errors"

    # Load the CSV file directly (gzipped)
    path_patches_for_stats = "untracked-files/milestone01/patches_for_stats.csv.gz"

    patches_df = pd.read_csv(path_patches_for_stats)

    # List of bands in the specified order
    bands = ["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8A", "B09", "B11", "B12"]

    # Initialize dictionaries to store the sums, squared sums, and counts
    band_stats = {band: [] for band in bands}

    # Loop through each row in the DataFrame
    for index, row in patches_df.iterrows():
        tile = row["tile"]
        patch_id = row["patch_id"]
    
        for band in bands:
            # Construct the path to each .tif file
            path_tif = os.path.join(path_big_earth_net_errors, tile, patch_id, f"{patch_id}_{band}.tif")

            # TODO: is it needed (if or assert)
            # Check if the file exists (to handle any missing files)
            if not os.path.isfile(path_tif):
                continue

            with rasterio.open(path_tif) as src:
                data = src.read(1)

                # Mask NO_DATA values
                valid_data = data[data != VALUE_NO_DATA]

                if valid_data.size > 0:
                    band_stats[band].append(valid_data)

    # Calculate and print the mean and standard deviation for each band
    for band in bands:
        if len(band_stats[band]) > 0:
            pixels = np.concatenate(band_stats[band])
            pixels_n = pixels.size
            pixels_mean = np.sum(pixels) / pixels_n
            pixels_std_dev = np.sqrt(1 / pixels_n * np.sum((pixels - pixels_mean) ** 2))
            
            print(f"{band} mean: {round(pixels_mean)}")
            print(f"{band} std-dev: {round(pixels_std_dev)}")
        else:
            print(f"{band} mean: 0")
            print(f"{band} std-dev: 0")


if __name__ == "__main__":
    milestone01_task_1_4()
