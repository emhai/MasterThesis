import argparse
import json
import os.path
from matplotlib import pyplot as plt, image as mpimg


def show_images(vc_scene, mv_scene, path, key):

    num_rows = 3
    num_cols = len(vc_scene) + 3
    indices = [0, num_cols // 2, num_cols - 1]
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(num_cols * 1.5, 3), dpi=500)

    GT_path = os.path.join(path, "viewcrafter", "input", key)
    ground_truth_images = os.listdir(GT_path)
    ground_truth_images = sorted(ground_truth_images)
    results_path = os.path.join(path, "results",  f"{key}.jpg")

    scene_i = 0
    gt_i = 0
    # really hacky but works
    for i in range(num_cols):
        if i in indices:
            img = os.path.join(GT_path, ground_truth_images[gt_i])
            gt_img = mpimg.imread(img)
            axes[1, i].imshow(gt_img)
            axes[1, i].axis("off")
            axes[1, i].text(0.5, 1.03, f"input {gt_i}", size=4, ha="center", transform=axes[1, i].transAxes)

            axes[0, i].axis("off")
            axes[2, i].axis("off")

            gt_i += 1
            continue
        vc_frame = vc_scene[str(scene_i)]
        mv_frame = mv_scene[str(scene_i)]
        gt = vc_frame.get("ground_truth")
        vc_novel_view = vc_frame.get("novel_view")
        mv_novel_view = mv_frame.get("novel_view")

        gt_img = mpimg.imread(gt)
        vc_img = mpimg.imread(vc_novel_view)
        mv_img = mpimg.imread(mv_novel_view)

        vc_name = os.path.basename(vc_novel_view)
        mv_name = os.path.basename(mv_novel_view)

        vc_lpips = vc_frame.get("LPIPS")
        vc_ssim = vc_frame.get("SSIM")
        vc_psnr = vc_frame.get("PSNR")

        mv_lpips = mv_frame.get("LPIPS")
        mv_ssim = mv_frame.get("SSIM")
        mv_psnr = mv_frame.get("PSNR")


        axes[0, i].imshow(vc_img)
        axes[0, i].axis("off")
        axes[0, i].text(0.5, 1.05, f"{vc_name}\nLPIPS: {vc_lpips:.2f}SSIM: {vc_ssim:.2f}PSNR: {vc_psnr:.2f}", size=4, ha="center", transform=axes[0, i].transAxes)

        axes[1, i].imshow(gt_img)
        axes[1, i].axis("off")

        axes[2, i].imshow(mv_img)
        axes[2, i].axis("off")
        axes[2, i].text(0.5, -0.2, f"{mv_name}\nLPIPS: {mv_lpips:.2f}SSIM: {mv_ssim:.2f}PSNR: {mv_psnr:.2f}", size=4, ha="center", transform=axes[2, i].transAxes)
        scene_i += 1


    plt.tight_layout()
    #plt.show()
    plt.subplots_adjust(wspace=0.01, hspace=0.01)  # Reduce spacing between rows and columns
    plt.savefig(results_path)

def run(path):
    vc_json_path = os.path.join(path, "viewcrafter_results.json")
    mv_json_path = os.path.join(path, "mvsplat_results.json")
    results_path = os.path.join(path, "results")
    if not os.path.exists(results_path):
        os.makedirs(results_path)

    with open(vc_json_path, 'r') as vc_file:
        viewcrafter_data = json.load(vc_file)

    with open(mv_json_path, 'r') as mv_file:
        mvsplat_data = json.load(mv_file)

    # Extract and organize data
    for key in viewcrafter_data:  # Iterate over scenes
        vc_scene = viewcrafter_data.get(key, {})
        mv_scene = mvsplat_data.get(key, {})

        show_images(vc_scene, mv_scene, path, key)


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
