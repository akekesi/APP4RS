import os
import geopandas as gpd


def milestone01_task_1_5() -> None:
    """
    Executes the sequence of subtasks for milestone01 task 1.5.
    """
    milestone01_task_1_5_1()
    milestone01_task_1_5_2()


def milestone01_task_1_5_1() -> None:
    """
    Calculates and prints the average number of labels for a set of GeoParquet files.
    """
    # Directory containing the GeoParquet files
    geoparquets_dir = "untracked-files/milestone01/geoparquets"

    # List to store the number of labels per patch
    num_labels = []

    unlabeld_class_id = [
        122,
        123,
        124,
        131,
        132,
        133,
        141,
        142,
        332,
        334,
        335,
        423,
        999,
    ]

    # Loop through each GeoParquet file in the directory
    for filename in os.listdir(geoparquets_dir):
        # Only process GeoParquet files
        if filename.endswith(".parquet"):
            # Load the GeoParquet file into a GeoDataFrame
            gdf = gpd.read_parquet(os.path.join(geoparquets_dir, filename))

            labels = gdf["DN"]

            # Filter out the "UNLABELED" label
            labels = [label for label in labels if label in unlabeld_class_id]

            # Append the count of labels for this patch
            num_labels.append(len(labels))

    # Calculate the average number of labels per patch
    average_num_labels = sum(num_labels) / len(num_labels) if num_labels else 0

    # Print the result, rounded to two decimal places
    print(f"geom-average-num-labels: {average_num_labels:.2f}")


def milestone01_task_1_5_2() -> None:
    """
    Identifies and counts the number of overlapping patches in a set of GeoParquet files.
    """
    # Directory containing the GeoParquet files
    geoparquets_dir = "untracked-files/milestone01/geoparquets"

    # List to store the geometries of the patches
    geometries = []
    patches = []

    # Loop through each GeoParquet file in the directory
    for filename in os.listdir(geoparquets_dir):
        # Only process GeoParquet files
        if filename.endswith(".parquet"):
            # Load the GeoParquet file into a GeoDataFrame
            gdf = gpd.read_parquet(os.path.join(geoparquets_dir, filename))

            geometries.extend(gdf["geometry"])
            patches.extend([filename] * len(gdf))

    # Count the number of overlaps
    overlaps = set()

    # Compare each patch with every other patch to find overlaps
    for i in range(len(geometries)):
        for j in range(i + 1, len(geometries)):  # Only compare once per pair
            if geometries[i].intersects(geometries[j]):
                overlaps.add(patches[i])  # Add patch i to overlaps
                overlaps.add(patches[j])  # Add patch j to overlaps

    # Print the result: number of overlaps
    print(f"geom-num-overlaps: {len(overlaps)}")


if __name__ == "__main__":
    milestone01_task_1_5()
