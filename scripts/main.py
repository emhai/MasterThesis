import argparse
import os
import shutil

import resize_images
import run_viewcrafter
import create_image_combinations
import utils
import extract_frames
import run_colmap
import visualize_cameras

def main():
    """
    Pipeline:   1. todo choose pictures
                2. create folder ../name
                3. copy images to ../name/original_images
                   run colmap to get tranfsorms.json
                   run viszalize cameras
                4. create pairwise combinations of variable length to ../name/input
                5. process each combination with viewcrafter to ../name/output
                6. create cropped ground truth images to ../name/cropped_images
                7. todo choose ground truth images
                8. evaluate metrics
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('path', type=utils.dir_path, help='Path to the image directory')
    parser.add_argument('name', type=str, help='Name of test')

    args = parser.parse_args()
    path = args.path
    name = args.name

    main_folder_path = os.path.join("/home/emmahaidacher/Masterthesis/MasterThesis/tests", name)
    if not os.path.exists(main_folder_path):
        os.makedirs(main_folder_path)
    else:
        print(f"Folder {main_folder_path} already exists, choose another test name")
        exit()

    print(f"Copying images from {path} to {main_folder_path}")
    original_images_path = os.path.join(main_folder_path, "original")
    cropped_images_path = os.path.join(main_folder_path, "cropped")
    colmap_images_path = os.path.join(main_folder_path, "colmap")
    input_path = os.path.join(main_folder_path, "input")
    output_path = os.path.join(main_folder_path, "output")

    shutil.copytree(path, original_images_path)
    filenames = [f for f in os.listdir(original_images_path)]
    filenames.sort()

    for i, filename in enumerate(filenames, start=1):
        name, extension = os.path.splitext(filename)
        old_path = os.path.join(original_images_path, filename)
        new_path = os.path.join(original_images_path, f"{i:03}{extension}")
        os.rename(old_path, new_path)

    run_colmap.run(original_images_path)
    visualize_cameras.run(os.path.join(colmap_images_path, "transforms.json"))

    width = 1024
    height = 576
    resize_images.run(original_images_path, width, height)
    create_image_combinations.run(original_images_path)
    run_viewcrafter.run(input_path)
    extract_frames.run(output_path)



if __name__ == "__main__":
    main()