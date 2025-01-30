import argparse
import json
import os.path
import re
import pandas as pd

from IPython.display import display, HTML


def run(path):
    vc_json_path = os.path.join(path, "viewcrafter_results.json")
    mv_json_path = os.path.join(path, "mvsplat_results.json")

    with open(vc_json_path, 'r') as vc_file:
        data = json.load(vc_file)

    with open(mv_json_path, 'r') as mv_file:
        mvsplat_data = json.load(mv_file)

    # Flatten the nested dictionary into a list of records
    records = []
    for scene_id, entries in data.items():
        for idx, values in entries.items():
            records.append({
                "Scene": scene_id,
                "Index": idx,
                "Ground Truth": values["ground_truth"],
                "Novel View": values["novel_view"]
            })

    # Create a DataFrame
    df = pd.DataFrame(records)

    # Function to format image paths as HTML images
    def path_to_image_html(path):
        return f'<img src="{path}" width="500">'

    # Convert DataFrame to an HTML table with images
    df_html = df.to_html(escape=False, formatters={
        "Ground Truth": path_to_image_html,
        "Novel View": path_to_image_html
    })

    # Wrap in full HTML structure
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Image Comparison Table</title>
        <style>
            table {{border-collapse: collapse; width: 100%;}}
            th, td {{border: 1px solid black; padding: 8px; text-align: center;}}
            img {{max-width: 100%; height: auto;}}
        </style>
    </head>
    <body>
        <h2>ViewCrafter Results</h2>
        {df_html}
    </body>
    </html>
    """

    # Save to an HTML file
    output_html_path = os.path.join(path, "viewcrafter_results.html")
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"HTML file saved as {output_html_path}")


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
