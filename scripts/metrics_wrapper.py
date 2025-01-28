import argparse
import os
import cv2
from skimage.metrics import structural_similarity as ssim
import utils
import metrics
import resize_images
from PIL import Image

def run(novel_view_path, ground_truth_path):

    synthesized_images = sorted(os.listdir(novel_view_path))
    ground_truth_images = sorted(os.listdir(ground_truth_path))

    first_nv_image = synthesized_images[0]
    image = Image.open(os.path.join(novel_view_path, first_nv_image))
    width, height = image.size

    resize_images.run(ground_truth_path, width, height)

    best_matches = {}

    for gt_file in ground_truth_images:
        gt_path = os.path.join(ground_truth_path, gt_file)
        gt_img = cv2.imread(gt_path)
        gt_img_gray = cv2.cvtColor(gt_img, cv2.COLOR_BGR2GRAY)

        best_ssim = -1  # Initialize best SSIM score
        best_match = None

        for synth_file in synthesized_images:
            synth_path = os.path.join(novel_view_path, synth_file)
            synth_img = cv2.imread(synth_path)
            synth_img_gray = cv2.cvtColor(synth_img, cv2.COLOR_BGR2GRAY)

            synth_img_resized = cv2.resize(synth_img_gray, (gt_img_gray.shape[1], gt_img_gray.shape[0]))
            current_ssim = ssim(synth_img_resized, gt_img_gray)

            if current_ssim > best_ssim:
                best_ssim = current_ssim
                best_match = synth_path
                # todo optimize somehow?


            print(f"Comparing {gt_file} to {synth_file} gives ssim {current_ssim}")

        best_matches[gt_path] = best_match

    for gt_file, best_match in best_matches.items():
        print(f"Synthesized: {gt_file} -> Best Match: {best_match}")
        metrics.run(gt_file, best_match)



def main():
    """
    Takes path ../name/viewcrafter and evaluates metrics.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('nv_path', type=utils.dir_path, help='Path to the ../output')
    parser.add_argument('gt_path', type=utils.dir_path, help='Path to  ../ground_truth')

    args = parser.parse_args()
    novel_view_path = args.nv_path.rstrip("/")
    ground_truth_path = args.gt_path.rstrip("/")

    run(novel_view_path, ground_truth_path)

if __name__ == "__main__":
    main()