import argparse
import os
import resize_images
import shutil
import utils


def main():
    """
    Pipeline:   1. todo choose pictures
                2. create folder ../name
                3. copy images to ../name/original_images
                4. create pairwise combinations of variable length to ../name/input
                5. process each combination with viewcrafter to ../name/output
                6. create cropped ground truth images to ../name/cropped_images
                7. todo choose ground truth images
                8. evaluate metrics
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('path', type=utils.dir_path, help='Path to the directory')
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
    original_images_path = os.path.join(main_folder_path, "original_images")
    shutil.copytree(path, original_images_path)

    width = 1024
    height = 576
    resize_images.run(original_images_path, width, height)

if __name__ == "__main__":
    main()