import argparse
import shutil
import utils
import re
import os
import json

def strip_to_numerals(name):
    # probably unneccesarry because files are 001 to ....
    return ''.join(re.findall(r'\d+', name))

def run(input_path, vc_input_path, vc_ground_truth_path, mv_input_path):

    name = os.path.basename(os.path.dirname(input_path))

    filenames = [f for f in os.listdir(input_path)]
    filenames.sort()

    len_filenames = len(filenames)
    if len_filenames % 2 == 0:
        os.remove(os.path.join(input_path, filenames[-1]))

    image_amount = len(filenames) // 2
    middle_i = image_amount

    print(f"Creating inputs")

    for i in range(image_amount):
        last_i = len_filenames - 1 - i
        name1 = strip_to_numerals(filenames[i])
        name2 = strip_to_numerals(filenames[last_i])

        if middle_i == int(name1) + 1 and middle_i == int(name2) - 1:
            continue
        # INPUT FOR VIEWCRAFTER
        folder_name = f"{name1}_{name2}"
        folder_path = os.path.join(vc_input_path, folder_name)
        os.makedirs(folder_path)
        shutil.copyfile(os.path.join(input_path, filenames[i]), os.path.join(folder_path, filenames[i]))
        shutil.copyfile(os.path.join(input_path, filenames[last_i]), os.path.join(folder_path, filenames[last_i]))
        shutil.copyfile(os.path.join(input_path, filenames[middle_i]), os.path.join(folder_path, filenames[middle_i]))

        # GROUND TRUTH FOR VIEWCRAFTER
        ground_truth_folder_path = os.path.join(vc_ground_truth_path, folder_name)
        os.makedirs(ground_truth_folder_path)

        # JSON INPUT FOR MVSPLAT360
        targets = []
        for j in range(i + 1, last_i):
            if j == middle_i:
                continue
            shutil.copyfile(os.path.join(input_path, filenames[j]), os.path.join(ground_truth_folder_path, filenames[j]))
            targets.append(j)

        json_data = {name: {"context": [i, middle_i, last_i], "target": targets}}

        json_file_name = folder_name + ".json"
        with open(os.path.join(mv_input_path, json_file_name), 'w') as f:
            json.dump(json_data, f)

def main():
    """
    Takes path ../name/original_images and creates a new subfolder ../name/input
    and subsequently new folders for pairs of images of varying length.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', type=utils.dir_path, help='Path to ../name/original_images')
    parser.add_argument('vc_input_path', type=utils.dir_path, help='Path to ../name/viewcrafter/input')
    parser.add_argument('vc_ground_truth_path', type=utils.dir_path, help='Path to ../name/viewcrafter/GT')
    parser.add_argument('mv_input_path', type=utils.dir_path, help='Path to ../name/mvsplat360/input/json_files')

    args = parser.parse_args()
    input_path = args.input_path.rstrip("/")
    mv_input_path = args.mv_input_path.rstrip("/")
    vc_input_path = args.vc_input_path.rstrip("/")
    vc_ground_truth_path = args.vc_ground_truth_path.rstrip("/")

    run(input_path, vc_input_path, vc_ground_truth_path, mv_input_path)

if __name__ == "__main__":
    main()