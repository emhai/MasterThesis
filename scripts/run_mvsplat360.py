import argparse
import io
import shutil
import subprocess

import cv2
import torch
from PIL import Image

import utils
import os
import re
import resource
import json
import generate_video

def run(input_path, output_path):

    print(f"Running MVSPLAT360 on {input_path}")
    json_dir = os.path.join(input_path, "json_files") # ACHTUNG, muss gleich sein wie in main.py
    mvsplat_dir = "/home/emmahaidacher/Desktop/mvsplat360/mvsplat360"
    with open("/home/emmahaidacher/Masterthesis/MasterThesis/scripts/mvsplat_input.txt", 'r') as file:
        script_content = file.read()

    outer_path = input_path.split("/")[0: -2]
    results_path = os.path.join("/", *outer_path, "results.json")
    stdout_path = os.path.join("/", *outer_path, "output.log")

    results = {}

    for file in os.listdir(os.path.join(input_path, "test")):
        if file.endswith(".torch"):
            torch_data = torch.load(os.path.join(input_path, "test", file))
            image_tensor = torch_data[0]["images"][0]

            byte_data = image_tensor.numpy().tobytes()
            image = Image.open(io.BytesIO(byte_data))
            width, height = image.size

            size = f"[{height},{width}]"

    image_amount = len(os.listdir(json_dir))
    for i, file in enumerate(os.listdir(json_dir), start=1):

        test_file = os.path.join(json_dir, file)
        name = file.split(".")[0]
        modified_content = script_content
        modified_content = re.sub(r'CHOSEN_NAME', name, modified_content)
        modified_content = re.sub(r'PATH_TO_JSON', test_file, modified_content)
        modified_content = re.sub(r'PATH_TO_DATASET', input_path, modified_content)
        modified_content = re.sub(r'IMAGE_SHAPE', size, modified_content) # e.g. [378,504] -- [h,w]
        modified_content = re.sub(r'PATH_TO_OUT_DIR', output_path, modified_content)
        modified_content = modified_content.replace("\n", "")

        original_env = os.environ.copy()
        # https://stackoverflow.com/questions/13889066/run-an-external-command-and-get-the-amount-of-cpu-it-consumed/13933797#13933797
        usage_start = resource.getrusage(resource.RUSAGE_CHILDREN)
        print(f"Currently running {i}/{image_amount}:", name)
        with open(stdout_path, "a") as f:
            subprocess.run(
                f'bash -c "source ~/.zshrc && conda deactivate && conda activate mvsplat360 && cd {mvsplat_dir} && {modified_content}"',
                shell=True,  stdout=f, stderr=subprocess.STDOUT)
        usage_end = resource.getrusage(resource.RUSAGE_CHILDREN)
        cpu_time = usage_end.ru_utime - usage_start.ru_utime
        os.environ.clear()
        os.environ.update(original_env)
        results[name] = {"inference_time": cpu_time, "name": name, "framework": "mvsplat360"}

        generate_video.run(os.path.join(output_path, name))

    print("MVSPLAT360 Success")

    try:
        with open(results_path, 'r') as f:
            data = json.load(f)
            data["mvsplat360"] = results
    except FileNotFoundError:
        data = {"mvsplat360": results}

    with open(results_path, 'w') as f:
        json.dump(data, f, indent=4)


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