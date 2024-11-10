import os
import rasterio
import numpy as np
import pandas as pd


# Define NO_DATA value
# NO_DATA pixel value indicating missing or invalid data in the image
VALUE_NO_DATA = 7


def milestone01_task_1_4() -> None:
    """
    Executes the sequence of subtasks for milestone01 task 1.4.
    """
    milestone01_task_1_4_3()
    milestone01_task_1_4_4()
    milestone01_task_1_4_5()


def milestone01_task_1_4_3() -> None:
    """
    Task 1.4.3: Validates patch sizes, checks for NO_DATA values, and verifies if the patch 
    exists in the metadata. Counts errors for wrong size, NO_DATA, and missing metadata.
    """
    num_wrong_size = 0
    num_with_no_data = 0
    num_not_part_of_dataset = 0

    # Define expected resolutions for each band (in pixels)
    expected_resolutions = {
        "B02": (120, 120), "B03": (120, 120), "B04": (120, 120), "B08": (120, 120),
        "B05": (60, 60), "B06": (60, 60), "B07": (60, 60), "B8A": (60, 60), "B11": (60, 60), "B12": (60, 60),
        "B01": (20, 20), "B09": (20, 20),
    }

    # Path to the metadata Parquet file
    path_metadata_parquet = "untracked-files/milestone01/metadata.parquet"

    # TODO: is it needed (if or assert)
    # Check if the metadata file exists
    if not os.path.isfile(path_metadata_parquet):
        return

    # Read the metadata file into a DataFrame
    metadata = pd.read_parquet(path=path_metadata_parquet)

    # Path to the BigEarthNet-v2.0-S2-with-errors directory containing the patches
    path_big_earth_net_errors = "untracked-files/milestone01/BigEarthNet-v2.0-S2-with-errors"

    # Recursively walk through the directory to find patch files
    for dirpath, dirnames, filenames in os.walk(path_big_earth_net_errors):
        tif_files = [f for f in filenames if f.endswith(".tif")]

        # Process only directories containing .tif files (band data)
        if tif_files:
            # Extract patch ID from the directory name
            patch_id = os.path.basename(dirpath)

            # Check if the patch ID exists in the metadata
            if patch_id not in metadata["patch_id"].values:
                num_not_part_of_dataset += 1
                continue

            # Check each .tif file for resolution and NO_DATA values
            for tif_file in tif_files:
                band = tif_file.split(".")[0].split("_")[-1]
                if band in expected_resolutions:
                    expected_size = expected_resolutions[band]

                    # Construct the full path to the .tif file
                    path_tif = os.path.join(dirpath, tif_file)

                    # TODO: is it needed (if or assert)
                    # Check if the .tif file exists
                    if not os.path.isfile(path_tif):
                        continue

                    # Open the .tif file and check its data
                    with rasterio.open(path_tif) as src:
                        data = src.read(1)  # Read the first (only) band of the .tif file

                        # Check if the image has the expected resolution (size)
                        if data.shape != expected_size:
                            num_wrong_size += 1
                            continue

                        # Check for NO_DATA values in the image
                        if (data == VALUE_NO_DATA).any():
                            num_with_no_data += 1
                            continue

    # Print the error counts
    print(f"wrong-size: {num_wrong_size}")
    print(f"with-no-data: {num_with_no_data}")
    print(f"not-part-of-dataset: {num_not_part_of_dataset}")


def milestone01_task_1_4_4() -> None:
    """
    Task 1.4.4: Calculates and prints the mean and standard deviation for each band across all patches
    based on valid (non-NO_DATA) pixel values. It uses the patches_for_stats.csv.gz file to determine the patches.
    """
    # Path to the BigEarthNet-v2.0-S2-with-errors directory containing the patches
    path_big_earth_net_errors = "untracked-files/milestone01/BigEarthNet-v2.0-S2-with-errors"

    # Path to the CSV file containing patch information
    path_patches_for_stats = "untracked-files/milestone01/patches_for_stats.csv.gz"

    # TODO: is it needed (if or assert)
    # Check if the CSV file exists
    if not os.path.isfile(path_patches_for_stats):
        return

    # Read the CSV file into a DataFrame
    patches_df = pd.read_csv(path_patches_for_stats)

    # List of bands to analyze
    bands = ["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8A", "B09", "B11", "B12"]

    # Dictionary to store pixel data for each band
    band_stats = {band: [] for band in bands}

    # Loop through each patch row in the DataFrame
    for index, row in patches_df.iterrows():
        tile = row["tile"]
        patch_id = row["patch_id"]

        # Loop through each band and gather pixel values
        for band in bands:
            # Construct the path to the corresponding .tif file
            path_tif = os.path.join(path_big_earth_net_errors, tile, patch_id, f"{patch_id}_{band}.tif")

            # TODO: is it needed (if or assert)
            # Check if the .tif file exists
            if not os.path.isfile(path_tif):
                continue

            # Open the .tif file and read its pixel data
            with rasterio.open(path_tif) as src:
                data = src.read(1)    # Read the first (only) band of the .tif file

                # Mask out NO_DATA pixels
                valid_data = data[data != VALUE_NO_DATA]

                if valid_data.size > 0:
                    band_stats[band].append(valid_data)

    # Calculate and print the mean and standard deviation for each band
    for band in bands:
        pixels_mean = 0
        pixels_std_dev = 0
        if len(band_stats[band]) > 0:
            pixels = np.concatenate(band_stats[band])
            pixels_n = pixels.size
            pixels_mean = np.sum(pixels) / pixels_n
            pixels_std_dev = np.sqrt(1 / pixels_n * np.sum((pixels - pixels_mean) ** 2))
        print(f"{band} mean: {round(pixels_mean)}")
        print(f"{band} std-dev: {round(pixels_std_dev)}")


