import argparse
import shutil
import subprocess

import utils
import os
import re
import stat
import resource
import json

def run(input_path, output_path, scripts_path):

    # in ViewCrafter folder
    ori_script_path = '/home/emmahaidacher/Desktop/viewcrafter/ViewCrafter/run_sparse.sh'
    ori_script_folder = os.path.dirname(ori_script_path)
    outer_path = input_path.split("/")[0: -2]
    results_path = os.path.join("/", *outer_path, "results.json")
    stdout_path = os.path.join("/", *outer_path, "output.json")

    with open(ori_script_path, 'r') as file:
        script_content = file.read()

    results = {}

    for name in os.listdir(input_path):
        in_dir = os.path.join(input_path, name)
        files = [f for f in os.listdir(in_dir)]

        if len(files) != 3:
            print("ERROR: There should be exactly three files in " + in_dir)
            exit()

        out_dir = os.path.join(output_path, name)
        video_length = 16
        modified_script_path = os.path.join(scripts_path, name + ".sh")

        modified_content = script_content
        modified_content = re.sub(r'--image_dir\s+\S+', f'--image_dir {in_dir}', modified_content)
        modified_content = re.sub(r'--out_dir\s+\S+', f'--out_dir {out_dir}', modified_content)
        modified_content = re.sub(r'--video_length\s+\S+', f'--video_length {video_length}', modified_content)
        # modified_content = re.sub(r'python\s+\S+', f'python {modified_script_path}', modified_content)

        print("Currently running:", name)

        with open(modified_script_path, 'w') as file:
            file.write("#!/bin/bash\n")
            file.write("source ~/.zshrc\n")
            file.write(f"cd {ori_script_folder}\n")
            file.write("conda deactivate\n")
            file.write("source /home/emmahaidacher/miniconda3/bin/activate viewcrafter\n")
            # todo get right path to conda env
            file.write(modified_content)
            st = os.stat(modified_script_path)
            os.chmod(modified_script_path, st.st_mode | stat.S_IEXEC)

        original_env = os.environ.copy()
        # https://stackoverflow.com/questions/13889066/run-an-external-command-and-get-the-amount-of-cpu-it-consumed/13933797#13933797
        usage_start = resource.getrusage(resource.RUSAGE_CHILDREN)
        result = subprocess.run([modified_script_path], check=True, text=True, capture_output=True)
        usage_end = resource.getrusage(resource.RUSAGE_CHILDREN)
        cpu_time = usage_end.ru_utime - usage_start.ru_utime
        os.environ.clear()
        os.environ.update(original_env)

        print(result.stdout)
        extra_folder = os.path.join(out_dir, os.listdir(out_dir)[0])
        all_files = os.listdir(extra_folder)
        for f in all_files:
            shutil.move(os.path.join(extra_folder, f), out_dir)

        os.rmdir(extra_folder)
        results[name] = {"inference_time": cpu_time, "name": name, "framework": "viewcrafter"}


    print("ViewCrafter Success")


    try:
        with open(results_path, 'r') as f:
            data = json.load(f)
            data["viewcrafter"] = results
    except FileNotFoundError:
        data = {"viewcrafter": results}


    with open(results_path, 'w') as f:
        json.dump(data, f, indent=4)


def main():
    """
    Takes path ../name/input and runs viewcrafter on each pairwise image combination. This is done by copying the
    original shell file, modifying the --image_dir and --out_dir, adding some terminal commands and then running
    this modified shell scrips. The output folder is ../name/output with pattern out44x46.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', type=utils.dir_path, help='Path to the ../name/viewcrafter/input that contains e.g. 44_46')
    parser.add_argument('output_path', type=utils.dir_path, help='Path to  ../name/viewcrafter/output')
    parser.add_argument('scripts_path', type=utils.dir_path, help='Path to  ../name/viewcrafter/scripts')

    args = parser.parse_args()
    input_path = args.input_path.rstrip("/")
    output_path = args.output_path.rstrip("/")
    scripts_path = args.scripts_path.rstrip("/")

    run(input_path, output_path, scripts_path)

if __name__ == "__main__":
    main()