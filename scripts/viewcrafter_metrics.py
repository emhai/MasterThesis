import argparse
import json
import os
import cv2
from skimage.metrics import structural_similarity as ssim
import utils
import metrics
import resize_images
from PIL import Image

def get_size(synthesized_path):
    synthesized_images = os.listdir(synthesized_path)
    first_nv_image = synthesized_images[0]
    image = Image.open(os.path.join(synthesized_path, first_nv_image))

    return image.size

def find_best_matches(synthesized_path, ground_truth_path):
    synthesized_images = sorted(os.listdir(synthesized_path))
    ground_truth_images = sorted(os.listdir(ground_truth_path))

    best_matches = {}

    for gt_file in ground_truth_images:
        gt_path = os.path.join(ground_truth_path, gt_file)
        gt_img = cv2.imread(gt_path)
        gt_img_gray = cv2.cvtColor(gt_img, cv2.COLOR_BGR2GRAY)

        best_ssim = -1  # Initialize best SSIM score
        best_match = None

        for synth_file in synthesized_images:
            synth_path = os.path.join(synthesized_path, synth_file)
            synth_img = cv2.imread(synth_path)
            synth_img_gray = cv2.cvtColor(synth_img, cv2.COLOR_BGR2GRAY)

            synth_img_resized = cv2.resize(synth_img_gray, (gt_img_gray.shape[1], gt_img_gray.shape[0]))
            current_ssim = ssim(synth_img_resized, gt_img_gray)

            if current_ssim > best_ssim:
                best_ssim = current_ssim
                best_match = synth_path
                # todo optimize somehow?

            #print(f"Comparing {gt_file} to {synth_file} gives ssim {current_ssim}")

        best_matches[gt_path] = best_match

    return best_matches

def run(viewcrafter_path):

    print("Calculating VIEWCRAFTER metrics")

    synthesized_path = os.path.join(viewcrafter_path, "output")
    ground_truth_path = os.path.join(viewcrafter_path, "GT")

    outer_path = os.path.dirname(viewcrafter_path)
    results_path = os.path.join(outer_path, "results.json")
    detailed_results_path = os.path.join(outer_path, "viewcrafter_results.json")

    try:
        with open(results_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("File not found, run frameworks first.")

    detailed_results = {}
    for synth_name in os.listdir(synthesized_path):

        synth_images_path = os.path.join(synthesized_path, synth_name, "extracted_diffusion")
        gt_images_path = os.path.join(ground_truth_path, synth_name)
        width, height = get_size(synth_images_path)
        resize_images.run(gt_images_path, width, height)

        best_matches = find_best_matches(synth_images_path, gt_images_path)

        total_lpips = 0
        total_ssim = 0
        total_psnr = 0
        no_gt = 0

        i = 0
        detailed_results[synth_name] = {}
        for gt_file, best_match in best_matches.items():
            calc_lpips, calc_psnr, calc_ssim = metrics.run(gt_file, best_match)
            total_lpips += calc_lpips
            total_ssim += calc_ssim
            total_psnr += calc_psnr
            no_gt += 1

            detailed_results[synth_name][i] = {"ground_truth": gt_file, "novel_view": best_match , "LPIPS": calc_lpips, "SSIM": calc_ssim, "PSNR": calc_psnr}
            i+=1

        result = {"no_gt": no_gt, "LPIPS": total_lpips / no_gt, "SSIM": total_ssim / no_gt, "PSNR": total_psnr / no_gt, "Resolution": f"{width}x{height}"}

        for key, value in result.items():
            data["viewcrafter"][synth_name][key] = value

    with open(results_path, 'w') as f:
        json.dump(data, f, indent=4)

    with open(detailed_results_path, 'w') as f:
        json.dump(detailed_results, f, indent=4)

def main():
    """
    Takes path ../name/viewcrafter and evaluates metrics.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('viewcrafter_path', type=utils.dir_path, help='Path to the name/viewcrafter')

    args = parser.parse_args()
    vc_path = args.viewcrafter_path.rstrip("/")

    run(vc_path)

if __name__ == "__main__":
    main()