import argparse
import os
import utils
import subprocess

def run(path):

    for subdir in os.listdir(path):
        subdir_path = os.path.join(path, subdir)

        print(f"Extracting frames from {subdir_path}")
        diffusion_path = os.path.join(subdir_path, "extracted_diffusion")
        if not os.path.exists(diffusion_path):
            os.makedirs(diffusion_path)

        ffmpeg_command = ['ffmpeg', '-i', os.path.join(subdir_path, "diffusion.mp4"), f"{diffusion_path}/diffusion_frame_%04d.jpg"]
        subprocess.run(ffmpeg_command)

        render_path = os.path.join(subdir_path, "extracted_render")
        if not os.path.exists(render_path):
            os.makedirs(render_path)

        ffmpeg_command = ['ffmpeg', '-i', os.path.join(subdir_path, "render.mp4"), f"{render_path}/render_frame_%04d.jpg"]
        subprocess.run(ffmpeg_command)

def main():
    """
    Takes path ../name/output and iterates through all created results (by viewcrafter). Subsequently extracts the frames from
    diffusion.mp4 to folder ../name/output/../extracted_diffusion and render.mp4 to folder ../name/output/../extracted_render
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=utils.dir_path, help='Path to ../name/output')
    args = parser.parse_args()
    run(args.path)

if __name__ == "__main__":
    main()