import subprocess

from PIL import Image, ImageOps
import os
import argparse
import utils

def run(input_path, output_path):

    original_env = os.environ.copy()

    print(f"Running Colmap on {input_path}")
    # got error, fixed with https://chatgpt.com/c/679a117a-c5ec-8001-8bb6-6d6679505fbc
    os.environ["QT_QPA_PLATFORM"] = "offscreen"

    # https://chatgpt.com/c/67891c7d-8db4-8001-8f47-5e79e6e89c68 -- help from chatgpt
    # Important! deactivate scripts - activate nerfstudio - deactivate nerfstudio - activate scripts
    subprocess.run(
        f'bash -c "source ~/.zshrc && conda deactivate && conda activate nerfstudio && ns-process-data images --data {input_path} --output-dir {output_path}"',
        shell=True)

    os.environ.clear()
    os.environ.update(original_env)


def main():
    """
    Takes path ../name/original_images and runs colmap (via nerfstudio) and saves result to mvsplat360/colmap
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('input_path', type=utils.dir_path, help='Path to original_images')
    parser.add_argument('output_path', type=utils.dir_path, help='Path to mvsplat360/colmap')

    args = parser.parse_args()

    input_path = args.input_path.rstrip("/")
    output_path = args.output_path.rstrip("/")

    run(input_path, output_path)


if __name__ == "__main__":
    main()
