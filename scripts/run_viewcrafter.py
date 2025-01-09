import argparse
import shutil
import subprocess
import utils
import os
import re
import stat


def run(path):

    # in ViewCrafter folder
    script_path = '/home/emmahaidacher/Desktop/viewcrafter/ViewCrafter/run_sparse.sh'
    script_folder = os.path.dirname(script_path)

    modified_script_folder = os.path.join(os.path.dirname(path), "viewcrafter_scripts")

    if not os.path.exists(modified_script_folder):
        os.makedirs(modified_script_folder)

    with open(script_path, 'r') as file:
        script_content = file.read()

    for subdir in os.listdir(path):
        subdir_path = os.path.join(path, subdir)
        files = [f for f in os.listdir(subdir_path)]

        if len(files) != 2:
            print("ERROR: There should be exactly two files in " + subdir_path)
            exit()

        name = subdir.replace("test", "")
        image_dir = subdir_path
        out_dir = os.path.join(os.path.dirname(path), "outs", "out" + name)
        video_length = 16
        modified_script_path = os.path.join(modified_script_folder, "script" + name + ".sh")

        modified_content = re.sub(r'--image_dir\s+\S+', f'--image_dir {image_dir}', script_content)
        modified_content = re.sub(r'--out_dir\s+\S+', f'--out_dir {out_dir}', modified_content)
        modified_content = re.sub(r'--video_length\s+\S+', f'--video_length {video_length}', modified_content)
        #modified_content = re.sub(r'python\s+\S+', f'python {modified_script_path}', modified_content)


        with open(modified_script_path, 'w') as file:
            file.write("#!/bin/sh\n")
            file.write(f"cd {script_folder}\n")
            file.write("conda deactivate\n")
            file.write("source /home/emmahaidacher/miniconda3/bin/activate viewcrafter\n")
            # todo get right path to conda env
            file.write(modified_content)
            st = os.stat(modified_script_path)
            os.chmod(modified_script_path, st.st_mode | stat.S_IEXEC)

        process = subprocess.Popen(modified_script_path, shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        process.wait()  # Wait for process to complete.

        # iterate on the stdout line by line
        for line in process.stdout.readlines():
            print(line)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=utils.dir_path, help='Path to the directory that contains e.g. test44to46')
    args = parser.parse_args()
    path = args.path.rstrip("/")

    run(path)

if __name__ == "__main__":
    main()