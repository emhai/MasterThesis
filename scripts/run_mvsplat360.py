import argparse
import shutil
import subprocess

from fontTools.unicodedata import script

import utils
import os
import re
import stat
import resource
import json
def run(input_path, output_path):

    json_dir = os.path.join(input_path, "json_files") # todo ACHTUNG, muss gleich sein wie in main.py
    mvsplat_dir = "/home/emmahaidacher/Desktop/mvsplat360/mvsplat360"
    with open("/home/emmahaidacher/Masterthesis/MasterThesis/scripts/mvsplat_input.txt", 'r') as file:
        script_content = file.read()

    results = {}

    for file in os.listdir(json_dir):

        test_file = os.path.join(json_dir, file)
        name = file.split(".")[0]
        modified_content = script_content
        modified_content = re.sub(r'CHOSEN_NAME', name, modified_content)
        modified_content = re.sub(r'PATH_TO_JSON', test_file, modified_content)
        modified_content = re.sub(r'PATH_TO_DATASET', input_path, modified_content)
        modified_content = re.sub(r'IMAGE_SHAPE', "[378,504]", modified_content) # e.g. [378,504] -- [h,w]
        modified_content = re.sub(r'PATH_TO_OUT_DIR', output_path, modified_content)
        modified_content = modified_content.replace("\n", "")

        original_env = os.environ.copy()
        # https://stackoverflow.com/questions/13889066/run-an-external-command-and-get-the-amount-of-cpu-it-consumed/13933797#13933797
        usage_start = resource.getrusage(resource.RUSAGE_CHILDREN)
        print("Currently running:", name)
        subprocess.run(
            f'bash -c "source ~/.zshrc && conda deactivate && conda activate mvsplat360 && cd {mvsplat_dir} && {modified_content}"',
            shell=True)
        usage_end = resource.getrusage(resource.RUSAGE_CHILDREN)
        cpu_time = usage_end.ru_utime - usage_start.ru_utime
        os.environ.clear()
        os.environ.update(original_env)
        results[name] = {"inference_time": cpu_time, "name": name, "framework": "mvsplat360"}


    print("MVSplat360 Success")
    results_path = input_path.split("/")[0: -2]
    results_path = os.path.join("/", *results_path)
    final_results = {"mvsplat360": results}
    with open(os.path.join(results_path, "results.json"), 'w') as f:
        json.dump(final_results, f)


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