def milestone01_task_1_4_5() -> None:
    """
    Task 1.4.5: Splits a single GeoTIFF file into four square sub-patches and saves them as new GeoTIFFs. 
    Each sub-patch is saved in a specified output directory, and checks are performed to ensure integrity.
    """
    # Path to the original GeoTIFF file to be split
    path_tile_original = "untracked-files/milestone01/BigEarthNet-v2.0-S2-with-errors/S2B_MSIL2A_20170808T094029_N9999_R036_T35ULA/S2B_MSIL2A_20170808T094029_N9999_R036_T35ULA_33_29/S2B_MSIL2A_20170808T094029_N9999_R036_T35ULA_33_29_B02.tif"

    # Output directory to save the split patches
    path_output_dir = "untracked-files/re-tiled"

    # TODO: is it needed (if or assert)
    # Check if the original file exists
    if not os.path.isfile(path_tile_original):
        return

    # Create the output directory if it doesn't exist
    os.makedirs(path_output_dir, exist_ok=True)

    # Open the original GeoTIFF file
    with rasterio.open(path_tile_original) as src:
        # Read the image data into a numpy array
        data = src.read()

        # Get the dimensions of the image
        height = data.shape[1]
        width = data.shape[2]
        
        # Ensure the image is square (can be split evenly into 4 patches)
        if height != width:
            raise ValueError("Input image must be square.")
        
        # Calculate the midpoint to split the image into 4 patches
        mid_x = width // 2
        mid_y = height // 2
        # TODO: check divisibility
        
        # Create the 4 sub-patches
        patches = {
            'A': data[:, :mid_y, :mid_x],
            'B': data[:, :mid_y, mid_x:],
            'C': data[:, mid_y:, :mid_x],
            'D': data[:, mid_y:, mid_x:],
        }

        # Write each patch to a new GeoTIFF file
        for patch, patch_data in patches.items():

            # Extract the base filename and extension from the original tile path
            file_name, file_ext = os.path.splitext(os.path.basename(path_tile_original))

            # Define the output filename by appending the patch name (A, B, C, D) to the original filename
            path_output_file = os.path.join(path_output_dir, f'{file_name}_{patch}{file_ext}')
            
            # Create a new GeoTIFF file for each patch with the appropriate metadata
            with rasterio.open(
                fp=path_output_file,
                mode='w', 
                driver='GTiff', 
                width=patch_data.shape[2], 
                height=patch_data.shape[1], 
                count=src.count, 
                crs=src.crs, 
                transform=src.transform,
                dtype=src.dtypes[0], 
            ) as dst:
                # Write the patch data to the new GeoTIFF file
                dst.write(patch_data)

            # After writing the patch, open the new GeoTIFF file to verify its integrity
            with rasterio.open(path_output_file) as dst:
                # Perform integrity checks on the new GeoTIFF
                milestone01_task_1_4_5_check(src, dst)


def milestone01_task_1_4_5_check(src, dst) -> None:
    """
    Perform integrity checks on two raster files to ensure that
    the Coordinate Reference System (CRS) and affine transform are consistent.
    
    Args:
        src: The source raster (original tile).
        dst: The destination raster (patch).
    
    Raises:
        AssertionError: If there is a mismatch in CRS or transform.
    """
    # Check if the Coordinate Reference System (CRS) of the patch matches the original image
    assert dst.crs == src.crs, f"CRS mismatch: {dst.crs} vs {src.crs}"

    # Check if the affine transformation (spatial referencing) of the patch matches the original image
    assert dst.transform == src.transform, f"Transform mismatch: {dst.transform} vs {src.transform}"


if __name__ == "__main__":
    milestone01_task_1_4()
