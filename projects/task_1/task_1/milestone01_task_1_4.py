import os
import rasterio
import numpy as np
import pandas as pd
from rasterio.transform import Affine


def milestone01_task_1_4() -> None:
    """
    """
    milestone01_task_1_4_1()
    milestone01_task_1_4_2()
    milestone01_task_1_4_3()


def milestone01_task_1_4_1() -> None:
    """
    Checks each remote-sensing patch in the BigEarthNet-v2.0-S2-with-errors/ directory 
    for the following issues:
        - Incorrect number of pixels for specific bands
        - Presence of NO_DATA (value 7) pixels
        - Missing metadata in the metadata.parquet file

    The function prints the total count of invalid patches per error type in the 
    specified format:
        wrong-size: #samples
        with-no-data: #samples
        not-part-of-dataset: #samples

    Raises:
        AssertionError: If essential files or directories are not found.
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

    # Ensure the metadata file exists before proceeding; raise an error if not found.
    assert os.path.isfile(path_metadata_parquet), f"File not found: {path_metadata_parquet}"

    # Read the metadata file into a DataFrame
    metadata = pd.read_parquet(path=path_metadata_parquet)

    # Path to the BigEarthNet-v2.0-S2-with-errors directory containing the patches
    path_big_earth_net_errors = "untracked-files/milestone01/BigEarthNet-v2.0-S2-with-errors"

    # Ensure the BigEarthNets with errors directory exists before proceeding; raise an error if not found.
    assert os.path.isdir(path_big_earth_net_errors), f"Directory not found: {path_big_earth_net_errors}"

    # Recursively walk through the directory to find patch files
    for dirpath, dirnames, filenames in os.walk(path_big_earth_net_errors):
        tif_files = [f for f in filenames if f.endswith(".tif")]

        not_part_of_dataset = False
        with_no_data = False
        wrong_size = False

        # Process only directories containing .tif files (band data)
        if tif_files:
            # Extract patch ID from the directory name
            patch_id = os.path.basename(dirpath)

            # Check if the patch ID exists in the metadata
            if patch_id not in metadata["patch_id"].values:
                not_part_of_dataset = True

            # Check each .tif file for resolution and NO_DATA values
            for tif_file in tif_files:
                # Extract band from filename
                band = tif_file.split(".")[0].split("_")[-1]
                if band in expected_resolutions:
                    expected_size = expected_resolutions[band]

                    # Construct the full path to the .tif file
                    path_tif = os.path.join(dirpath, tif_file)

                    # Ensure the .tif file exists before proceeding; raise an error if not found.
                    assert os.path.isfile(path_tif), f"File not found: {path_tif}"

                    # Open the .tif file and check for errors
                    with rasterio.open(path_tif) as src:
                        # Read the first (only) band of the .tif file
                        data = src.read(1)
                        value_no_data = src.nodata

                    # Check if the image has the expected resolution (size)
                    if data.shape != expected_size:
                        wrong_size = True

                    # Check for NO_DATA values in the image
                    if (data == value_no_data).any():
                        with_no_data = True

        # count for patches
        if not_part_of_dataset:
            num_not_part_of_dataset += 1
        if wrong_size:
            num_wrong_size += 1
        if with_no_data:
            num_with_no_data += 1

    # Print the results
    print(f"wrong-size: {num_wrong_size}")
    print(f"with-no-data: {num_with_no_data}")
    print(f"not-part-of-dataset: {num_not_part_of_dataset}")


def milestone01_task_1_4_2() -> None:
    """
    Calculates and prints the mean and standard deviation for each band across all patches
    based on valid (non-NO_DATA) pixel values. Uses the patches_for_stats.csv.gz file to determine
    the patches and ensures that all files are read correctly without including any NO_DATA values.

    Expected output format for each band:
    B01 mean: MEAN rounded to the closest integer
    B01 std-dev: Std-Dev rounded to the closest integer
    ...
    B12 mean: MEAN rounded to the closest integer
    B12 std-dev: Std-Dev rounded to the closest integer

    Raises:
        AssertionError: If essential files or directories are not found.
    """
    # Path to the BigEarthNet-v2.0-S2-with-errors directory containing the patches
    path_big_earth_net_errors = "untracked-files/milestone01/BigEarthNet-v2.0-S2-with-errors"

    # Ensure the BigEarthNets with errors directory exists before proceeding; raise an error if not found.
    assert os.path.isdir(path_big_earth_net_errors), f"Directory not found: {path_big_earth_net_errors}"

    # Path to the CSV file containing patch information
    path_patches_for_stats = "untracked-files/milestone01/patches_for_stats.csv.gz"

    # Ensure the CSV file exists before proceeding; raise an error if not found.
    assert os.path.isfile(path_patches_for_stats), f"File not found: {path_patches_for_stats}"

    # Read the CSV file into a DataFrame
    patches_df = pd.read_csv(path_patches_for_stats, compression='gzip')

    # List of bands to analyze
    bands = ["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8A", "B09", "B11", "B12"]

    # # Dictionary to store pixel data for each band
    # band_stats = {band: [] for band in bands}
    # Dictionary to store mean, variance, and count for each band
    band_stats = {band: {'mean': 0.0, 'var': 0.0, 'count': 0} for band in bands}

    # Loop through each patch row in the DataFrame
    for index, row in patches_df.iterrows():
        tile = row["tile"]
        patch_id = row["patch_id"]

        # Loop through each band and gather pixel values
        for band in bands:
            # Construct the path to the corresponding .tif file
            path_tif = os.path.join(path_big_earth_net_errors, tile, patch_id, f"{patch_id}_{band}.tif")

            # Ensure the .tif file exists before proceeding; raise an error if not found.
            assert os.path.isfile(path_tif), f"File not found: {path_tif}"

            # Open the .tif file and read its pixel data
            with rasterio.open(path_tif) as src:
                # Read the first (only) band of the .tif file
                data = src.read(1)
                value_no_data = src.nodata

            # Mask out NO_DATA pixels
            valid_data = data[data != value_no_data]

            # Check size
            if valid_data.size > 0:
                # band_stats[band].append(valid_data)
                band_stats[band]['mean'], band_stats[band]['var'], band_stats[band]['count'] = update_stats(
                    existing_mean=band_stats[band]['mean'],
                    existing_var=band_stats[band]['var'],
                    count=band_stats[band]['count'],
                    new_data=valid_data,
                )

    # Calculate and print the mean and standard deviation for each band
    for band in bands:
        # if len(band_stats[band]) > 0:
        #     # Concatenate all pixel arrays for the band and calculate statistics
        #     pixels = np.concatenate(band_stats[band])
        #     pixels_n = pixels.size
        #     pixels_mean = np.sum(pixels) / pixels_n
        #     pixels_std_dev = np.sqrt(1 / pixels_n * np.sum((pixels - pixels_mean) ** 2))
        if band_stats[band]['count'] > 1:
            pixels_mean = band_stats[band]['mean']
            pixels_std_dev = np.sqrt(band_stats[band]['var'] / (band_stats[band]['count'] - 1))        
        else:
            # Default values if no valid data is found
            pixels_mean = 0
            pixels_std_dev = 0
        print(f"{band} mean: {round(pixels_mean)}")
        print(f"{band} std-dev: {round(pixels_std_dev)}")


def milestone01_task_1_4_3() -> None:
    """
    Splits a given GeoTIFF image into four equally sized, square sub-patches and 
    exports them as new GeoTIFF files with suffixes (_A.tif, _B.tif, _C.tif, _D.tif).
    Ensures the sub-patches retain correct geographical information and verifies this 
    after exporting.

    Raises:
        AssertionError: If essential files or directories are not found.
    """
    # Path to the original GeoTIFF file to be split
    path_tile_original = "untracked-files/milestone01/BigEarthNet-v2.0-S2-with-errors/S2B_MSIL2A_20170808T094029_N9999_R036_T35ULA/S2B_MSIL2A_20170808T094029_N9999_R036_T35ULA_33_29/S2B_MSIL2A_20170808T094029_N9999_R036_T35ULA_33_29_B02.tif"

    # Ensure the .tif file exists before proceeding; raise an error if not found.
    assert os.path.isfile(path_tile_original), f"File not found: {path_tile_original}"

    # Output directory to save the split patches
    path_output_dir = "untracked-files/re-tiled"

    # Create the output directory if it doesn't exist
    os.makedirs(path_output_dir, exist_ok=True)

    # Open the original GeoTIFF file
    with rasterio.open(path_tile_original) as src:
        # Read the image data into a numpy array
        data = src.read()

    # Get the dimensions of the image
    height = data.shape[1]
    width = data.shape[2]
    
    # Calculate the midpoint to split the image into 4 patches
    if width % 2 or height % 2:
        assert False, f"GeoTIFF file {path_tile_original} can not be equally sized."

    # Calculate the midpoint to split the image into 4 patches
    mid_x = width // 2
    mid_y = height // 2

    # Create the 4 sub-patches
    patches = {
        'A': (data[:, :mid_y, :mid_x], src.transform),
        'B': (data[:, :mid_y, mid_x:], src.transform * Affine.translation(mid_x, 0)),
        'C': (data[:, mid_y:, :mid_x], src.transform * Affine.translation(0, mid_y)),
        'D': (data[:, mid_y:, mid_x:], src.transform * Affine.translation(mid_x, mid_y)),
    }

    # Write each patch to a new GeoTIFF file
    for patch, (patch_data, patch_transform) in patches.items():

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
            transform=patch_transform,
            dtype=src.dtypes[0], 
        ) as dst:
            # Write the patch data to the new GeoTIFF file
            dst.write(patch_data)

        # After writing the patch, open the new GeoTIFF file to verify its integrity
        with rasterio.open(path_output_file) as dst:
            # Perform integrity checks on the new GeoTIFF
            milestone01_task_1_4_3_check(src, dst)


def milestone01_task_1_4_3_check(src, dst) -> None:
    """
    Perform integrity checks on the original and newly generated sub-patch GeoTIFFs 
    to ensure they retain the correct geographical information. The checks include:

    - Verifying that the Coordinate Reference System (CRS) matches between the source 
      and destination images.
    - Checking that the spatial transform is updated and consistent for each patch 
      (ensuring accurate geographical referencing).

    Args:
        src: The source raster (original tile).
        dst: The destination raster (sub-patch).
    """
    # Check if the Coordinate Reference System (CRS) of the patch matches the original image
    assert dst.crs == src.crs, f"CRS mismatch: {dst.crs} vs {src.crs}"

    # Check the affine transformation:
    # Patch "_A.tif" should retain the original transform, others should differ.
    if "_A.tif" in dst.name:
        assert dst.transform == src.transform, f"Transform should be the same: {dst.transform} vs {src.transform}"
    else:
        assert dst.transform != src.transform, f"Transform should be different: {dst.transform} vs {src.transform}"


def update_stats(existing_mean, existing_var, count, new_data):
    """
    Incrementally updates the mean and variance based on new data using Welford's method.

    Args:
        existing_mean (float): Current mean value.
        existing_var (float): Current variance value.
        count (int): Current count of observations.
        new_data (np.ndarray): New batch of data points.

    Returns:
        tuple: Updated mean, variance, and count.
    """
    for x in new_data:
        count += 1
        delta = x - existing_mean
        existing_mean += delta / count
        delta2 = x - existing_mean
        existing_var += delta * delta2
    return existing_mean, existing_var, count


if __name__ == "__main__":
    milestone01_task_1_4()
