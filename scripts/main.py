import argparse
import os
import shutil
from datetime import datetime

import run_viewcrafter
import create_image_combinations
import utils
import extract_frames
import run_colmap
import visualize_cameras
import convert_to_torch
import run_mvsplat360
import viewcrafter_metrics
import mvsplat_metrics
import add_distances
import resize_images

def create_folder_structure(folders):
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print('Created folder:', folder)

def main():
    """
    Pipeline:   1. todo choose pictures
                2. create folder ../name
                3. copy images to ../name/original_images
                   run colmap to get tranfsorms.json
                   run visualize cameras
                4. create pairwise combinations of variable length to ../name/input
                5. process each combination with viewcrafter to ../name/output
                6. create cropped ground truth images to ../name/cropped_images
                7. todo choose ground truth images
                8. evaluate metrics
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('path', type=utils.dir_path, help='Path to the image directory')
    parser.add_argument('name', type=str, nargs='?', default=None, help='Name of test (optional)')

    args = parser.parse_args()
    path = args.path # folder with input pictures
    name = args.name # name of test

    if name is None:
        time = datetime.now().strftime("%m%d_%H%M")
        folder_name = os.path.basename(path)
        name = f"{folder_name}_{time}"

    main_folder_path = os.path.join("/home/emmahaidacher/Masterthesis/MasterThesis/tests", name)
    if not os.path.exists(main_folder_path):
        os.makedirs(main_folder_path)
    else:
        print(f"Folder {main_folder_path} already exists, choose another test name")
        exit()

    print(f"Copying images from {path} to {main_folder_path}")

    original_images_path = os.path.join(main_folder_path, "images")
    viewcrafter_path = os.path.join(main_folder_path, "viewcrafter")
    mvsplat_path = os.path.join(main_folder_path, "mvsplat360")
    results_path = os.path.join(main_folder_path, "results.json")

    vc_input_path = os.path.join(viewcrafter_path, "input")
    vc_output_path = os.path.join(viewcrafter_path, "output")
    vc_scripts_path = os.path.join(viewcrafter_path, "scripts")
    vc_GT_path = os.path.join(viewcrafter_path, "GT")

    mv_input_path = os.path.join(mvsplat_path, "input")
    mv_output_path = os.path.join(mvsplat_path, "output")
    mv_colmap_path = os.path.join(mvsplat_path, "colmap")

    mv_input_test_path = os.path.join(mv_input_path, "test")
    mv_input_json_path = os.path.join(mv_input_path, "json_files")

    all_folders = [viewcrafter_path, mvsplat_path, vc_input_path, vc_output_path, vc_scripts_path,
                   vc_GT_path, mv_input_path, mv_output_path, mv_colmap_path, mv_input_test_path, mv_input_json_path]

    create_folder_structure(all_folders)

    # copy to original_images
    shutil.copytree(path, original_images_path)
    filenames = [f for f in os.listdir(original_images_path)]
    filenames.sort()

    # rename
    for i, filename in enumerate(filenames):
        name, extension = os.path.splitext(filename)
        old_path = os.path.join(original_images_path, filename)
        new_path = os.path.join(original_images_path, f"{i:03}{extension}")
        os.rename(old_path, new_path)

    create_image_combinations.run(original_images_path, vc_input_path, vc_GT_path, mv_input_json_path)

    # VIEWCRAFTER
    print()
    run_viewcrafter.run(vc_input_path, vc_output_path, vc_scripts_path)
    extract_frames.run(vc_output_path)
    viewcrafter_metrics.run(viewcrafter_path)
    print()


    # MVSPLAT360
    print()
    run_colmap.run(original_images_path, mv_colmap_path)
    visualize_cameras.run(os.path.join(mv_colmap_path, "transforms.json"))
    convert_to_torch.run(mv_colmap_path, "images_8", mv_input_test_path) # choose resolution based on size
    run_mvsplat360.run(mv_input_path, mv_output_path)
    mvsplat_metrics.run(mv_output_path)
    print()


    add_distances.run(os.path.join(mv_colmap_path, "transforms.json"), results_path)

if __name__ == "__main__":
    main()