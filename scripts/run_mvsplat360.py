import argparse
import shutil
import subprocess

from fontTools.unicodedata import script

import utils
import os
import re
import stat


def run(input_path, output_path):

    json_dir = os.path.join(input_path, "json_files") # todo ACHTUNG, muss gleich sein wie in main.py
    mvsplat_dir = "/home/emmahaidacher/Desktop/mvsplat360/mvsplat360"
    with open("/home/emmahaidacher/Masterthesis/MasterThesis/scripts/mvsplat_input.txt", 'r') as file:
        script_content = file.read()

    for file in os.listdir(json_dir):

        test_file = os.path.join(json_dir, file)
        name = file.split(".")[0]
        out_dir = os.path.join(output_path, name)

        modified_content = script_content
        modified_content = re.sub(r'CHOSEN_NAME', name, modified_content)
        modified_content = re.sub(r'PATH_TO_JSON', test_file, modified_content)
        modified_content = re.sub(r'PATH_TO_DATASET', input_path, modified_content)
        modified_content = re.sub(r'IMAGE_SHAPE', "[378,504]", modified_content) # e.g. [378,504] -- [h,w]
        modified_content = re.sub(r'PATH_TO_OUT_DIR', out_dir, modified_content)
        modified_content.strip("\n")

        original_env = os.environ.copy()

        print("Currently running:", name)
        subprocess.run(
            f'bash -c "source ~/.zshrc && conda deactivate && conda activate mvsplat360 && cd {mvsplat_dir} && {modified_content}"',
            shell=True)

        os.environ.clear()
        os.environ.update(original_env)


def main():
    """
    Takes path ../name/mvsplat360/input and runs mvsplat on each pairwise image combination. Saves to mvsplat360/output
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', type=utils.dir_path, help='Path to the ../name/mvsplat/input that contains test and json_files')
    parser.add_argument('output_path', type=utils.dir_path, help='Path to  ../name/mvsplat/output')

    args = parser.parse_args()
    input_path = args.input_path.rstrip("/")
    output_path = args.output_path.rstrip("/")

    run(input_path, output_path)

if __name__ == "__main__":
    main()