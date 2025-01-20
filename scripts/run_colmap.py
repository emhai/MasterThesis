import subprocess

from PIL import Image, ImageOps
import os
import argparse
import utils


def run(path):
    path = path.rstrip("/")

    new_folder_path = os.path.join(os.path.dirname(path), "colmap_images")
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)

    original_env = os.environ.copy()

    print(f"Running Colmap on {path}")
    # https://chatgpt.com/c/67891c7d-8db4-8001-8f47-5e79e6e89c68 -- help from chatgpt
    # Important! deactivate scripts - activate nerfstudio - deactivate nerfstudio - activate scripts
    subprocess.run(
        f'bash -c "source ~/.zshrc && conda deactivate && conda activate nerfstudio && ns-process-data images --data {path} --output-dir {new_folder_path}"',
        shell=True)

    os.environ.clear()
    os.environ.update(original_env)


def main():
    """
    Takes path ../name/original_images and runs colmap (via nerfstudio)
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('path', type=utils.dir_path, help='Path to the directory')

    args = parser.parse_args()
    run(args.path)


if __name__ == "__main__":
    main()
