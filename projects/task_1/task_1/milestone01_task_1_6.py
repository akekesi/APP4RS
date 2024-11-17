import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def milestone01_task_1_6(save_png: bool = False) -> None:
    """
    """
    # Path to the metadata Parquet file
    path_metadata_parquet = "untracked-files/milestone01/metadata.parquet"

    # Ensure the metadata file exists before proceeding; raise an error if not found.
    assert os.path.isfile(path_metadata_parquet), f"File not found: {path_metadata_parquet}"

    # Read the metadata file into a DataFrame
    metadata = pd.read_parquet(path=path_metadata_parquet)

    # Ensure the "labels" and "patch_id" columns exist in the metadata
    assert "labels" in metadata.columns, "Missing 'labels' column in metadata"
    assert "patch_id" in metadata.columns, "Missing 'patch_id' column in metadata"

    # Train/test split ratio
    ratio_train = 0.8

    # Initialize train and test sets
    patches_train = set()
    patches_test = set()

    # Extract unique labels
    labels_all = np.unique([label for sublist in metadata["labels"] for label in sublist])
    
    # Iterate through each label
    for label in labels_all:
        # Find patches associated with this label
        patches_with_label = metadata[metadata["labels"].apply(lambda x: label in x)]["patch_id"]
        
        # Shuffle patches for reproducibility
        shuffled_patches = patches_with_label.sample(frac=1, random_state=42).reset_index(drop=True)

        # Determine split indices
        split_idx = int(len(shuffled_patches) * ratio_train)

        # Assign patches to train and test, avoiding overlaps
        for patch in shuffled_patches[:split_idx]:
            # Ensure patch is not already in test
            if patch not in patches_test:
                patches_train.add(patch)
        for patch in shuffled_patches[split_idx:]:
            # Ensure patch is not already in train
            if patch not in patches_train:
                patches_test.add(patch)

    # DataFrame létrehozása a train/test split-hez
    split_df = pd.DataFrame({
        "train": pd.Series(list(patches_train)),
        "test": pd.Series(list(patches_test))
    })

    path_untracked_files = "untracked-files"

    # Ensure the BigEarthNets with errors directory exists before proceeding; raise an error if not found.
    assert os.path.isdir(path_untracked_files), f"Directory not found: {path_untracked_files}"

    # Construct the path to the corresponding .csv file
    path_split_csv = os.path.join(path_untracked_files, "split.csv")

    # Save the split to CSV
    split_df.to_csv(path_split_csv, index=False)

    if save_png:
        # Construct the path to the corresponding .csv file
        path_split_png = os.path.join(path_untracked_files, "split.png")

        # Count label occurrences in train and test
        train_counts = metadata[metadata["patch_id"].isin(patches_train)]["labels"].explode().value_counts()
        test_counts = metadata[metadata["patch_id"].isin(patches_test)]["labels"].explode().value_counts()

        # Plot the label distribution
        fig, ax = plt.subplots(figsize=(25, 15))
        train_counts.plot(kind='bar', alpha=0.7, label="Train", color='blue', ax=ax)
        test_counts.plot(kind='bar', alpha=0.7, label="Test", color='orange', ax=ax)

        plt.title("Label Distribution in Train/Test Splits")
        plt.xlabel("Labels")
        plt.ylabel("Count")
        plt.legend()
        plt.savefig(path_split_png)
        plt.close()


if __name__ == "__main__":
    milestone01_task_1_6()
    # milestone01_task_1_6(save_png=True)
