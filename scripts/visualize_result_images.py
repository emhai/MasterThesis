import argparse
import json
import os.path
import re
import pandas as pd

from IPython.display import display, HTML
from matplotlib import pyplot as plt, image as mpimg


# https://chatgpt.com/c/679b8689-8ab4-8001-9c6b-6d74b305d4b5
def show_images(df, path):
    num_rows = len(df)
    num_cols = 4  # The four image columns

    fig, axes = plt.subplots(num_rows + 1, num_cols + 1, figsize=(9, num_rows * 1.5), dpi=300) # Reduce figure size

    # Set column headers
    headers = ["Scene", "Viewcrafter GT", "Viewcrafter NV", "MVSplat360 GT", "MVSplat360 NV"]
    for col_idx, header in enumerate(headers):
        axes[0, col_idx].text(0.5, 0.5, header, fontsize=7, ha="center", va="center")
        axes[0, col_idx].axis("off")

    # Display images with row labels
    for row_idx, row in enumerate(df.itertuples(index=False), start=1):
        scene_name = f"{row.scene} {row_idx}"
        axes[row_idx, 0].text(0.5, 0.5, scene_name, fontsize=7, ha="center", va="center")
        axes[row_idx, 0].axis("off")

        # Iterate over the image columns
        image_paths = [row._2, row._3, row._4, row._5]  # Assuming column order
        for col_idx, img_path in enumerate(image_paths, start=1):
            img = mpimg.imread(img_path)
            axes[row_idx, col_idx].imshow(img)
            axes[row_idx, col_idx].axis("off")

    plt.subplots_adjust(wspace=0.01, hspace=0.01)  # Reduce spacing between rows and columns
    #plt.tight_layout()
    #plt.show()
    plt.savefig(path)

def run(path):
    vc_json_path = os.path.join(path, "viewcrafter_results.json")
    mv_json_path = os.path.join(path, "mvsplat_results.json")

    with open(vc_json_path, 'r') as vc_file:
        viewcrafter_data = json.load(vc_file)

    with open(mv_json_path, 'r') as mv_file:
        mvsplat_data = json.load(mv_file)

    rows = []
    columns = [
        "scene", "id",
        "Viewcrafter GT", "Viewcrafter NV",
        "MVSplat360 GT", "MVSplat360 NV",
    ]
    # Extract and organize data
    for key in viewcrafter_data:  # Iterate over scenes
        vc_scene = viewcrafter_data.get(key, {})
        mv_scene = mvsplat_data.get(key, {})

        for i in vc_scene:

            row = {
                "scene": key,
                "id": i,
                "Viewcrafter GT": vc_scene[i].get("ground_truth"),
                "Viewcrafter NV": vc_scene[i].get("novel_view"),
                "MVSplat360 GT":  mv_scene[i].get("ground_truth"),
                "MVSplat360 NV": mv_scene[i].get("novel_view"),
            }
            rows.append(row)

    # Create DataFrame
    df = pd.DataFrame(rows, columns=columns)
    show_images(df, os.path.join(path, "view.png"))




def main():
    """
    Takes path to outer folder and visualizes results.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help='Path to whole folder')

    args = parser.parse_args()
    path = args.path

    run(path)


if __name__ == "__main__":
    main()
