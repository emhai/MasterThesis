import argparse
import json
import os
import utils
import metrics
from PIL import Image

def get_size(synthesized_path):
    synthesized_images = os.listdir(synthesized_path)
    first_nv_image = synthesized_images[0]
    image = Image.open(os.path.join(synthesized_path, first_nv_image))

    return image.size

def run(mv_path):

    print("Calculating MVSPLAT360 metrics")
    outer_path = os.path.dirname(os.path.dirname(mv_path))
    results_path = os.path.join(outer_path, "results.json")
    detailed_results_path = os.path.join(outer_path, "mvsplat_results.json")

    try:
        with open(results_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("File not found, run frameworks first.")

    detailed_results = {}
    for synth_name in os.listdir(mv_path):

        synthesized_path = os.path.join(mv_path, synth_name, "ImagesRefined0")
        ground_truth_path = os.path.join(mv_path, synth_name, "ImagesGT")
        width, height = get_size(synthesized_path)

        total_lpips = 0
        total_ssim = 0
        total_psnr = 0
        no_gt = 0

        detailed_results[synth_name] = {}
        for i, frame in enumerate(os.listdir(synthesized_path)):
            gt_file = os.path.join(ground_truth_path, frame)
            synth_file = os.path.join(synthesized_path, frame)
            calc_lpips, calc_psnr, calc_ssim = metrics.run(gt_file, synth_file)
            total_lpips += calc_lpips
            total_ssim += calc_ssim
            total_psnr += calc_psnr
            no_gt += 1

            detailed_results[synth_name][i] = {"ground_truth": gt_file, "novel_view": synth_file, "LPIPS": calc_lpips, "SSIM": calc_ssim, "PSNR": calc_psnr}

        result = {"no_gt": no_gt, "LPIPS": total_lpips / no_gt, "SSIM": total_ssim / no_gt, "PSNR": total_psnr / no_gt, "Resolution": f"{width}x{height}"}

        for key, value in result.items():
            data["mvsplat360"][synth_name][key] = value

    with open(results_path, 'w') as f:
        json.dump(data, f, indent=4)

    with open(detailed_results_path, 'w') as f:
        json.dump(detailed_results, f, indent=4)

def main():
    """
    Takes path ../name/mvsplat360/output and evaluates metrics.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('mvsplat_path', type=utils.dir_path, help='Path to the name/mvsplat/output')

    args = parser.parse_args()
    mvsplat_path = args.mvsplat_path.rstrip("/")

    run(mvsplat_path)

if __name__ == "__main__":
    main()