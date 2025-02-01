import argparse
import json
import os.path
import re
import pandas as pd

def run(path):
    with open(path, 'r') as file:
        data = json.load(file)

    columns = [
        "name",
        "vc_inference_time", "vc_lpips", "vc_ssim", "vc_psnr", "vc_resolution",
        "mv_inference_time", "mv_lpips", "mv_ssim", "mv_psnr", "mv_resolution",
        "distance_01", "distance_02", "distance_12",
        "no_gt"
    ]

    rows = []

    # Extract and organize data
    for key in data["viewcrafter"]:  # Iterate over scenes
        vc = data["viewcrafter"].get(key, {})
        mv = data["mvsplat360"].get(key, {})

        row = {
            "name": key,
            "vc_inference_time": vc.get("inference_time"),
            "vc_lpips": vc.get("LPIPS"),
            "vc_ssim": vc.get("SSIM"),
            "vc_psnr": vc.get("PSNR"),
            "vc_resolution": vc.get("Resolution"),
            "mv_inference_time": mv.get("inference_time"),
            "mv_lpips": mv.get("LPIPS"),
            "mv_ssim": mv.get("SSIM"),
            "mv_psnr": mv.get("PSNR"),
            "mv_resolution": mv.get("Resolution"),
            "distance_01": vc.get("dist_01"),
            "distance_02": vc.get("dist_02"),
            "distance_12": vc.get("dist_12"),
            "no_gt": vc.get("no_gt")
        }
        rows.append(row)

    # Create DataFrame
    df = pd.DataFrame(rows, columns=columns)

    def compare_resolution(row, col1, col2):
        """Highlights the resolution with fewer pixels in yellow (lower resolution)."""

        def get_pixels(res):
            if isinstance(res, str):
                # Use regex to extract width and height
                match = re.match(r"(\d+)x(\d+)", res)
                if match:
                    width, height = map(int, match.groups())
                    return width * height  # Total pixels
            return None  # Handle missing values

        res_1 = get_pixels(row[col1])
        res_2 = get_pixels(row[col2])
        
        styles = ["", ""]
        if res_1 is not None and res_2 is not None:
            if res_1 > res_2:
                styles[0] = "border: 1px solid red"  # Highlight lower resolution
            elif res_1 < res_2:
                styles[1] = "border: 1px solid red"  # Highlight lower resolution

        return styles

    def highlight_lower(row, col1, col2):
        color = "border: 1px solid red"
        no_color = ""
        return [
            color if row[col1] < row[col2] else no_color,
            color if row[col2] < row[col1] else no_color,
        ]

    def highlight_higher(row, col1, col2):
        color = "border: 1px solid red"
        no_color = ""
        return [
            color if row[col1] > row[col2] else no_color,
            color if row[col2] > row[col1] else no_color,
        ]

    df = df.sort_values(by="distance_02", ascending=True)  # Set ascending=False for descending order

    styled_df = df.style \
        .apply(lambda row: highlight_lower(row, "vc_lpips", "mv_lpips"), subset=["vc_lpips", "mv_lpips"], axis=1) \
        .apply(lambda row: highlight_higher(row, "vc_psnr", "mv_psnr"), subset=["vc_psnr", "mv_psnr"], axis=1) \
        .apply(lambda row: highlight_higher(row, "vc_ssim", "mv_ssim"), subset=["vc_ssim", "mv_ssim"], axis=1) \
        .apply(lambda row: highlight_lower(row, "vc_inference_time", "mv_inference_time"), subset=["vc_inference_time", "mv_inference_time"], axis=1) \
        .apply(lambda row: compare_resolution(row, "vc_resolution", "mv_resolution"), subset=["vc_resolution", "mv_resolution"], axis=1) \
        .background_gradient(subset=["distance_02"], cmap="Greens") \
        .background_gradient(subset=["vc_psnr"], cmap="Greens") \
        .background_gradient(subset=["mv_psnr"], cmap="Greens") \
        .background_gradient(subset=["vc_ssim"], cmap="Greens") \
        .background_gradient(subset=["mv_ssim"], cmap="Greens") \
        .background_gradient(subset=["vc_lpips"], cmap="Greens_r") \
        .background_gradient(subset=["mv_lpips"], cmap="Greens_r") \
        .set_properties(**{
        "text-align": "center",  # Center all text
        "width": "120px"  # Increase column width
    })
    # Gradient on distance_1

    # Display styled DataFrame
    styled_path = os.path.join(os.path.dirname(path), "styled_results.html")
    styled_df.to_html(styled_path)

def main():
    """
    Takes path to results.json and visualizes results.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help='Path to results.json')

    args = parser.parse_args()
    path = args.path

    run(path)


if __name__ == "__main__":
    main()
