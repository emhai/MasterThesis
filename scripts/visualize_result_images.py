import argparse
import json
import os.path
import re
import pandas as pd

from IPython.core.display import display, HTML


def run(path):
    vc_json_path = os.path.join(path, "viewcrafter_results.json")
    mv_json_path = os.path.join(path, "mvsplat_results.json")

    with open(vc_json_path, 'r') as vc_file:
        viewcrafter_data = json.load(vc_file)

    with open(mv_json_path, 'r') as mv_file:
        mvsplat_data = json.load(mv_file)

    # Create a DataFrame with properly structured columns
    df = pd.DataFrame({
        "Input": viewcrafter_data["input"],
        "Ground Truth": [viewcrafter_data["ground_truth"]] * len(viewcrafter_data["input"]),
        "Novel View": [viewcrafter_data["novel_view"]] * len(viewcrafter_data["input"])
    })

    # Function to display images in HTML format
    def path_to_image_html(path):
        return f'<img src="{path}" width="100">'

    # Convert the DataFrame to HTML with images
    df_html = df.to_html(escape=False, formatters={
        "Input": path_to_image_html,
        "Ground Truth": path_to_image_html,
        "Novel View": path_to_image_html
    })


def main():
    """
    Takes path to results.json and visualizes results.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help='Path to whole folder')

    args = parser.parse_args()
    path = args.path

    run(path)


if __name__ == "__main__":
    main()
