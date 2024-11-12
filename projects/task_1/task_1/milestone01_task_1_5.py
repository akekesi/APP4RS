import os
import numpy as np
import geopandas as gpd


def milestone01_task_1_5() -> None:
    """
    """
    milestone01_task_1_5_1()
    milestone01_task_1_5_2()


def milestone01_task_1_5_1() -> None:
    """
    This function processes GeoParquet files in the specified directory to extract 
    the multi-label set associated with each patch, omitting the "UNLABELED" labels. 
    It calculates the average number of labels per patch and prints the result rounded 
    to two decimal places.

    Expected output format:
    geom-average-num-labels: AVG rounded to two decimals

    Raises:
        AssertionError: If essential files or directories are not found.
    """

    # Directory containing the GeoParquet files
    path_geoparquets_dir = "untracked-files/milestone01/geoparquets"

    # Ensure the geoparquet directory exists before proceeding; raise an error if not found.
    assert os.path.isdir(path_geoparquets_dir), f"Directory not found: {path_geoparquets_dir}"

    # List to store the count of valid labels per patch
    num_labels_unique = []

    # List of class IDs corresponding to "UNLABELED" labels
    unlabeld_class_ids = {122, 123, 124, 131, 132, 133, 141, 142, 332, 334, 335, 423, 999}

    # Loop through each file in the GeoParquet directory
    for filename in os.listdir(path_geoparquets_dir):
        # Process only files with a _reference_map.parquet extension
        if filename.endswith("_reference_map.parquet"):
            # Construct full path to the current GeoParquet file
            file_path = os.path.join(path_geoparquets_dir, filename)

            # Load the GeoParquet file into a GeoDataFrame
            gdf = gpd.read_parquet(file_path)

            # Extract the "DN" column, which contains label IDs
            labels = gdf["DN"]

            # Filter out "UNLABELED" labels and count valid unique labels for this patch
            valid_labels = labels[~np.isin(labels, unlabeld_class_ids)]
            labels_unique = np.unique(valid_labels)

            # Add the count of unique valid labels to the list
            num_labels_unique.append(len(labels_unique))

    # Ensure there were valid patches processed
    if num_labels_unique:
        # Calculate the average number of labels per patch, rounded to two decimals
        average_num_labels = round(sum(num_labels_unique) / len(num_labels_unique), 2)
    else:
        average_num_labels = 0.0  # Handle case where no valid patches were found

    # Print the result: average number of labels per patch
    print(f"geom-average-num-labels: {average_num_labels:.2f}")


def milestone01_task_1_5_2() -> None:
    """
    This function processes GeoParquet files to count overlapping patches based on their geometries.
    Patches are considered overlapping if they share any interior point. Each patch is counted only once
    for overlaps.

    The task uses a spatial index to efficiently find overlapping geometries and count the unique overlaps.

    Raises:
        AssertionError: If essential files or directories are not found.    
    """
    # Directory containing the GeoParquet files
    path_geoparquets_dir = "untracked-files/milestone01/geoparquets"

    # Ensure the geoparquet directory exists before proceeding; raise an error if not found.
    assert os.path.isdir(path_geoparquets_dir), f"Directory not found: {path_geoparquets_dir}"

    # List to store the geometries and corresponding patch names
    geometries = []
    patches = []

    # Loop through each GeoParquet file in the directory
    for filename in os.listdir(path_geoparquets_dir):
        # Only process GeoParquet files
        if filename.endswith("_reference_map.parquet"):
            # Load the GeoParquet file into a GeoDataFrame
            gdf = gpd.read_parquet(os.path.join(path_geoparquets_dir, filename))

            # Add geometries and corresponding patch names
            geometries.extend(gdf["geometry"])
            patches.extend([filename] * len(gdf))

    # Create a GeoDataFrame to use its spatial index
    gdf_all = gpd.GeoDataFrame(geometry=geometries)

    # Use the spatial index for efficient overlap checks
    sindex = gdf_all.sindex

    # Set to track unique overlapping patches
    overlaps = set()

    # Compare each geometry with others using the spatial index
    for i, geom in enumerate(geometries):
        # Query the spatial index to find potential overlapping geometries
        possible_matches_index = list(sindex.intersection(geom.bounds))
        for j in possible_matches_index:
            # Ensure not comparing the same patch with itself
            if i != j and geom.intersects(geometries[j]):
                # Add the overlapping patch
                overlaps.add(patches[i])
                overlaps.add(patches[j])

    # Print the result: number of unique overlaps
    print(f"geom-num-overlaps: {len(overlaps)}")


if __name__ == "__main__":
    milestone01_task_1_5()
