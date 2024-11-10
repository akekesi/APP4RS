import os
import rasterio
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def convert_tif2png(path_original: str, path_output_dir: str) -> None:
    """
    """
    with rasterio.open(path_original) as src:
        # Read the first (and only) band
        band = src.read(1)

        # Plot the single band
        plt.imshow(band, cmap='gray')
        plt.colorbar(label='Pixel values')
        plt.title("Single Band GeoTIFF")
        plt.xlabel("X coordinate")
        plt.ylabel("Y coordinate")

        # Save the figure to a file
        file_name, _ = os.path.splitext(os.path.basename(path_original))
        path_png = os.path.join(path_output_dir, f"{file_name}.png")
        plt.savefig(path_png)
        plt.close()


def save_retiled_tif(path_orignal: str, path_tiles: list[str], path_output_dir: str) -> None:
    """
    """
    file_name, _ = os.path.splitext(os.path.basename(path_orignal))
    path_output_png = os.path.join(path_output_dir, f"{file_name}_all.png")

    with rasterio.open(path_orignal) as src:
        # Read the first (and only) band
        band_original = src.read(1)

        band_tiles = []
    for path_ in path_tiles:
        with rasterio.open(path_) as src:
            # Read the first (and only) band
            band_tiles.append(src.read(1))

    # Create a grid with custom spacing
    fig = plt.figure(figsize=(10, 20))
    # fig = plt.figure(figsize=(10, 20), constrained_layout=True)
    gs = gridspec.GridSpec(4, 2, figure=fig)
    # gs = gridspec.GridSpec(4, 2, figure=fig, width_ratios=[1, 1], height_ratios=[1, 1, 1, 1])

    # Set a common colormap for consistency
    cmap = "gray"

    # Plot the original image in a 2x2 space (first two rows and columns)
    ax_original = fig.add_subplot(gs[0:2, 0:2])
    img = ax_original.imshow(band_original, cmap=cmap)
    ax_original.set_title("Original Image")
    ax_original.axis("off")

    # Plot each tile in the remaining rows
    ax_top_left = fig.add_subplot(gs[2, 0])
    ax_top_left.imshow(band_tiles[0], cmap=cmap)
    ax_top_left.set_title("Top Left Tile")
    ax_top_left.axis("off")

    ax_top_right = fig.add_subplot(gs[2, 1])
    ax_top_right.imshow(band_tiles[1], cmap=cmap)
    ax_top_right.set_title("Top Right Tile")
    ax_top_right.axis("off")

    ax_bottom_left = fig.add_subplot(gs[3, 0])
    ax_bottom_left.imshow(band_tiles[2], cmap=cmap)
    ax_bottom_left.set_title("Bottom Left Tile")
    ax_bottom_left.axis("off")

    ax_bottom_right = fig.add_subplot(gs[3, 1])
    ax_bottom_right.imshow(band_tiles[3], cmap=cmap)
    ax_bottom_right.set_title("Bottom Right Tile")
    ax_bottom_right.axis("off")

    # Add a horizontal colorbar at the bottom of the figure
    cbar = fig.colorbar(img, ax=fig.get_axes(), orientation='horizontal', fraction=0.05, pad=0.1)
    cbar.set_label('Pixel Values')

    # Save the entire figure as a single image file
    # plt.tight_layout()
    plt.savefig(path_output_png, dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    path_output_dir = "untracked-files/re-tiled"
    path_original = "untracked-files/milestone01/BigEarthNet-v2.0-S2-with-errors/S2B_MSIL2A_20170808T094029_N9999_R036_T35ULA/S2B_MSIL2A_20170808T094029_N9999_R036_T35ULA_33_29/S2B_MSIL2A_20170808T094029_N9999_R036_T35ULA_33_29_B02.tif"

    path_tiles = []
    for path_ in os.listdir(path=path_output_dir):
        if path_.endswith(".tif"):
            path_ = os.path.join(path_output_dir, path_)
            path_tiles.append(path_)
            convert_tif2png(path_original=path_, path_output_dir=path_output_dir)

    convert_tif2png(path_original=path_original, path_output_dir=path_output_dir)
    save_retiled_tif(
        path_orignal=path_original,
        path_tiles=sorted(path_tiles),
        path_output_dir=path_output_dir
    )
