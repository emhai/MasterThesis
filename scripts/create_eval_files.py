import argparse
import shutil
import utils
import re
import os

def strip_to_numerals(name):
    return ''.join(re.findall(r'\d+', name))

def run(path):
    path = path.rstrip("/")
    filenames = [f for f in os.listdir(path)]
    filenames.sort()

    len_filenames = len(filenames)
    image_amount = len(filenames) // 2

    outer_folder_path = os.path.dirname(path)
    input_path = os.path.join(outer_folder_path, "input")
    os.makedirs(input_path)

    # todo what if even amount -> delete 1?
    print(f"Creating new folders")

    print(f"Creating {image_amount} new folders in {input_path}")
    for i in range(image_amount):
        last_i = len_filenames - 1 - i
        name1 = strip_to_numerals(filenames[i])
        name2 = strip_to_numerals(filenames[last_i])
        folder_name = f"in{name1}x{name2}"
        folder_path = os.path.join(os.path.dirname(path), "input", folder_name)
        os.makedirs(folder_path)
        shutil.copyfile(os.path.join(path, filenames[i]), os.path.join(folder_path, filenames[i]))
        shutil.copyfile(os.path.join(path, filenames[last_i]), os.path.join(folder_path, filenames[last_i]))


def main():
    """
    Takes path ../name/original_images and creates a new subfolder ../name/input
    and subsequently new folders for pairs of images of varying length.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=utils.dir_path, help='Path to ../name/original_images')

    args = parser.parse_args()
    run(args.path)

if __name__ == "__main__":
    main()